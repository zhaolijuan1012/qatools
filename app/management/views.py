"""
@author: zhao
@file: views.py
@time:2025/4/5  8:33 PM
"""
import flask
from app.management.management import *
manage_bp = flask.Blueprint('manage', __name__)
manage_bp.add_url_rule('/environment_list', view_func=environment_list, methods=['GET'])
manage_bp.add_url_rule('/add_env', view_func=add_env, methods=['POST'])
manage_bp.add_url_rule('/set_default_env', view_func=set_default_env, methods=['POST'])
manage_bp.add_url_rule('/add_module', view_func=add_module, methods=['POST'])
manage_bp.add_url_rule('/module_list', view_func=module_list, methods=['GET'])