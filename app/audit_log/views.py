"""
@author: zhao
@file: views.py
@time:2023/7/25  6:50 PM
"""
from flask import Blueprint
from app.audit_log.audit_log import *

audit_log_bp = Blueprint('audit_log', __name__, url_prefix='/audit_log')
audit_log_bp.add_url_rule('/show', view_func=show)