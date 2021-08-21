#!/Users/panliang/.pyenv/versions/3.7.9/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/23 23:45
# @Author  : panlianghnu
# @File    : AjaxJson.py
# @Software: PyCharm


from flask import Flask, g, send_from_directory, jsonify
from flask import request, abort
from string import Template
from utils.middlewares import jwt_authentication
import json
import utils.mail
from utils import jwt_util
from flask import make_response
from dao import config
from dao.exts import db
from dao.models import Company, Invention, Collect, User
import requests
import time
import os.path
from secret import appSecret

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
appId = 'wx9b920bb75dbff842'
invention_pdf_path = '/invention_pdf'

# def make_log(userEmail, log):
#     tmp_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#     log = Log(userEmail=userEmail, date=str(tmp_time), log=log)
#     db.session.add(log)
#     db.session.commit()
#     pass

# for test
@app.route('/')
def index():
    return "Hello World"


@app.route('/hotSearch')
def hotSearch():
    sql = 'select * from company order by searchCount desc limit 28'
    result = db.session.execute(sql)
    data = []
    for company in result:
        temp = {'id': company.id, 'companyName': company.name, 'field': company.field, 'formDate': company.formDate,
                'registeredCapital': company.registeredCapital,
                'tel': company.tel, 'inventionRating': company.InventionRating, 'webSite': company.webSite,
                'legalPersonType': company.legalPersonType,
                'legalPerson': company.legalPerson, 'registerStatus': company.registeredStatus, 'CEO': company.CEO,
                'manager': company.manager,
                'inventionCount': company.inventionCount,
                'address': company.address, 'businessScope': company.businessScope,
                'introduction': company.introduction, 'financing': company.financing,
                'firstTag': company.firstTag, 'secondTag': company.secondTag, 'thirdTag': company.thirdTag,
                'searchCount': company.searchCount, 'companyPic': company.logo}
        data.append(temp)
    return jsonify(data)


@app.route('/search')
def search():
    searchValue = request.args.get('searchValue')
    # 搜索内容判空或空格
    if not searchValue or searchValue == '' or searchValue.isspace():
        return hotSearch()
    match_rule = 'company.id=team.companyId and ' \
                 'team.personId=person.id '
    # 如果 searchValue 是一个以空格分割的列表，则将每一项作为并列搜索条件
    searchValueList = searchValue.split(' ')
    for value in searchValueList:
        value = '"%' + value + '%"'
        match_rule = match_rule + ' and (' \
                                  f'field like {value} or ' \
                                  f'company.name like {value} or ' \
                                  f'firstTag like {value} or ' \
                                  f'secondTag like {value} or ' \
                                  f'thirdTag like {value} or ' \
                                  f'address like {value} or ' \
                                  f'financing like {value} or ' \
                                  f'person.name like {value} ' \
                                  ')'
    sql = f'select distinct company.* from company,team,person where {match_rule} order by searchCount desc'
    result = db.session.execute(sql)
    data = []
    for company in result:
        temp = {'id': company.id, 'companyName': company.name, 'field': company.field,
                'formDate': str(company.formDate),
                'registeredCapital': company.registeredCapital,
                'tel': company.tel, 'inventionRating': company.InventionRating, 'webSite': company.webSite,
                'legalPersonType': company.legalPersonType,
                'legalPerson': company.legalPerson, 'registerStatus': company.registeredStatus, 'CEO': company.CEO,
                'manager': company.manager,
                'inventionCount': company.inventionCount,
                'address': company.address, 'businessScope': company.businessScope,
                'introduction': company.introduction, 'financing': company.financing,
                'firstTag': company.firstTag, 'secondTag': company.secondTag, 'thirdTag': company.thirdTag,
                'searchCount': company.searchCount, 'companyPic': company.logo}
        data.append(temp)
    return jsonify(data)


@app.route('/companyDetail')
def getCompanyById():
    companyId = request.args.get('id')
    company = Company.query.get(companyId)
    if company is None:
        return '404'
    # 增加一次访问量
    company.searchCount = company.searchCount + 1
    db.session.commit()

    # 判断是否该用户收藏了该公司
    isFollow = False
    userId = g.user_id
    if not userId == 'no user_id':
        # 用户已经登陆 判断是否收藏
        sql = f'select * from collect where companyId = "{company.id}" and userId = "{userId}";'
        result = db.session.execute(sql).fetchall()
        if len(result):
            isFollow = True
    print('是否关注？', isFollow)
    data = {'id': company.id, 'companyName': company.name, 'major': company.field,
            'companyRegisterDate': str(company.formDate),
            'companyRegisterMoney': company.registeredCapital,
            'phone': company.tel, 'level': company.InventionRating,
            'website': company.webSite, 'inventionNum': company.inventionCount,
            'legalPersonType': company.legalPersonType,
            'legalPerson': company.legalPerson, 'isFollow': isFollow,
            'registerStatus': company.registeredStatus, 'CEO': company.CEO,
            'manager': company.manager, 'address': company.address,
            'businessScope': company.businessScope, 'introduction': company.introduction,
            'invest': company.financing, 'firstTag': company.firstTag,
            'secondTag': company.secondTag, 'thirdTag': company.thirdTag,
            'searchCount': company.searchCount, 'logo': company.logo}
    return jsonify(data)


