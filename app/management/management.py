"""
@author: zhao
@file: management.py
@time:2025/4/5  8:33 PM
"""
from flask import render_template, request, redirect, url_for, flash, g, jsonify
from app.models import *


def environment_list():
    environments = Environment.query.all()
    default_env = Environment.query.filter_by(is_default=True).first()
    return render_template('management/environment.html', envs=environments, user=g.user,default_env=default_env)


def add_env():
    if request.method == 'POST':
        name = request.form['name']
        host = request.form['host']
        port = request.form['port']
        description = request.form['description']
        # 检查字段是否存在且不为空
        if not name or not host or not port:
            return jsonify({'code': 400, 'message': '名称、Host、端口、描述都不能为空'})
        env = Environment.query.filter_by(name=name).first()
        if env:
            return jsonify({'code': 400,'message': '环境名称已存在'})
        new_env = Environment(name=name, host=host, port=port, description=description,creator=g.user.username,mender=g.user.username)
        db.session.add(new_env)
        db.session.commit()
        return jsonify({'code': 200,'message': '添加环境成功'})



def set_default_env():
    if request.method == 'POST':
        env_id = request.form['default_env']
        now_default_env = Environment.query.filter_by(is_default=True).all()
        env = Environment.query.filter_by(id=env_id).first()
        if not env:
            return jsonify({'code': 400,'message': '环境不存在'})
        env.is_default = True
        for e in now_default_env:
            e.is_default = False
        db.session.add(env)
        db.session.commit()
        return jsonify({'code': 200,'message': '设置默认环境成功'})


def module_list():
    modules = Module.query.all()
    return render_template('management/module.html', modules=modules, user=g.user)


def add_module():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        module = Module.query.filter_by(name=name).first()
        if module:
            return jsonify({'code': 400,'message': '模块名称已存在'})
        new_module = Module(name=name, description=description, creator=g.user.username, mender=g.user.username)
        db.session.add(new_module)
        db.session.commit()
        return jsonify({'code': 200,'message': '添加模块成功'})