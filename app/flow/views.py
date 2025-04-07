"""
@author: zhao
@file: views.py
@time:2023/7/25  6:55 PM
"""
from flask import Blueprint
from app.flow.flow import *

flow_bp = Blueprint('flow', __name__, url_prefix='/flow')
flow_bp.add_url_rule('/show', view_func=show)
flow_bp.add_url_rule('/<int:flowID>/detail', view_func=detail)
flow_bp.add_url_rule('/add_flow', view_func=add_flow,methods=['POST'])
flow_bp.add_url_rule('/del_flow', view_func=del_flow)
flow_bp.add_url_rule('/edit_flow', view_func=edit_flow,methods=['POST'])
flow_bp.add_url_rule('/search_case', view_func=search_case)
flow_bp.add_url_rule('/add_step', view_func=add_step,methods=['POST'])
flow_bp.add_url_rule('/del_step', view_func=del_step)
flow_bp.add_url_rule('/flows_execute', view_func=flows_execute)


