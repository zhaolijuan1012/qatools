"""
@author: zhao
@file: views.py
@time:2023/7/24  6:41 PM
路由表
"""
from flask import Blueprint
from app.tools.tools import *

tools_bp = Blueprint('tools', __name__, url_prefix='/tools')

tools_bp.add_url_rule('/', view_func=tools)
