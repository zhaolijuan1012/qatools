from app import create_app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand  # 导入migrate
from ext import db, bootstrap
from app.models import *
import logging
from logging.handlers import RotatingFileHandler
from flask import g, request, redirect, url_for, render_template, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

''' 主运行文件'''
# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'
app = create_app()
manager = Manager(app=app)
migrate = Migrate(app=app, db=db)  # migrate和flask连接
manager.add_command('db', MigrateCommand)  # migrate和manager命令连接
bootstrap.init_app(app=app)

def setup_logger(app):
    # Set up file logging
    file_handler = RotatingFileHandler('your_log_file.log', maxBytes=1024*1024*100, backupCount=10)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(file_handler)

    # Set up console logging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(console_handler)
    # Set up SQLAlchemy logging
    sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
    sqlalchemy_logger.setLevel(logging.INFO)
    sqlalchemy_logger.addHandler(file_handler)  # Add the same file handler to SQLAlchemy logger


    app.logger.setLevel(logging.INFO)


# @app.teardown_request
# def del_redis():
#     for elem in app.redis.keys():
#         app.redis.delete(elem)
# setup_logger(app)


@app.before_request
def get_user():
        # 从会话中获取用户信息
        user_id = session.get('user_id')
        if user_id:
            # 这里可以根据 user_id 从数据库中获取用户详细信息
            user = Users.query.filter_by(id=user_id).first()
            # 并将用户信息存储到 g 对象中
            g.user = user
        else:
            g.user = None
            if request.endpoint not in ['user.login','user.register', 'static']:
                return render_template('user/login.html', msg='请先登录')


# 自动生成数据
@manager.command
def generate_data():
    '''默认生成一个root用户'''
    with app.app_context():
        # 检查数据库中是否已经有数据
        if not Users.query.first():
            # 创建用户对象
            password = generate_password_hash('123456')
            user = Users(username='root', password=password,realpassword='123456', email='root@example.com',phone='13800138000')
            # 将用户对象添加到会话中
            db.session.add(user)
            # 提交会话，将数据保存到数据库
            db.session.commit()

@app.template_filter('password_hash')
def str_title(str):
    return str.title()

if __name__ == '__main__':
    print(app.url_map)  # 打印接口
    # generate_data()  # 生成root用户数据
    manager.run()  # 启动程序  python3 run.py runserver

