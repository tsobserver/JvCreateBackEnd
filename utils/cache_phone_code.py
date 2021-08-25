import time
import threading

# 根据 python 官方文档
# 以下操作为线程安全：
# --  L.append(x)
# --  L1.extend(L2)
# --  x = L[i]
# --  x = L.pop()
# --  L1[i:j] = L2
# --  L.sort()
# --  x = y
# --  x.field = y
# --  D[x] = y
# --  D1.update(D2)
# --  D.keys()
# 以下操作为非线程安全：
# --  i = i+1
# --  L.append(L[-1])
# --  L[i] = L[j]
# --  D[x] = D[x] + 1
cache_dic = {}
max_item_num = 10000
mutex = threading.Lock()


# 临时保存的验证码对象，包装了有效期
class PhoneCode:
    def __init__(self, code: str, exp_time: int):
        self.code = code
        self.exp_time = exp_time

    code: str
    exp_time: int


def set_phone_code(phone: str, code: str):
    # 过期时间(exp_time) 设置为当前时间加五分钟
    phone_code = PhoneCode(code=code, exp_time=int(time.time()) + 60 * 5)
    if not cache_dic.get(phone):
        # 该操作线程安全
        cache_dic[phone] = phone_code
        global max_item_num
        with mutex:
            if len(cache_dic) > max_item_num:
                # 需要进行内存回收
                # 遍历发现过期的验证码，调用 pop
                for key in cache_dic.keys():
                    if cache_dic[key].exp_time < int(time.time()):
                        cache_dic.pop(key)
    else:
        # 该操作线程安全
        cache_dic[phone] = phone_code


def check_phone_code(phone: str, code: str):
    if not cache_dic.get(phone):
        return False
    phone_code = cache_dic[phone]
    if phone_code.code == code and phone_code.exp_time > int(time.time()):
        # 返回True之前，删除验证码
        with mutex:
            cache_dic.pop(phone)
        return True
    return False
