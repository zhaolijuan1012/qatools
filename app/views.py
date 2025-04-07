"""
@author: zhao
@file: views.py
@time:2023/7/25  4:07 PM
"""

from flask import Blueprint, render_template,g,request
from app.models import *
from app.common import *
base_bp = Blueprint('base', __name__)


base_bp.add_url_rule('/', view_func=overview, methods=['GET'])




