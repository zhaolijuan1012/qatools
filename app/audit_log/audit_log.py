"""
@author: zhao
@file: audit_log.py
@time:2023/7/25  6:50 PM
"""
from flask import render_template,request,jsonify,json,g
from app.models import *
from sqlalchemy import or_
import json,datetime

def show():
    content = request.args.get('content','')
    page = int(request.args.get('page', 1))
    logs = Audit_log.query.filter(or_(Audit_log.type.like('%'+content+'%'),Audit_log.content.like('%'+content+'%'))).order_by(-Audit_log.id).paginate(page=page, per_page=10)
    return render_template('audit_log/show.html',logs=logs,content=content,user= g.user)


def add_audit_log(type,content):
    '''添加日志'''
    new_log = Audit_log(type=type,content=content,operator=g.user.username,operator_time=datetime.datetime.now())
    db.session.add(new_log)
    db.session.commit()
    return jsonify({'status': '添加审计日志成功'})