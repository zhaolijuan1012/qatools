from flask import Blueprint
from app.report.report import *
report_bp = Blueprint('report', __name__, url_prefix='/report')
report_bp.add_url_rule('/show',view_func=show)
report_bp.add_url_rule('/log_download',view_func=log_download)
report_bp.add_url_rule('/report_download',view_func=report_download)
report_bp.add_url_rule('/send',view_func=send)