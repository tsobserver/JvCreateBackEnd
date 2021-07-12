# 建表写在models.py文件里面
from .exts import db

"""
建表
以下表关系：
一个用户对应多篇文章（一对多）
一篇文章对应多个标签，一个标签对应多个文章（多对多）
"""
"""
一对一关系中，需要设置relationship中的uselist=Flase，其他数据库操作一样。
一对多关系中，外键设置在多的一方中，关系（relationship）可设置在任意一方。
多对多关系中，需建立关系表，设置 secondary=关系表
"""


# 用户表
# class User(db.Model):
#     __tablename__ = 'user'
#     email = db.Column(db.String(30), primary_key=True)
#     username = db.Column(db.String(30))
#     password = db.Column(db.String(20))
#
#
# # Log表
# class Log(db.Model):
#     __tablename__ = 'log'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     userEmail = db.Column(db.String(30), db.ForeignKey('user.email'))  # 外键
#     log = db.Column(db.String(50))
#     date = db.Column(db.String(50))

#公司表
class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.String(30),primary_key=True) # 统一社会信用代码
    name = db.Column(db.String(50))
    field = db.Column(db.String(50))
    formDate = db.Column(db.Date)
    registeredCapital = db.Column(db.String(20))
    tel = db.Column(db.String(15))
    InventionRating = db.Column(db.String(5))
    webSite = db.Column(db.String(100))
    legalPersonType = db.Column(db.Boolean)
    legalPerson = db.Column(db.String(50))
    registeredStatus = db.Column(db.String(10))
    CEO = db.Column(db.String(10))
    manager = db.Column(db.String(10))
    address = db.Column(db.String(50))
    businessScope = db.Column(db.String(1000))
    introduction = db.Column(db.String(1000))
    financing = db.Column(db.String(16))
    firstTag = db.Column(db.String(20))
    secondTag = db.Column(db.String(40))
    thirdTag = db.Column(db.String(60))
    searchCount = db.Column(db.Integer)

#自然人表
class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(20))
    picture = db.Column(db.String(150))
    introduction = db.Column(db.String(1000))

#团队信息表
class Team(db.Model):
    __tablename__ = 'team'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    personId = db.Column(db.Integer,db.ForeignKey('person.id'))
    companyId = db.Column(db.String(30),db.ForeignKey('company.id'))

#发明信息表
class Invention(db.Model):
    __tablename__ = 'invention'
    id = db.Column(db.String(30),primary_key=True) #申请号
    name = db.Column(db.String(50))
    applyDate = db.Column(db.Date)
    applyPerson = db.Column(db.String(30),db.ForeignKey('company.id'))
    inventor = db.Column(db.String(20))
    lawStatus = db.Column(db.String(10))
    abstract = db.Column(db.String(1500))
    fullText = db.Column(db.String(100))
    publishDate = db.Column(db.Date)

#融资情况表
class Invest(db.Model):
    __tablename__ = 'invest'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    date = db.Column(db.Date)
    round = db.Column(db.String(16))
    capital = db.Column(db.String(20))
    investor = db.Column(db.String(50))
    FA = db.Column(db.String(50))
    companyId = db.Column(db.String(30),db.ForeignKey('company.id'))

#股权结构表
class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    companyId = db.Column(db.String(30), db.ForeignKey('company.id'))
    investor = db.Column(db.String(50))
    date = db.Column(db.Date)
    capital = db.Column(db.String(20))
    percent = db.Column(db.String(15))

#变更记录表
class Change(db.Model):
    __tablename__ = 'change'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    date = db.Column(db.Date)
    content = db.Column(db.String(100))
    companyId = db.Column(db.String(30), db.ForeignKey('company.id'))

#产品服务表
class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(50))
    picture = db.Column(db.String(150))
    introduction = db.Column(db.String(1500))
    companyId = db.Column(db.String(30), db.ForeignKey('company.id'))

#主要客户表
class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(50))
    picture = db.Column(db.String(150))
    introduction = db.Column(db.String(1500))
    companyId = db.Column(db.String(30), db.ForeignKey('company.id'))

#财务状况表
class Finance(db.Model):
    __tablename__ = 'finance'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    companyId = db.Column(db.String(30), db.ForeignKey('company.id'))
    year = db.Column(db.String(6))
    turnover = db.Column(db.String(20))
    profits = db.Column(db.String(20))

#资质证书表
class Qualification(db.Model):
    __tablename__ = 'qualification'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    companyId = db.Column(db.String(30), db.ForeignKey('company.id'))
    StartDate = db.Column(db.Date)
    type = db.Column(db.String(30))
    number = db.Column(db.String(40))  #证书编号
    endDate = db.Column(db.Date)

#招聘信息表
class Employ(db.Model):
    __tablename__ = 'employ'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    companyId = db.Column(db.String(30), db.ForeignKey('company.id'))
    date = db.Column(db.Date)
    position = db.Column(db.String(20))
    salary = db.Column(db.String(20))
    education = db.Column(db.String(10))
    workExperience = db.Column(db.String(20))
    region = db.Column(db.String(20))

#行政许可表
class AdminLicense(db.Model):
    __tablename__ = 'adminlicense'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    companyId = db.Column(db.String(30), db.ForeignKey('company.id'))
    StartDate = db.Column(db.Date)
    endDate = db.Column(db.Date)
    fileNumber = db.Column(db.String(40)) #文书编号
    fileName = db.Column(db.String(30))
    department = db.Column(db.String(40))
    content = db.Column(db.String(200))

#细分行业表
class Field(db.Model):
    __tablename__ = 'field'
    secondTag = db.Column(db.String(40),primary_key=True)
    introduction = db.Column(db.String(1500))

#经营异常表
class BusinessException(db.Model):
    __tablename__ = 'businessexception'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    companyId = db.Column(db.String(30), db.ForeignKey('company.id'))
    StartDate = db.Column(db.Date)
    endDate = db.Column(db.Date)
    startReason = db.Column(db.String(200))
    endReason = db.Column(db.String(200))
    department = db.Column(db.String(40))

#行政处罚表
class AdminPunish(db.Model):
    __tablename__ = 'adminpunish'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    companyId = db.Column(db.String(30), db.ForeignKey('company.id'))
    date = db.Column(db.Date)
    fileNumber = db.Column(db.String(40))  # 决定文书编号
    reason = db.Column(db.String(200))
    result = db.Column(db.String(200))
    department = db.Column(db.String(40))

#法律诉讼表
class LegalCase(db.Model):
    __tablename__ = 'legalcase'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    companyId = db.Column(db.String(30), db.ForeignKey('company.id'))
    judgeDate = db.Column(db.Date)
    caseName = db.Column(db.String(100))
    caseNumber = db.Column(db.String(30))
    reason = db.Column(db.String(200))
    role = db.Column(db.String(20))
    result = db.Column(db.Date)
    money = db.Column(db.String(20))
    court = db.Column(db.String(30))
    publishDate = db.Column(db.Date)