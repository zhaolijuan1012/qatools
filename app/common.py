"""
@author: zhao
@file: common.py
@time:2025/3/27  8:29 PM
"""
from flask import render_template, g, Response
from app.models import *
from openpyxl import Workbook
import io, os
from urllib.parse import quote
from werkzeug.utils import secure_filename
import pandas as pd


def overview():
    '''概览'''
    interfaces = Interface.query.all()
    interface_len = len(interfaces)
    cases = Case.query.all()
    case_len = len(cases)
    flows = Flow.query.all()
    flow_len = len(flows)
    users = Users.query.filter_by(isdelete=0).all()
    user_len = len(users)
    # 接口覆盖率计算
    covered_interface_ids = set()
    # 遍历所有的用例集
    for flow in flows:
        cover_cases = set(flow.case_list.split(','))
        for cover_case in cover_cases:
            case = Case.query.filter_by(id=int(cover_case)).first()
            print('---------------------case',case)
            interface = case.interfaceID
            covered_interface_ids.add(interface)
    # 计算已覆盖的接口数量
    cover_interface = len(covered_interface_ids)
    interface_coverage = (cover_interface / interface_len) * 100 if interface_len > 0 else 0
    # 四舍五入保留两位小数
    interface_coverage = round(interface_coverage, 2)
    return render_template('overview.html', interface_len=interface_len, case_len=case_len, flow_len=flow_len,
                           user=g.user,user_len=user_len, interface_coverage=interface_coverage)


def export_excel(title, headers, data):
    wb = Workbook()
    ws = wb.active
    ws.title = title

    # 写入标题
    ws.append(headers)
    # 写入数据
    for row in data:
        ws.append(row)
    # 保存到内存
    output = io.BytesIO()
    wb.save(output)
    # 对文件名进行编码
    encoded_title = quote(title + '.xlsx')
    # 返回文件
    response = Response(output.getvalue(), mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response.headers["Content-Disposition"] = f"attachment; filename*=UTF-8''{encoded_title}"
    return response


def allowed_file(filename, allowed_extensions={'xlsx', 'xls', 'csv'}):
    """检查文件是否为允许的格式"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def save_uploaded_file(file, upload_folder):
    """保存上传的文件"""
    filename = file.filename
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    return file_path


def read_excel(file_path):
    """读取 Excel 文件并返回 DataFrame"""
    try:
        data = pd.read_excel(file_path, engine='openpyxl')  # 指定解析引擎
        return data
    except Exception as e:
        raise ValueError(f'Excel 解析失败: {str(e)}')
