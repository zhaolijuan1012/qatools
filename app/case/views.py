"""
@author: zhao
@file: views.py
@time:2023/7/25  6:49 PM
"""
from flask import Blueprint
from app.case.case import *

case_bp = Blueprint('case', __name__, url_prefix='/case')
case_bp.add_url_rule('/show', view_func=show)
case_bp.add_url_rule('/add_case', view_func=add_case,methods=['POST'])
case_bp.add_url_rule('/edit_case', view_func=edit_case,methods=['POST'])
case_bp.add_url_rule('/del_case', view_func=del_case)
case_bp.add_url_rule('/export_cases', view_func=export_cases)
case_bp.add_url_rule('/test_case', view_func=test_case,methods=['POST'])