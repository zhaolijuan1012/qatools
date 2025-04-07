"""
@author: zhao
@file: tools.py
@time:2023/7/25  6:11 PM
"""
from flask import render_template,g


def tools():
    return render_template('tools/tools.html',user=g.user)
