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

# 首页，招生台账页面
@app.route('/catalog')
def catalog():
    try:
        cursor = connection.cursor()
        query = """
        SELECT ac.disciplineid, ac.direction, ac.mentoridentity, ac.totalquota, 
               ac.additionalquota, ac.preliminarysubjects, ac.reexaminationsubjects, 
               acm.hasadmissionrights
        FROM AdmissionCatalog ac
        LEFT JOIN AdmissionCatalogStatus acm ON ac.disciplineid = acm.disciplineid;
        """
        cursor.execute(query)
        records = cursor.fetchall()
        return render_template('catalog.html', records=records)
    except Exception as e:
        return f"查询数据失败：{e}"

if __name__ == '__main__':
    app.run(debug=True)
