"""
@author: zhao
@file: views.py
@time:2023/7/24  6:41 PM
"""
from flask import Blueprint
from app.user.user import *

user_bp = Blueprint('user', __name__, url_prefix='/user')

user_bp.add_url_rule('/login', view_func=login,methods=['POST','GET'])
# user_bp.add_url_rule('/add_user', view_func=add_user, methods=['POST'])
user_bp.add_url_rule('/register', view_func=register, methods=['POST','GET'])
user_bp.add_url_rule('/logout', view_func=logout)
user_bp.add_url_rule('/del_user', view_func=del_user)
user_bp.add_url_rule('/user_list', view_func=user_list)
user_bp.add_url_rule('/edit_user', view_func=edit_user, methods=['POST'])
user_bp.add_url_rule('/reset_password', view_func=reset_password, methods=['POST'])
user_bp.add_url_rule('/add_user', view_func=add_user, methods=['POST'])
user_bp.add_url_rule('/export_users', view_func=export_users)
user_bp.add_url_rule('/import_users', view_func=import_users, methods=['POST'])