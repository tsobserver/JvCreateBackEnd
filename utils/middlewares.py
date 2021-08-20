import time

from flask import g, request

from . import jwt_util

"""用户认证机制==>每次请求前获取并校验token"""

"@app.before_request 不使@调用装饰器 在 init文件直接装饰"


def jwt_authentication():
    """
    1.获取请求头Authorization中的token
    2.判断是否以 Bearer开头
    3.使用jwt模块进行校验
    4.判断校验结果,成功就提取token中的载荷信息,赋值给g对象保存
    """
    g.user_id = 'no user_id'
    token = request.headers.get('Authorization')
    "校验token"
    payload = jwt_util.verify_jwt(token)

    "判断token的校验结果"
    if payload and payload['open_id']:
        # 这是微信登陆
        g.user_id = payload['open_id']

    elif payload and int(time.time()) < payload.get('exp'):
        "获取载荷中的信息赋值给g对象"
        # 这是手机号登陆
        g.user_id = payload.get('id')
