"""
@author: zhao
@file: user.py
@time:2023/7/25  8:07 PM
"""
from flask import render_template, request, redirect, url_for, g, session, jsonify, flash,current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import *
from ext import db
from app.audit_log.audit_log import add_audit_log
from sqlalchemy import and_, or_
from app.common import *


def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # user = Users.query.filter_by(and_(Users.username == username, Users.isdelete == 0)).first()
        user = Users.query.filter(and_(Users.username == username, Users.isdelete == 0)).first()

        if user == None:
            return redirect(url_for('user.login', msg='用户名不存在'))
        else:
            flag = check_password_hash(user.password, password)
            if flag:
                session['user_id'] = user.id
                g.user = user
                add_audit_log('登陆', f'用户{username}登录成功')
                return redirect(url_for('base.overview'))
            else:
                return redirect(url_for('user.login', msg='密码错误请重试'))  # 登录失败，返回登陆页面，报错message提示
    elif request.method == 'GET':
        msg = request.args.get('msg')
        return render_template('user/login.html', msg=msg)


def register():
    if request.method == 'GET':
        msg = request.args.get('msg')
        return render_template('user/register.html', msg=msg)
    elif request.method == 'POST':
        username = request.form.get('username')
        realpassword = request.form.get('password')
        password = generate_password_hash(realpassword)
        repassword = request.form.get('repassword')
        phone = request.form.get('phone')
        email = request.form.get('email')
        if realpassword != repassword:
            return render_template('user/register.html', msg='两次密码输入不一致')

        # 检查用户名是否已存在
        existing_user = Users.query.filter_by(username=username).first()
        if existing_user:
            return render_template('user/register.html', msg='用户名已存在')
        try:
            # 创建新用户记录
            user = Users(username=username, password=password, realpassword=realpassword, email=email, phone=phone)
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            return redirect(url_for('base.overview'))
        except Exception as e:
            db.session.rollback()
            return render_template('user/register.html', msg=f'注册失败: {str(e)}')


def logout():
    username = g.user.username
    session.pop('user_id', None)
    add_audit_log('退出登录', f'用户{username}退出登录')
    return redirect(url_for('user.login'))


def del_user():
    user_id = request.args.get('id')
    user = Users.query.filter_by(id=user_id).first()
    print('---------------', user.username)
    if user:
        if user.username == 'root':
            return jsonify({'code': 203, 'message': '不能删除root用户'})
        elif user.id == g.user.id:
            db.session.delete(user)
            db.session.commit()
            session.pop('user_id', None)
            add_audit_log('删除用户', f'用户{user.username}删除成功')
            return jsonify({'code': 201, 'message': '注销成功，请重新登录'})
        elif g.user.username != 'root':
            return jsonify({'code': 202, 'message': '没有权限删除用户'})
        else:
            db.session.delete(user)
            db.session.commit()
            add_audit_log('删除用户', f'用户{user.username}删除成功')
            return jsonify({'code': 200, 'message': '删除成功'})
    else:
        # return redirect(url_for('user.user_list', msg='用户不存在'))
        return jsonify({'code': 204, 'message': '用户不存在'})


def user_list():
    content = request.args.get('content','')
    users = Users.query.filter(and_(Users.isdelete == 0, or_(Users.username.like('%'+content+'%'),Users.phone.like('%'+content+'%')))).all()
    return render_template('user/show.html', users=users, user=g.user, content=content)


def add_user():
    username = request.form.get('username')
    phone = request.form.get('phone')
    email = request.form.get('email')
    realpassword = request.form.get('password')
    password = generate_password_hash(realpassword)
    repassword = request.form.get('repassword')
    if realpassword != repassword:
        return jsonify({'code': 201, 'message': '两次密码输入不一致'})
    # 检查用户名是否已存在
    existing_user = Users.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'code': 202, 'message': '用户名已存在'})
    try:
        # 创建新用户记录
        user = Users(username=username, password=password, realpassword=realpassword, email=email, phone=phone)
        db.session.add(user)
        db.session.commit()
        add_audit_log('新增用户', f'新增用户{username}成功')
        return jsonify({'code': 200, 'message': '新增成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'code': 203, 'message': f'新增失败: {str(e)}'})


def edit_user():
    user_id = int(request.form.get('id'))
    phone = request.form.get('edit_phone')
    email = request.form.get('edit_email')
    username = request.form.get('edit_username')
    # status = request.form.get('edit_status')
    user = Users.query.get(user_id)
    if user:
        # if user.username == 'root':
        if user.username == 'root' and username != 'root':
            return jsonify({'code': 201, 'message': '不能修改root用户名称'})
        # elif user.username == 'root' and status != '0':
        #     return jsonify({'code': 204, 'message': '不能修改root用户状态'})
        if user.id == g.user.id or g.user.username == 'root':
            user.username = username
            user.phone = phone
            user.email = email
            # if status:
            #     user.isdelete = int(status)
            db.session.commit()
            add_audit_log('编辑用户', f'编辑用户{user.username}信息成功')
            return jsonify({'code': 200, 'message': '修改成功'})
        else:
            return jsonify({'code': 202, 'message': '没有权限编辑用户'})
    else:
        return jsonify({'code': 203, 'message': '用户不存在'})


def reset_password():
    user_id = int(request.form.get('id'))
    new_password = request.form.get('edit_password')
    new_repassword = request.form.get('edit_repassword')
    user = Users.query.get(user_id)
    if user:
        if g.user.username == 'root':
            if new_password != new_repassword:
                return jsonify({'code': 201, 'message': '两次密码输入不一致'})
            user.password = generate_password_hash(new_password)
            user.realpassword = new_password
            db.session.commit()
            add_audit_log('重置密码', f'重置用户{user.username}密码成功')
            return jsonify({'code': 200, 'message': '修改成功'})
        else:
            return jsonify({'code': 202, 'message': '没有权限修改密码'})


def export_users():
    users = Users.query.filter_by(isdelete=0)
    headers = ['id', '用户名', '手机号', '邮箱', '状态']
    data = []
    for user in users:
        if user.isdelete == 0:
            status = '正常'
        elif user.isdelete == 1:
            status = '已删除'
        else:
            status = '未知'
        data.append([user.id, user.username, user.phone, user.email, status])
    return export_excel('用户列表', headers, data)


def import_users():
    if request.method == 'POST':
        file = request.files.get('file')
        print(f'文件名称{file.filename}')

        if not file or file.filename == '':
            return jsonify({'code': 201, 'message': '请选择文件'})

        if not allowed_file(file.filename):
            return jsonify({'code': 202, 'message': '文件类型不支持'})

        # 调用公共方法处理文件
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'user')
        file_path = save_uploaded_file(file, path)

        try:

            data = read_excel(file_path)  # 解析 Excel
            for _, row in data.iterrows():
                username = row['用户名']
                phone = row['手机号']
                email = row['邮箱']
                realpassword = str(row['密码'])
                password = generate_password_hash(realpassword)
                # 判断用户名是否存在
                existing_user = Users.query.filter_by(username=username).first()
                if existing_user:
                    existing_user.phone = phone
                    existing_user.email = email
                    existing_user.password = password
                    existing_user.realpassword = realpassword
                    existing_user.isdelete = 0
                    db.session.commit()
                else:
                    # 创建新用户记录
                    user = Users(username=username, password=password, realpassword=realpassword, email=email, phone=phone, isdelete=0)
                    db.session.add(user)
                    db.session.commit()
            return jsonify({'code': 200, 'message': '导入成功'})
        except Exception as e:
            return jsonify({'code': 203, 'message': f'导入失败:{str(e)}'})



