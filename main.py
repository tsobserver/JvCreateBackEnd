#!/Users/panliang/.pyenv/versions/3.7.9/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/23 23:45
# @Author  : panlianghnu
# @File    : AjaxJson.py
# @Software: PyCharm


from flask import Flask, g, send_from_directory
from flask import request

from utils.middlewares import jwt_authentication
import json
import utils.mail
from utils import jwt_util
from flask import make_response
from dao import config
from dao.exts import db
from dao.models import Company
import time

app = Flask(__name__)
# 加载配置文件
app.config.from_object(config)
# db绑定app
db.init_app(app)
app.debug = True
# hook auth\
# if user login correctly,
# - g.user_email isn't the default value 'no user_email'
app.before_request(jwt_authentication)


# def make_log(userEmail, log):
#     tmp_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#     log = Log(userEmail=userEmail, date=str(tmp_time), log=log)
#     db.session.add(log)
#     db.session.commit()
#     pass


@app.route('/')
def index():
    company = Company()
    company.id = 'asdzz'
    db.session.add(company)
    db.session.commit()
    return "Hello World"


# @app.route('/login', methods=['POST'])
# def login():
#     json_data = json.loads(request.get_data().decode("utf-8"))
#     email = json_data.get('email')
#     upwd = json_data.get('password')
#     user = User.query.get(email)  # 主键查询
#     if user is not None:
#         if user.password == upwd:
#             jwt = jwt_util.create_token(email)
#             response = make_response({'email': email, 'succMsg': '欢迎用户：' + user.username})
#             response.headers['token'] = jwt
#             make_log(userEmail=email, log='登陆AIDrug')
#             return response

    # sql = 'select * from user where email = "'+email+'" and password = "'+upwd+'";'
    # result = db.session.execute(sql)
    # for user in result:
    #     if user is not None:
    #         account_id = user.id
    #         jwt = jwt_util.create_token(account_id, email)
    #         response = make_response({'email': email, 'succMsg': '欢迎用户：' + user.username})
    #         response.headers['token'] = jwt
    #         return response

    return "账号或密码错误", 401  # 后端返回401状态码，前端收到后会自动跳到登陆页面


# @app.route('/register', methods=['POST'])
# def register():
#     json_data = json.loads(request.get_data().decode("utf-8"))
#     uname = json_data.get('username')
#     email = json_data.get('email')
#     upwd = json_data.get('password')
#     code = json_data.get('code')
#     if utils.mail.generate_code(email) != code:
#         return '验证码错误', 403
#     user = User.query.get(email)  # 主键查询
#     if user is not None:
#         return '邮箱已被注册', 403
#     # sql = 'select email from user where email="' + email + '";'
#     # result = db.session.execute(sql)
#     # for user in result:
#     #     if user is not None:
#     #         return '邮箱已被注册', 403
#     user = User(username=uname, password=upwd, email=email)
#     db.session.add(user)
#     db.session.commit()  # 因为外键，必须先commit register
#     make_log(userEmail=email, log='欢迎加入AIDrug')
#     return login()
#
#
# @app.route('/changePSW', methods=['POST'])
# def changePSW():
#     json_data = json.loads(request.get_data().decode("utf-8"))
#     email = json_data.get('email')
#     upwd = json_data.get('password')
#     code = json_data.get('code')
#     if utils.mail.generate_code(email) != code:
#         return '验证码错误', 403
#     user = User.query.get(email)  # 主键查询
#     if user is None:
#         return '邮箱未被注册', 403
#     user.password = upwd
#     db.session.commit()
#     return login()
#
#
# @app.route('/get_verify_code', methods=['POST'])
# def get_verify_code():
#     json_data = json.loads(request.get_data())
#     email = json_data.get('email')
#     if_send = utils.mail.send_verify_code(receiver=email)
#     if if_send:
#         return '验证码发送成功', 200
#     return '验证码发送失败', 500
#
#
# @app.route('/test_mysql', methods=['GET', 'POST'])
# def test():
#     if request.method == 'POST':
#         print('进入TEST_POST方法')
#         use = User(username='hah', password='123', email='heih@asd')
#         db.session.add(use)
#         db.session.commit()
#         return "进入TEST_POST方法"
#     elif request.method == 'GET':
#         print('进入TEST_GET方法')
#         # sql = 'select * from user'
#         # result = db.session.execute(sql)
#         # for i in result:
#         #     print(i.username)
#         users = User.query.all()
#         print('用户们的名称：')
#         for i in users:
#             print(i.username)
#         return "进入TEST_GET方法"
#     pass
#
#
# @app.route('/test_token', methods=['POST'])
# def test_token():
#     if request.method == 'POST':
#         pass
#
#
# @app.route('/format_file', methods=['GET'])
# def format_file():
#     if g.user_email == 'no user_email':
#         return "请登陆", 401
#     direct = '/Users/panliang/Documents/湖南大学/本科/毕业设计/flask-backend'
#     return send_from_directory(directory=direct, filename='format_file.txt', as_attachment=True)
#
#
# @app.route('/drug_dict_file', methods=['GET'])
# def drug_dict_file():
#     if g.user_email == 'no user_email':
#         return "请登陆", 401
#     direct = '/Users/panliang/Documents/湖南大学/本科/毕业设计/flask-backend/algorithm/dataset'
#     return send_from_directory(directory=direct, filename='drug_dict.txt', as_attachment=True)
#
#
# @app.route('/getLog', methods=['POST'])
# def getLog():
#     if g.user_email == 'no user_email':
#         return "请登陆", 401
#     # json_data = json.loads(request.get_data())
#     # email = json_data.get('email')
#     email = g.user_email
#     print('getLog_email:', email)
#     sql = 'select * from log where userEmail="' + email + '";'
#     result = db.session.execute(sql)
#     json_data = []
#     for row in result:
#         data = {'date': str(row[3]), 'log': str(row[2]), 'userEmail': str(row[1])}
#         json_data.append(data)
#     print('json.dumps', json.dumps(json_data))
#     return json.dumps(json_data)


if __name__ == '__main__':
    app.run()
