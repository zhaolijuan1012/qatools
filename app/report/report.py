from flask import render_template,request,send_file,jsonify,g
from app.models import *
import smtplib
from email.mime.text import MIMEText
from email.header import Header
def show():
    try:
        page = int(request.args.get('page', 1))
        reports = Report.query.order_by(-Report.id).paginate(page=page, per_page=10)
        return render_template('report/show.html',reports=reports, user=g.user)
    except Exception as e:
         return repr(e)
     
     
def log_download():
    file = request.args.get('file')
    return send_file(file, as_attachment=True)

def report_download():
    file = request.args.get('file')
    return send_file(file, as_attachment=True)

def send():
    try:
        # 第三方 SMTP 服务
        mail_host = "smtp.qq.com"  # 设置服务器
        mail_user = "1259702360@qq.com"  # 用户名
        mail_pass = "ffhsnawmyqqqgbcb"  # 口令

        sender = '1259702360@qq.com'
        receivers = '2449312564@qq.com'  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱


        # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
        message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
        message['From'] = Header(sender)  # 发送者
        message['To'] = Header(receivers)  # 收件人

        subject = '接口自动化测试报告'
        message['Subject'] = Header(subject, 'utf-8')


        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        # smtpObj.quit()
        return jsonify({"message":"success"})
    except Exception as e:
        return jsonify({"message":repr(e)})
    