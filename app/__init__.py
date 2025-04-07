from flask import Flask,g
from ext import db, bootstrap
import config
from app.views import base_bp
from app.tools.views import tools_bp
from app.interface.views import interface_bp
from app.case.views import case_bp
from app.flow.views import flow_bp
from app.user.views import user_bp
from app.audit_log.views import audit_log_bp
from app.report.views import report_bp
from app.management.views import manage_bp
import redis
import logging



  

def create_app():
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    app.config.from_object(config.Production)  # 配置文件
    db.init_app(app)  # 关联映射
    app.redis = redis.StrictRedis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], db=app.config['REDIS_DB'])
    app.register_blueprint(base_bp)  # 注册蓝图
    app.register_blueprint(tools_bp)
    app.register_blueprint(interface_bp)
    app.register_blueprint(case_bp)
    app.register_blueprint(flow_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(audit_log_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(manage_bp)  # 注册bootstrap
    app.secret_key = 'qwderfcsdsce2131fsecs'
    return app

