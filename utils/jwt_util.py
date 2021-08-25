import jwt
from flask import current_app
import time


def verify_jwt(token, secret='secret'):
    """
    检验jwt
    :param token: jwt
    :param secret: 密钥
    :return: dict: payload
    """
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
    except jwt.PyJWTError:
        payload = None
    return payload


def create_wx_token(open_id, session_key):
    # wx token 由 wx 管理，时间无上限
    # 这里 token 时限直接给一年 否则老是过期了，decode 检查直接给返回 None
    payload = {
        "iat": int(time.time()),
        "exp": int(time.time()) + 60*60*24*30*12,
        "open_id": open_id,
        "session_key": session_key
    }
    return jwt.encode(payload, 'secret')


def create_phone_token(phone):
    # 手机号登陆 时限一小时
    payload = {
        "iat": int(time.time()),
        "exp": int(time.time()) + 60*60,
        'phone': phone
    }
    return jwt.encode(payload, 'secret')
