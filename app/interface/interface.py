"""
@author: zhao
@file: interface.py
@time:2023/7/25  6:26 PM
"""
import json

from flask import render_template, request, redirect, url_for, jsonify, g,current_app
from sqlalchemy import or_,and_

from app.audit_log.audit_log import add_audit_log
from app.models import *
from ext import db
from datetime import datetime
from app.common import *


def show():
    content = request.args.get('content', '')
    page = int(request.args.get('page', 1))
    interfaces = Interface.query.filter(or_(Interface.interfaceDescription.like('%' + content + '%'),
                                            Interface.interfaceURL.like('%' + content + '%'))).order_by(
        Interface.id).paginate(page=page, per_page=10)
    return render_template('interface/show.html', interfaces=interfaces, content=content, user=g.user)


def add_interface():
    # 1.找到模型类并创建对象
    interface = Interface()
    # 2.给对象的属性赋值
    interface.interfaceDescription = request.form.get('interfaceDescription')
    interface.interfaceURL = request.form.get('interfaceURL')
    interface.request_method = request.form.get('request_method')
    interface.module = request.form.get('module')
    interface.creator = g.user.username
    interface.mender = g.user.username
    # 3.将对象添加到seesion中，类似缓存
    db.session.add(interface)
    # 4.提交数据
    db.session.commit()
    # 增加审计日志
    add_audit_log('添加接口', request.form.get('interfaceDescription') + '-' + request.form.get(
        'interfaceURL') + '-' + request.form.get('request_method') + '-' + request.form.get('module'))
    return jsonify(code=200, message='添加接口成功')


def edit_interface():
    id = request.args.get('id')
    interface = Interface.query.get(id)
    interface.interfaceDescription = request.form.get('edit_interfaceDescription')
    interface.interfaceURL = request.form.get('edit_interfaceURL')
    interface.request_method = request.form.get('edit_request_method')
    interface.module = request.form.get('edit_module')
    interface.mender = g.user.username
    interface.edit_time = datetime.now()
    # 提交数据
    db.session.commit()
    # 增加审计日志
    add_audit_log('修改接口', '修改的接口id:' + id + ' ' + '修改后的结果:' + request.form.get(
        'edit_interfaceDescription') + '-' + request.form.get('edit_interfaceURL') + '-' + request.form.get(
        'edit_request_method') + '-' + request.form.get('edit_module'))
    return redirect(url_for('interface.show'))


def del_interface():
    '''删除接口'''
    # 获取接口id
    interface_id = int(request.args.get('id'))
    # 获取需删除case
    case_list = Case.query.filter(Case.interfaceID == interface_id).all()
    if case_list:
        for case in case_list:
            # 1.删除flow中该接口的数据
            if case.flowID != '':
                flow = Flow.query.get(int(case.flowID))
                flow_cases = flow.case_list
                flow_case_list = flow_cases.split(',')
                flow_case_list = [item for item in flow_case_list if item != str(case.id)]
                flow.case_list = ','.join(flow_case_list)
                db.session.commit()
                add_audit_log(f'删除接口{interface_id}',
                              f'删除用例集{flow.id}-{flow.flowName}中的用例{case.id}-{case.caseDescription}')
        # 2.删除该接口创建的case
        for case in case_list:
            db.session.delete(case)
            db.session.commit()
            add_audit_log(f'删除接口{interface_id}',
                          f'删除使用该接口的用例{case.id}-{case.caseDescription}')
    # 3.删除interface表中数据
    interface_list = Interface.query.all()
    for interface in interface_list:
        if interface.id == interface_id:
            db.session.delete(interface)
            db.session.commit()
    # 增加审计日志
    add_audit_log('删除接口', f'删除的接口id:{str(interface_id)}')
    # return redirect(url_for('interface.show'))
    return jsonify(code=200, message='success')


def search_interface():
    '''查询接口url和id，用于添加case中查询'''
    content = request.args.get('str', '')
    print(f'------------------------------content:{content}')
    interfaces = Interface.query.filter(and_(Interface.interfaceURL.like('%' + content + '%'),Interface.interfaceDescription.like('%' + content + '%')))
    data = {}
    for interface in interfaces:
        data[interface.id] = interface.interfaceURL+interface.interfaceDescription
    return jsonify(code=200, data=data)


def import_interfaces():
    """ 导入接口 """
    if request.method == 'POST':
        file = request.files.get('file')
        try:
            if not file or file.filename == '':
                return jsonify({'code': 201, 'message': '请选择文件'})
            # 调用公共方法导入文件
            path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'interface')
            file_path = save_uploaded_file(file, path)
            # 判断是否是合格的openapi3.0文档L
            with open(file_path, 'r', encoding='utf-8') as f:
                spec = json.load(f)
            if 'openapi' not in spec or not spec.get('paths'):
                return jsonify({'code': 204, 'message': '不是合法的 OpenAPI 3.0 文档'})
            paths = spec.get('paths', {})
            print(f'--------------------paths:{paths}')
            for path, methods in paths.items():
                for method, details in methods.items():
                    summary = details.get('summary', '')
                    exits_interface = Interface.query.filter_by(interfaceURL=path, request_method=method.upper()).first()
                    if not exits_interface:
                        new_interface = Interface(
                            interfaceURL=path,
                            request_method=method.upper(),
                            interfaceDescription=summary,
                            creator=g.user.username,
                            mender=g.user.username,
                            module='未分类'
                        )
                        db.session.add(new_interface)
            db.session.commit()
            return jsonify({'code': 200, 'message': '导入成功'})
        except Exception as e:
            return jsonify({'code': 203, 'message': f'导入失败:{str(e)}'})

def export_interface():
    '''导出接口'''
    interface_list = Interface.query.all()
    headers = ['id', '接口描述', '接口URL', '请求方式', '所属模块']
    data = []
    for interface in interface_list:
        data.append([interface.id, interface.interfaceDescription, interface.interfaceURL, interface.request_method,
                     interface.module])
    print('----------------data----------------')
    print(data)
    return export_excel('接口列表', headers, data)
