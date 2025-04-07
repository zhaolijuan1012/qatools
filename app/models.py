"""
@author: zhao
@file: models.py
@time:2023/7/24  6:41 PM
"""
from ext import db
from datetime import datetime


class Users(db.Model):
    # __tablename__ = 'user_table'  # 默认为类的小写，可自定义表的名字
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    realpassword = db.Column(db.String(128), nullable=False)
    phone = db.Column(db.String(11), nullable=False, unique=True)
    email = db.Column(db.String(30), unique=True,default='')
    isdelete = db.Column(db.Boolean, default=False)
    add_time = db.Column(db.DateTime, default=datetime.now)

    def __str__(self):
        return self.username


class Interface(db.Model):
    # __tablename__ = 'user_table'  # 默认为类的小写，可自定义表的名字
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    interfaceDescription = db.Column(db.Text(), nullable=False)
    interfaceURL = db.Column(db.Text(), nullable=False)
    request_method = db.Column(db.String(11), nullable=False)
    creator = db.Column(db.String(11), nullable=False)
    add_time = db.Column(db.DateTime, default=datetime.now)
    mender = db.Column(db.String(11), nullable=False)
    edit_time = db.Column(db.DateTime, default=datetime.now)
    module = db.Column(db.String(11), nullable=False)

    def __str__(self):
        return '获取接口'


class Case(db.Model):
    # __tablename__ = 'user_table'  # 默认为类的小写，可自定义表的名字
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    caseDescription = db.Column(db.Text(), nullable=False)
    # InterfaceID = db.Column(db.Integer, nullable=False)
    request = db.Column(db.JSON(),default='')
    response = db.Column(db.JSON(),default='')
    creator = db.Column(db.String(11), nullable=False)
    add_time = db.Column(db.DateTime, default=datetime.now)
    mender = db.Column(db.String(11), nullable=False)
    edit_time = db.Column(db.DateTime, default=datetime.now)
    module = db.Column(db.String(11), nullable=False)
    flowID = db.Column(db.Text(),default='')
    request_parameterization_dict = db.Column(db.String(255),default='')
    response_parameterization_dict = db.Column(db.Text(),default='')
    code = db.Column(db.Integer)
    interfaceID = db.Column(db.Integer, db.ForeignKey('interface.id'), nullable=False)
    interface = db.relationship('Interface', backref='case')

    def __str__(self):
        return '获取case'


class Flow(db.Model):
    # __tablename__ = 'user_table'  # 默认为类的小写，可自定义表的名字
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flowDescription = db.Column(db.Text(), nullable=False)
    case_list = db.Column(db.String(128),default='')
    creator = db.Column(db.String(11), nullable=False)
    add_time = db.Column(db.DateTime, default=datetime.now)
    mender = db.Column(db.String(11), nullable=False)
    edit_time = db.Column(db.DateTime, default=datetime.now)
    module = db.Column(db.String(11), nullable=False)

    def __str__(self):
        return '获取flow'
    
class Audit_log(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(128), nullable=False)
    content = db.Column(db.String(128),default='', nullable=False)
    operator = db.Column(db.String(11), nullable=False)
    operator_time = db.Column(db.DateTime, default=datetime.now)

    def __str__(self):
        return '获取审计日志'
    
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(128), nullable=False)
    content = db.Column(db.String(128),default='', nullable=False)
    operator = db.Column(db.String(11), nullable=False)
    operator_time = db.Column(db.DateTime, default=datetime.now)
    module = db.Column(db.String(11), nullable=False)
    URL = db.Column(db.Text(),default='')
    log = db.Column(db.Text(),default='')
    count = db.Column(db.Integer)
    success = db.Column(db.Integer)
    fail = db.Column(db.Integer)
    def __str__(self):
        return '获取测试报告'


class Environment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False , unique=True)
    host = db.Column(db.String(128), nullable=False)
    port = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(128),default='', nullable=False)
    creator = db.Column(db.String(11), nullable=False)
    add_time = db.Column(db.DateTime, default=datetime.now)
    mender = db.Column(db.String(11), nullable=False)
    edit_time = db.Column(db.DateTime, default=datetime.now)
    is_default = db.Column(db.Boolean, default=False)
    def __str__(self):
        return '获取环境信息'


class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.String(128),default='', nullable=False)
    creator = db.Column(db.String(11), nullable=False)
    add_time = db.Column(db.DateTime, default=datetime.now)
    mender = db.Column(db.String(11), nullable=False)
    edit_time = db.Column(db.DateTime, default=datetime.now)
    def __str__(self):
        return '获取模块信息'