@app.route('/invention')
def getInventionsByCompanyId():
    companyId = request.args.get('id')
    sql = 'select * from invention where applyPerson="' + companyId + '" order by applyDate desc;'
    result = db.session.execute(sql)
    ret = []
    for invention in result:
        temp = {
            'id': invention.id,
            'name': invention.name,
            'filingDate': str(invention.applyDate),
            'status': invention.lawStatus,
            'abstract': invention.abstract,
            'fullText': invention.fullText,
            'inventionPerson': invention.inventor
        }
        ret.append(temp)
    return jsonify(ret)


@app.route('/inventionDetail')
def getInventionDetail():
    inventionId = request.args.get('id')
    result = Invention.query.get(inventionId)
    data = {'id': result.id, 'name': result.name,
            'filingDate': str(result.applyDate),
            'applyPerson': result.applyPerson,
            'inventionPerson': result.inventor, 'status': result.lawStatus,
            'abstract': result.abstract,
            'fullText': result.fullText,
            'publishDate': str(result.publishDate)}
    # print(jsonify(data))
    return jsonify(data)


@app.route('/stock')
def getStocksByCompanyId():
    companyId = request.args.get('id')
    sql = 'select * from stock where companyId="' + companyId + '" order by `date` desc;'
    result = db.session.execute(sql)
    ret = []
    for stock in result:
        if len(str(stock.investor)) > 5:
            isPerson = False
        else:
            isPerson = True
        temp = {
            'isPerson': isPerson,
            'id': stock.id,
            'name': stock.investor,
            'money': stock.capital,
            'percent': stock.percent,
            'date': str(stock.date)
        }
        ret.append(temp)
    return jsonify(ret)


@app.route('/change')
def getChangesByCompanyId():
    companyId = request.args.get('id')
    sql = 'select * from `change` where companyId="' + companyId + '" order by `date` desc;'
    result = db.session.execute(sql)
    ret = []
    for change in result:
        temp = {
            'date': str(change.date),
            'changeItem': change.changeItem,
            'beforeChange': change.beforeChange,
            'afterChange': change.afterChange
        }
        ret.append(temp)
    return jsonify(ret)


@app.route('/financing')
def getFinancingByCompanyId():
    companyId = request.args.get('id')
    sql = 'select * from invest where companyId="' + companyId + '" order by `date` desc;'
    result = db.session.execute(sql)
    ret = []
    for invest in result:
        content = []
        if invest.round:
            content.append('轮次：' + invest.round)
        if invest.investor:
            content.append('投资者：' + invest.investor)
        if invest.capital:
            content.append('金额：' + invest.capital)
        if invest.FA:
            content.append('融资顾问：' + invest.FA)
        temp = {
            'title': str(invest.date),
            'content': content
        }
        ret.append(temp)
    return jsonify(ret)


@app.route('/customer')
def getCustomersByCompanyId():
    companyId = request.args.get('id')
    sql = 'select * from client where companyId="' + companyId + '";'
    result = db.session.execute(sql)
    ret = []
    for client in result:
        temp = {
            'id': client.id,
            'name': client.name,
            'picture': client.picture,
            'introduction': client.introduction
        }
        ret.append(temp)
    return jsonify(ret)


@app.route('/legalCase')
def getLegalCasesByCompanyId():
    companyId = request.args.get('id')
    sql = 'select * from legalcase where companyId="' + companyId + '" order by publishDate desc;'
    result = db.session.execute(sql)
    ret = []
    for legalcase in result:
        temp = {
            'id': legalcase.id,
            'judgeDate': str(legalcase.judgeDate),
            'caseName': legalcase.caseName,
            'caseNumber': legalcase.caseNumber,
            'publishDate': str(legalcase.publishDate),
            'reason': legalcase.reason,
            'role': legalcase.role,
            'result': legalcase.result,
            'money': legalcase.money,
            'court': legalcase.court
        }
        ret.append(temp)
    return jsonify(ret)


@app.route('/getFinance')
# 经营状况-公司财务
def getFinanceByCompanyId():
    companyId = request.args.get('id')
    sql = 'select * from finance where companyId="' + companyId + '" order by year desc;'
    result = db.session.execute(sql)
    ret = []
    for finance in result:
        temp = {
            'id': finance.id,
            "year": finance.year,
            "turnover": finance.turnover,
            "profits": finance.profits
        }
        ret.append(temp)
    return jsonify(ret)


@app.route('/getEmploy')
# 经营状况-招聘信息
def getEmployByCompanyId():
    companyId = request.args.get('id')
    sql = 'select * from employ where companyId="' + companyId + '" order by `date` desc;'
    result = db.session.execute(sql)
    ret = []
    for employ in result:
        temp = {
            "id": employ.id,
            "date": str(employ.date),
            "position": employ.position,
            "salary": employ.salary,
            "education": employ.education,
            "workExperience": employ.workExperience,
            "region": employ.region
        }
        ret.append(temp)
    return jsonify(ret)


