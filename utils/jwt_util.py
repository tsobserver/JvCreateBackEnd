import jwt
from flask import current_app
import time


def generate_jwt(payload, expiry, secret=None):
    """
    生成jwt
    :param payload: dict 载荷
    :param expiry: datetime 有效期
    :param secret: 密钥
    :return: jwt
    """
    _payload = {'exp': expiry}
    _payload.update(payload)

    if not secret:
        secret = current_app.config['JWT_SECRET']

    token = jwt.encode(_payload, secret, algorithm='HS256')
    return token.decode()


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
