"""
@author: zhao
@file: case.py
@time:2023/7/25  6:50 PM
"""
from flask import render_template,request,jsonify,json,g

from app.audit_log.audit_log import add_audit_log
from app.models import *
from sqlalchemy import or_
import json
import logging
from app.common import *


def show():
    content = request.args.get('content','')
    page = int(request.args.get('page', 1))
    interfaces = Interface.query.filter(Interface.interfaceURL.like('%'+content+'%'))
    id_list = []
    for interface in interfaces:
        id_list.append(interface.id)
    cases = Case.query.filter(or_(Case.caseDescription.like('%'+content+'%'),Case.interfaceID.in_(id_list))).order_by(Case.id).paginate(page=page, per_page=10)
    return render_template('case/show.html', cases=cases,content=content,user = g.user)

def add_case():
    try:
        caseDescription = request.form.get('caseDescription')
        interfaceID = int(request.form.get('interfaceID').replace(" ", ""))
        request_parameterization_key = request.form.getlist('request_parameterization')
        request_content = request.form.get('request')
        response_content = request.form.get('response')
        code = request.form.get('code')
        if code.isdigit():
            code = int(code)
        elif code == '':
            code = None
        response_parameterization_keys = request.form.getlist('response_parameterization_key')
        response_parameterization_values = request.form.getlist('response_parameterization_value')
        module = request.form.get('module')
        # 将请求参数化中的变量去除空格,变量格式为字符串
        # request_parameterizations = [item for item in request_parameterizations if item.strip() != '']
        # request_parameterizations = ','.join(request_parameterizations)
        # 生成请求参数化列表
        request_parameterization_list = dict.fromkeys(request_parameterization_key, '') 
        # 校验传参内容是否为json格式
        # 校验预期返回内容是否为json格式
        # 生成返回参数化列表
        response_parameterization_dict = dict(zip(response_parameterization_keys,response_parameterization_values))
        case = Case()
        case.caseDescription = caseDescription
        case.request = request_content
        case.response = response_content
        case.module = module
        case.interfaceID = interfaceID
        case.request_parameterization_dict = json.dumps(request_parameterization_list)
        case.response_parameterization_dict = json.dumps(response_parameterization_dict)
        case.code = code
        case.creator = g.user.username
        case.mender = g.user.username
        db.session.add(case)
        db.session.commit()
        # 增加审计日志
        add_audit_log('添加case', f'用例描述:{caseDescription};用例id:{case.id};使用接口id:{interfaceID}')
        return jsonify({"data":1,"message":"success"})
    except Exception as e:
        return jsonify({"data":1,"message":repr(e)})



def edit_case():
    try:
        id = request.args.get('id')
        caseDescription = request.form.get('edit_caseDescription')
        interfaceID = request.form.get('edit_interfaceID')
        # if interfaceID!='None':
        #     interfaceID = int(request.form.get('interfaceID').replace(" ", ""))
        request_parameterization_key = request.form.getlist('edit_request_parameterization')
        logging.error(request_parameterization_key)
        request_content = request.form.get('edit_request')
        response_content = request.form.get('edit_response')
        code = request.form.get('edit_code')
        if code.isdigit():
            code = int(code)
        elif code == '':
            code = None
        response_parameterization_keys = request.form.getlist('edit_response_parameterization_key')
        response_parameterization_values = request.form.getlist('edit_response_parameterization_value')
        module = request.form.get('edit_module')
        # 将请求参数化中的变量去除空格
        # request_parameterizations = [item for item in request_parameterizations if item.strip() != '']
        # request_parameterizations = ','.join(request_parameterizations)
        # 生成请求参数化列表
        request_parameterization_list = dict.fromkeys(request_parameterization_key, '') 
        # 校验传参内容是否为json格式
        # 校验预期返回内容是否为json格式
        # 生成返回参数化列表
        response_parameterization_dict = dict(zip(response_parameterization_keys,response_parameterization_values))
        case = Case.query.get(id)
        case.caseDescription = caseDescription
        case.request = request_content
        case.response = response_content
        case.module = module
        case.interfaceID = interfaceID
        case.request_parameterization_dict = json.dumps(request_parameterization_list)
        case.response_parameterization_dict = json.dumps(response_parameterization_dict)
        case.code = code
        case.mender = g.user.username
        db.session.commit()
        # 增加审计日志
        add_audit_log('修改case', f'用例描述：{caseDescription};用例id:{case.id};使用接口id:{interfaceID}')
        return jsonify({"data":200,"message":"success"})
    except Exception as e:
        return jsonify({"data":200,"message":repr(e)})


def del_case():
    case_id = int(request.args.get('id'))
    case = Case.query.get(case_id)
    # 删除相关联flow中的case
    flow_id = case.flowID
    if flow_id:
        flow = Flow.query.get(flow_id)
        flow_cases = flow.case_list
        flow_case_list = flow_cases.split(',')
        flow_case_list.remove(str(case.id))
        flow.case_list = ','.join(flow_case_list)
        db.session.commit()
        add_audit_log(f'删除case', f'删除flow{flow_id}-{flow.flowName}中的case{case_id}-{case.caseDescription})')
    # 删除对应case
    db.session.delete(case)
    db.session.commit()
    # 增加审计日志
    add_audit_log('删除case',  f'删除case:{case_id}-{case.caseDescription}')
    return jsonify({"data":1,"message":"success"})


def export_cases():
    '''导出用例'''
    case_list = Case.query.all()
    headers = ['id', '用例描述','接口id', '接口URL', '请求方式','请求参数','预期结果','请求参数化','返回参数化', '所属模块']
    data = []
    for case in case_list:
        data.append([case.id, case.caseDescription, case.interfaceID,case.interface.interfaceURL, case.interface.request_method,
                     case.request,case.response,case.request_parameterization_dict,case.response_parameterization_dict,case.module ])
    print('----------------data----------------')
    print(data)
    return export_excel('用例列表', headers, data)


def test_case():
    '''未完成'''
    '''测试用例'''
    requests = request.form.get('requests')
    interface_id = requests.form.get('interface_id')
    return jsonify({"data":1,"message":"success"})