@app.route('/getQualification')
# 经营状况-资质证书
def getQualificationByCompanyId():
    companyId = request.args.get('id')
    sql = 'select * from qualification where companyId="' + companyId + '" order by StartDate desc;'
    result = db.session.execute(sql)
    ret = []
    for qualification in result:
        temp = {
            "id": qualification.id,
            "startDate": str(qualification.StartDate),
            "type": qualification.type,
            "productName": qualification.productName,
            "number": qualification.number,
            "endDate": str(qualification.endDate)
        }
        ret.append(temp)
    return jsonify(ret)


@app.route('/getAdmin')
# 经营状况-行政许可
def getAdminByCompanyId():
    companyId = request.args.get('id')
    sql = 'select * from adminlicense where companyId="' + companyId + '" order by StartDate desc;'
    result = db.session.execute(sql)
    ret = []
    for adminlicense in result:
        temp = {
            "id": adminlicense.id,
            "fileNumber": adminlicense.fileNumber,
            "department": adminlicense.department,
            "startDate": str(adminlicense.StartDate),
            "endDate": str(adminlicense.endDate),
            "content": adminlicense.content
        }
        ret.append(temp)
    return jsonify(ret)


@app.route('/product')
# 经营状况-行政许可
def getProductsByCompanyId():
    companyId = request.args.get('id')
    sql = 'select * from product where companyId="' + companyId + '";'
    result = db.session.execute(sql)
    ret = []
    for product in result:
        temp = {
            "id": product.id,
            "name": product.name,
            "picture": product.picture,
            "introduction": product.introduction
        }
        ret.append(temp)
    return jsonify(ret)


@app.route('/team')
def getTeamByCompanyId():
    companyId = request.args.get('id')
    sql = 'select person.id id, name,position,picture,introduction from team,person' \
          ' where companyId="' + companyId + '" and team.personId = person.id; '
    print('sql: ', sql)
    result = db.session.execute(sql)
    ret = []
    for person in result:
        temp = {
            'id': person.id,
            'name': person.name,
            'position': person.position,
            'picture': person.picture,
            'introduction': person.introduction
        }
        ret.append(temp)
    return jsonify(ret)


@app.route('/wxLogin')
def wxLogin():
    code = request.args.get('code')
    req_params = {
        "appid": appId,  # 小程序的 ID
        "secret": appSecret,  # 小程序的 secret
        "js_code": code,
        "grant_type": 'authorization_code'
    }
    reqResult = requests.get('https://api.weixin.qq.com/sns/jscode2session',
                             params=req_params, timeout=3, verify=False)
    info = reqResult.json()
    token = jwt_util.create_wx_token(info['openid'], info['session_key'])
    open_id = info['openid']
    # 通过 open_id 查询数据库，如果匹配则返回，如果没有匹配则添加
    # 微信用户无需保存 nickName 和 userAvatar
    user = User.query.get(open_id)
    if not user:
        db.session.add(User(id=open_id))
        db.session.commit()
    return jsonify(token)


@app.route('/invention_pdf')
def getInventionPDFByInventionId():
    inventionId = request.args.get('id')
    filename = inventionId + '.pdf'
    if not os.path.isfile(invention_pdf_path + '/' + filename):
        return abort(404)
    return send_from_directory(directory=invention_pdf_path, path=filename, as_attachment=False)


@app.route('/collect')
def collect():
    companyId = request.args.get('id')
    userId = g.user_id
    db.session.add(Collect(userId=userId, companyId=companyId))
    db.session.commit()
    return '200 OK'


@app.route('/cancelCollect')
def cancelCollect():
    companyId = request.args.get('id')
    userId = g.user_id
    collect = Collect.query.filter_by(userId=userId, companyId=companyId).first()
    db.session.delete(collect)
    db.session.commit()
    return '200 OK'


@app.route('/getCollectById')
def getCollectById():
    userId = g.user_id
    sql = f'select * from company where id in (select companyId from collect where userId = "{userId}");'
    result = db.session.execute(sql)
    ret = []
    for company in result:
        temp = {'id': company.id, 'companyName': company.name, 'field': company.field, 'formDate': company.formDate,
                'registeredCapital': company.registeredCapital,
                'tel': company.tel, 'inventionRating': company.InventionRating, 'webSite': company.webSite,
                'legalPersonType': company.legalPersonType,
                'legalPerson': company.legalPerson, 'registerStatus': company.registeredStatus, 'CEO': company.CEO,
                'manager': company.manager,
                'inventionCount': company.inventionCount,
                'address': company.address, 'businessScope': company.businessScope,
                'introduction': company.introduction, 'financing': company.financing,
                'firstTag': company.firstTag, 'secondTag': company.secondTag, 'thirdTag': company.thirdTag,
                'searchCount': company.searchCount, 'companyPic': company.logo
                }
        ret.append(temp)
    return jsonify(ret)


if __name__ == '__main__':
    app.run()
