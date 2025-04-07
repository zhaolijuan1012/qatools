"""
@author: zhao
@file: flow.py
@time:2023/7/25  6:56 PM
"""

from flask import render_template, request,jsonify,current_app,g
from flask_sqlalchemy.pagination import Pagination

from app.audit_log.audit_log import add_audit_log
from app.models import *
from sqlalchemy import or_,and_
import time
import requests,json,logging
from jsonpath import jsonpath 
from logging.handlers import RotatingFileHandler
import os
from jinja2 import  FileSystemLoader


def show():
    content = request.args.get('content','')
    page = int(request.args.get('page', 1))
    # flows = Flow.query.order_by(Flow.id).paginate(page=page, per_page=10)
    flows = Flow.query.filter(or_(Flow.flowDescription.like('%'+content+'%'),Flow.id==content)).order_by(Flow.id).paginate(page=page, per_page=10)
    return render_template('flow/show.html', flows=flows,content=content,user = g.user)


def detail(flowID):
    flow = Flow.query.get(flowID)
    page = int(request.args.get('page', 1))
    cases = []
    if flow.case_list == '':
        cases = []
    else:
        case_list = flow.case_list.split(',')
        for case_id in case_list:
            case = Case.query.get(int(case_id))
            if case:
                cases.append(case)
        # conditions = [Case.id == int(num) for num in case_list]
        # # 执行查询
        # cases = Case.query.filter(or_(*conditions)).all()

        # cases = Case.query.filter(Case.id.in_(list(case_list))).paginate(page=page, per_page=10)
    #     # 实现分页逻辑
    #     per_page = 10
    #     start = (page - 1) * per_page
    #     end = start + per_page
    #     paginated_cases = cases[start:end]
    #
    #     # 手动创建 Pagination 对象
    #     pagination = Pagination(
    #         query=None,
    #         page=page,
    #         per_page=per_page,
    #         total=len(cases),
    #         items=paginated_cases
    #     )
    # return render_template('flow/detail.html', flow=flow, cases=pagination,user=g.user)
    return render_template('flow/detail.html', flow=flow, cases=cases, user=g.user)



def add_flow():
    try:
        flowDescription = request.form.get('flowDescription')
        module = request.form.get('module')
        flow = Flow()
        flow.flowDescription = flowDescription
        flow.module = module
        flow.creator = g.user.username  # 未添加登录模块，暂时设置为admin
        flow.mender = g.user.username
        db.session.add(flow)
        db.session.commit()
        # 增加审计日志
        add_audit_log('增加用例集',flowDescription+'-'+module)
        return jsonify({"code":200,"message":"添加用例集成功"})
    except Exception as e:
        return jsonify({"code":201,"message":repr(e)})

def del_flow():
    # try:
    id = int(request.args.get('id'))
    flow = Flow.query.get(id)
    print(f'-------------------{flow}-----')
    flowDescription = flow.flowDescription
    print(f'-------------------------{flowDescription}')
    module = flow.module
    # 删除flow对应case的flowID
    case_list = flow.case_list
    if case_list!='':
        for case_id in case_list.split(','):
            case = Case.query.get(int(case_id))
            if case:
                try:
                    case.flowID = ''
                    db.session.commit()
                except Exception as e:
                    return jsonify({"code":201,"message":repr(e)})
    # 删除对应flow
    db.session.delete(flow)
    db.session.commit()
    # 增加审计日志
    add_audit_log('删除用例集',f'被删除的用例集为:{id}-{flowDescription}-{module};')
    return jsonify({"code" : 200 , "message" : "删除用例集成功"})
    # except Exception  as e:
    #     return jsonify({"data" : 1 , "message" : repr(e)})
    

def edit_flow():
    try:
        id = int(request.args.get('id'))
        flowDescription = request.form.get('edit_flowDescription')
        module = request.form.get('edit_module')
        flow = Flow.query.get(id)
        flow.flowDescription = flowDescription
        flow.module = module
        db.session.commit()
        # 增加审计日志
        add_audit_log('修改用例集','被修改的flowID为:'+str(id)+' 修改后的结果为:' +flowDescription+'-'+module)
        return jsonify({"data":200,"message":"修改用例集成功"})
    except Exception as e:
        return jsonify({"data":201,"message":repr(e)})


def search_case():
    '''查询case描述和caseID，用于添加flow步骤中查询'''
    content = request.args.get('str','')
    cases = Case.query.filter(or_(Case.id.like('%'+content+'%'),Case.caseDescription.like('%'+content+'%')))
    data = {}
    for case in cases:
        if case.flowID == '':
            data[case.id] = case.caseDescription
    return jsonify(code=200, data=data)



