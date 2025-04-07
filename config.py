"""
@author: zhao
@file: config.py
@time:2023/7/25  3:44 PM
"""


class Production:
    Env = 'production'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@qatools_db:3306/qatools?charset=utf8"  # 数据库
    SQLALCHEMY_ECHO = True  # 调试设置为True
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 不追踪对象的修改
    REDIS_HOST = 'redis'
    REDIS_PORT = 6379
    REDIS_DB = 0
    UPLOAD_FOLDER = 'uploads'


class Development:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/qatools?charset=utf8"  # 数据库
    SQLALCHEMY_ECHO = True  # 调试设置为True
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 不追踪对象的修改
    Env = 'development'
    DEBUG = True
    REDIS_HOST = 'redis'
    REDIS_PORT = 6379
    REDIS_DB = 0
    AA = 1
    UPLOAD_FOLDER = 'uploads'