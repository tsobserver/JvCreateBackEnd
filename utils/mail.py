import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from hashlib import md5

my_sender = '2261834866@qq.com'  # 发件人邮箱账号
my_pass = 'jlpqkcreqyaieccc'  # 发件人邮箱密码, 可能是授权码


# 返回True则发送成功，返回False则发送失败
def send_verify_code(receiver=''):
    try:
        code = generate_code(receiver)
        msg = MIMEText('您的验证码为：' + code, 'plain', 'utf-8')
        msg['From'] = formataddr(["From AIdrug", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["nick_name", receiver])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "感谢使用AIdrug"  # 邮件的主题，也可以说是标题

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [receiver, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except smtplib.SMTPException:  # 如果 try 中的语句没有执行，则会return False
        return False
    return True


def generate_code(email: str = ""):
    code = md5(email.encode())
    return code.hexdigest()[0:4]


def send_email(receiver: str = "", content: str = "", file_path: str = ""):
    try:
        # msg = MIMEText('您的result为：' + content, 'plain', 'utf-8')
        msg = MIMEMultipart()
        msg['From'] = formataddr(["From AIdrug", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["nick_name", receiver])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "AIdrug：请查收您的DTIs预测报告"  # 邮件的主题，也可以说是标题

        with open(file_path, "r") as file:
            content = file.read()
        att = MIMEText(content, "base64", "utf-8")
        att["Content-Type"] = "application/octet-stream"
        att["Content-Disposition"] = 'attachment; filename="result.txt"'
        msg.attach(att)

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [receiver, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except smtplib.SMTPException:  # 如果 try 中的语句没有执行，则会return False
        return False
    return True
