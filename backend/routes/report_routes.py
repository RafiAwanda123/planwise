"""
Report generation and management routes
"""
from flask import Blueprint, request
from controllers.report_controller import ReportController
from utils.auth import auth_required

# Create blueprint
report_bp = Blueprint('reports', __name__, url_prefix='/api/reports')

# Report generation routes
@report_bp.route('/dashboard', methods=['POST'])
@auth_required
def generate_dashboard_report(current_user):
    """Generate dashboard report endpoint"""
    return ReportController.generate_dashboard_report(current_user)

@report_bp.route('/pdf', methods=['POST'])
@auth_required
def generate_pdf_report(current_user):
    """Generate PDF report endpoint"""
    return ReportController.generate_pdf_report(current_user)

# Report management routes
@report_bp.route('/', methods=['GET'])
@auth_required
def get_reports(current_user):
    """Get all reports endpoint"""
    return ReportController.get_reports(current_user)

@report_bp.route('/<int:report_id>', methods=['GET'])
@auth_required
def get_report(current_user, report_id):
    """Get specific report endpoint"""
    return ReportController.get_report(current_user, report_id)

@report_bp.route('/<int:report_id>/download', methods=['GET'])
@auth_required
def download_report(current_user, report_id):
    """Download report file endpoint"""
    return ReportController.download_report(current_user, report_id)

@report_bp.route('/<int:report_id>', methods=['DELETE'])
@auth_required
def delete_report(current_user, report_id):
    """Delete report endpoint"""
    return ReportController.delete_report(current_user, report_id)

# Analytics routes
@report_bp.route('/analytics', methods=['GET'])
@auth_required
def get_analytics_data(current_user):
    """Get analytics data endpoint"""
    return ReportController.get_analytics_data(current_user)

# Data export routes
@report_bp.route('/export', methods=['GET'])
@auth_required
def export_data(current_user):
    """Export user data endpoint"""
    export_format = request.args.get('format', 'json')
    return ReportController.export_data(current_user, export_format)

