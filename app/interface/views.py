"""
@author: zhao
@file: views.py
@time:2023/7/25  6:26 PM
"""
from flask import Blueprint
from app.interface.interface import *

interface_bp = Blueprint('interface', __name__, url_prefix='/interface')
interface_bp.add_url_rule('/show', view_func=show)
interface_bp.add_url_rule('/add_interface', view_func=add_interface, methods=['POST'])
interface_bp.add_url_rule('/edit_interface', view_func=edit_interface, methods=['POST'])
interface_bp.add_url_rule('/del_interface', view_func=del_interface)
interface_bp.add_url_rule('/search_interface', view_func=search_interface)
interface_bp.add_url_rule('/export_interface', view_func=export_interface)
interface_bp.add_url_rule('/import_interfaces', view_func=import_interfaces, methods=['POST'])