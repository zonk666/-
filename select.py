from flask import Flask, request, render_template
import pyodbc

app = Flask(__name__, template_folder='templates')  # 指定模板目录

# 配置数据库连接
server = 'LAPTOP-SCP9QF2J'  # 替换为你的服务器地址
database = 'keshe'  # 替换为你的数据库名称
connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=" + server + ";"
    "Database=" + database + ";"
    "UID=sa;"  # 替换为你的用户名
    "PWD=jjllzz66;"  # 替换为你的密码
    "TrustServerCertificate=yes;"
)


try:
    connection = pyodbc.connect(connection_string)
    print("数据库连接成功！")
except Exception as e:
    print("数据库连接失败：", e)
    exit()

# 首页
@app.route('/')
def index():
    return render_template('index.html')

# 处理导师遴选
@app.route('/select_mentor', methods=['POST'])
def select_mentor():
    mentor_id = request.form.get('mentor_id')
    mentor_type = request.form.get('mentor_type')

    try:
        cursor = connection.cursor()
        query = """
        UPDATE Mentors
        SET mentorposition = ?
        WHERE mentorid = ? AND mentorposition IS NULL
        """
        cursor.execute(query, (mentor_type, mentor_id))
        connection.commit()
        return f"导师遴选成功！导师ID: {mentor_id}, 新身份: {mentor_type}"
    except Exception as e:
        return f"导师遴选失败：{e}"

# 处理导师资格审核
@app.route('/verify_mentor', methods=['POST'])
def verify_mentor():
    mentor_id = request.form.get('verify_mentor_id')
    admission_rights = request.form.get('admission_rights')

    try:
        cursor = connection.cursor()
        query = """
        UPDATE Mentors
        SET hasadmissionrights = ?
        WHERE mentorid = ?
        """
        cursor.execute(query, (admission_rights, mentor_id))
        connection.commit()
        return f"导师资格审核成功！导师ID: {mentor_id}, 招生资格: {'是' if admission_rights == '1' else '否'}"
    except Exception as e:
        return f"导师资格审核失败：{e}"

if __name__ == '__main__':
    app.run(debug=True)