def add_step():
    try:
        flow_id = int(request.args.get('flow_id'))
        caseID = request.form.get('caseID')
        flow = Flow.query.get(flow_id)
        case_list = flow.case_list
        if case_list == '':
            flow.case_list = caseID
        else:
            flow.case_list += ','+caseID
        db.session.commit()
        return jsonify({"code":200,"message":"添加步骤成功"})
    except Exception as e:
        return jsonify({"code":201,"message":repr(e)})
    
def del_step():
    try:
        flow_id = int(request.args.get('flow_id'))
        case_id = request.args.get('case_id')
        flow = Flow.query.get(flow_id)
        case_list = flow.case_list.split(',')
        case_list.remove(case_id)
        flow.case_list = ','.join(case_list)
        db.session.commit()
        return jsonify({"data":200,"message":"删除步骤成功"})
    except Exception as e:
        return jsonify({"data":201,"message":repr(e)})
    

def add_report(type,content,module):
    # 生成新的一条测试报告
    report = Report()
    report.type = type
    report.content = content
    report.operator = g.user.username
    report.module = module
    db.session.add(report)
    db.session.commit()
    return report
    
def debug_logger(log_name):
    '''用于调试的日志显示'''
    debug_log = logging.getLogger('flows_execute')
    debug_log.setLevel(logging.INFO)
    file_handler = RotatingFileHandler(log_name)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(filename)s:%(lineno)d]'
    ))
    # # Set up SQLAlchemy logging
    # sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
    # sqlalchemy_logger.setLevel(logging.INFO)
    # sqlalchemy_logger.addHandler(file_handler)  # Add the same file handler to SQLAlchemy logger
    debug_log.addHandler(file_handler)
    return debug_log

def log_info(debug_log, message):
    debug_log.info(message)
    current_app.logger.info(message)
    
