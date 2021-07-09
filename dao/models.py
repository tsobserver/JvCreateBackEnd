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
class User(db.Model):
    __tablename__ = 'user'
    email = db.Column(db.String(30), primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(20))


# Log表
class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userEmail = db.Column(db.String(30), db.ForeignKey('user.email'))  # 外键
    log = db.Column(db.String(50))
    date = db.Column(db.String(50))

#公司表
class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.String(30),primary_key=True)
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
    financing = db.Column(db.Boolean)
    firstTag = db.Column(db.String(20))
    secondTag = db.Column(db.String(40))
    thirdTag = db.Column(db.String(60))

#自然人表
class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    picture = db.Column(db.String(150))
    introduction = db.Column(db.String(1000))

#团队信息表
class Team(db.Model):
    __tablename__ = 'Team'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    personId = db.Column(db.Integer,db.ForeignKey('person.id'))
    companyId = db.Column(db.String(30),db.ForeignKey('company.id'))

#发明信息表
class Invention(db.Model):
    id = db.Column(db.String(30),primary_key=True)
    name = db.Column(db.String(50))
    applyDate = db.Column(db.Date)
    applyPerson = db.Column(db.String(30),db.ForeignKey('company.id'))
    inventor = db.Column(db.String(20))
    lawStatus = db.Column(db.String(10))
    abstract = db.Column(db.String(1500))
    fullText = db.Column(db.String(100))
    publishDate = db.Column(db.Date)