def flows_execute():
    ''' 执行全部用例集'''
    current_app.logger.info('执行全部用例集')
    operation_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())     # 格式化成2016-03-20 11:45:39形式
    # 生成新的一条测试报告
    report = add_report('执行用例集','执行全部用例集','全部模块')
    file_path = os.getcwd()
    log_file_path = os.path.join(file_path,'log',str(report.id)+'.log')
    print('============================================================>',log_file_path)
    debug_log = debug_logger(log_file_path)
    # 获取所有flow
    flows = Flow.query.all()
    log_info(debug_log,'<-------------------执行全部用例集开始------------------->')
    test_situation = []
    fail_flows = {}
    if flows:
        for flow in flows:
            test_result = 1 # 测试结果 1:成功 0:失败 
            log_info(debug_log,'<-------------------执行flow{}-{}------------------->'.format(flow.id,flow.flowDescription))
            # 获取case列表
            case_list = flow.case_list
            log_info(debug_log,'获取case列表:{}'.format(case_list))
            if case_list != '':
                case_list = case_list.split(',')
                for case_id in case_list:
                    case = Case.query.get(int(case_id))
                    log_info(debug_log,'<-------------------执行case{}-{}------------------->'.format(case_id,case.caseDescription))
                    interface = Interface.query.get(case.interfaceID)
                    url = interface.interfaceURL
                    method = interface.request_method
                    params = case.request
                    if params :
                        params = json.loads(params)
                        log_info(debug_log,
                                 '<-------------------获取params的值:{}------------------->'.format(params))
                        # 获取请求参数化的值
                        log_info(debug_log,'<-------------------获取case:{}参数化的值------------------->'.format(case_id))
                        request_parameterization_dict = json.loads(case.request_parameterization_dict)
                        if request_parameterization_dict != {"":""}:
                            for request_parameterization_key in request_parameterization_dict.keys():
                                    try:
                                        value = current_app.redis.get(str(flow.id)+'_'+request_parameterization_key).decode('utf-8')
                                        request_parameterization_dict[request_parameterization_key] = value
                                    except:
                                        log_info(debug_log,'case:{} 从redis中获取参数{}失败'.format(case_id,request_parameterization_key))
                            log_info(debug_log,'获取case:{}参数化字典为:{}'.format(case_id,request_parameterization_dict))
                            # 替换参数化的值
                            try:
                                for param_key,param_value in params.items():
                                    if '$' in param_value:
                                        param_value = param_value.split('.')[1]
                                        params[param_key] = request_parameterization_dict[param_value]
                                log_info(debug_log,'获取case:{}请求参数为:{}'.format(case_id,params))
                            except:
                                log_info(debug_log,'获取case:{}请求参数失败'.format(case_id))

                    # 发送请求
                    default_env = Environment.query.filter_by(is_default=True).first()
                    url = default_env.host +':' + default_env.port+ url
                    log_info(debug_log, '获取case:{}URL为:{}'.format(case_id, url))
                    log_info(debug_log, '获取case :{}请求方式为:{}'.format(case_id, method))
                    try:
                        if method == 'GET':
                            response = requests.get(url=url,params=params)
                        elif method == 'POST':
                            response = requests.post(url=url,params=params)
                        response.raise_for_status()  # 如果响应状态码不是200，会抛出异常
                        print('请求结果:',response.text)
                        result = json.loads(response.text)
                    except requests.exceptions.RequestException as e:
                        log_info(debug_log, f"请求失败: {e}")
                        return jsonify({"code": 500, "message": "请求失败", "error": str(e)})
                    log_info(debug_log,'<-------------------开始case:{}断言验证------------------->'.format(case_id))
                    # 断言code正确
                    if case.code !='':
                        try:
                            assert case.code == response.status_code
                            log_info(debug_log,f"断言 code情况:{case.code == response.status_code} ")
                        except AssertionError as e:
                            test_result = 0
                            log_info(debug_log,"断言 code 失败，预期结果为{}，实际为{}".format(case.code,response.status_code))
                    # 断言预期结果和实际结果一致
                    try:
                        assert json.loads(case.response) == result
                        log_info(debug_log,f"断言response结果:{json.loads(case.response) == result} ")
                    except AssertionError as e:
                        test_result = 0
                        log_info(debug_log,'断言response失败:获取case:{}预期结果为{}实际结果为{}'.format(case_id,case.response,result))
                    # 将返回参数化的值存到redis
                    log_info(debug_log,'<-------------------将case:{}返回参数化的值存到redis------------------->'.format(case_id))
                    response_parameterization_dict = json.loads(case.response_parameterization_dict)
                    log_info(debug_log,'返回参数化字典:{}'.format(response_parameterization_dict))
                    if response_parameterization_dict != {"":""}:
                        for response_parameterization_key,response_parameterization_value in response_parameterization_dict.items():
                            try:
                                # 根据xpath获取对应的结果
                                log_info(debug_log,'参数{} 根据xpath获取对应的结果为:{}'.format(response_parameterization_key,jsonpath(result,response_parameterization_value)[0]))
                                str1 = jsonpath(result,response_parameterization_value)[0]
                                if not isinstance(str1, dict):
                                    current_app.redis.set(str(flow.id)+'_'+response_parameterization_key, str1)
                                    log_info(debug_log,'存储到redis，key:{},value:{}'.format(str(flow.id)+'_'+response_parameterization_key, str1))
                            except:
                                log_info(debug_log,'参数{} 根据xpath获取结果失败'.format(response_parameterization_key))
                    # 生成失败case详情信息
                    if test_result == 0:
                        fail_case = {}
                        fail_case['case_ID'] = case_id
                        fail_case['case_description'] = case.caseDescription
                        fail_case['case_URL'] = url
                        fail_case['case_method'] = method
                        fail_case['case_request'] = params
                        fail_case['case_code_expect'] = case.code
                        fail_case['case_code_result'] = response.status_code
                        fail_case['case_response_expect'] = case.response
                        fail_case['case_response_result'] = result
                        key = str(flow.id) +'_'+ flow.module +'_'+ flow.flowDescription
                        if key in fail_flows.keys():
                            value = fail_flows[key]
                            value.append(fail_case)
                            fail_flows[key] = value
                        else:
                            fail_flows[key] = [fail_case]
            test_situation.append(test_result)
    # 生成测试报告
    flow_len = len(flows) 
    operator = g.user.username
    success = test_situation.count(1)
    fail = test_situation.count(0)
    type = '全部用例集'
    log_info(debug_log,'<-------------------测试结果:操作时间{} 操作人{} 操作类型{} flow合计{} 成功数量{} 失败数量{} ------------------->'.format(operation_time,operator,type,flow_len,success,fail))
    log_info(debug_log,'<-------------------失败情况{}------------------->'.format(fail_flows))
    # 渲染模板
    html = render_template('report/report.html',operation_time=operation_time,operator = operator,type=type,flow_len=flow_len,success=success,fail=fail,fail_flows=fail_flows)

    report_file_path = os.path.join(file_path,'reports',str(report.id)+'.html')
    # 将渲染的模板写入文件
    with open(report_file_path, 'w') as f:
        f.write(html)
    report.URL = report_file_path
    # 将日志文件存储到report中
    report.log = log_file_path
    report.count = flow_len
    report.success = success
    report.fail = fail
    db.session.commit()
    return jsonify({"code":200,"message":"执行全部用例集成功"})
