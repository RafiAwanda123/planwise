"""
Report controller for generating and managing reports
"""
import os
from flask import jsonify, send_file
from models import Report, FinancialData, RiskAssessment, MonteCarloSimulation, FinancialGoal, db
from middlewares.error_handler import handle_api_error, handle_api_success
from middlewares.logging import log_user_action
from services.report_service import ReportService

class ReportController:
    """Report generation and management controller"""
    
    @staticmethod
    def generate_dashboard_report(current_user):
        """Generate dashboard report data"""
        try:
            # Get all user data
            financial_data = FinancialData.get_by_user_id(current_user.id)
            risk_assessment = RiskAssessment.get_by_user_id(current_user.id)
            latest_simulation = MonteCarloSimulation.get_latest_by_user_id(current_user.id)
            financial_goals = FinancialGoal.get_active_goals(current_user.id)
            
            # Generate dashboard data
            report_service = ReportService()
            dashboard_data = report_service.generate_dashboard_data(
                user=current_user,
                financial_data=financial_data,
                risk_assessment=risk_assessment,
                simulation=latest_simulation,
                goals=financial_goals
            )
            
            # Save report
            report = Report.create_report(
                user_id=current_user.id,
                report_type='dashboard',
                report_data=dashboard_data
            )
            
            # Log user action
            log_user_action(current_user.id, 'dashboard_report_generated')
            
            return handle_api_success({
                'report': report.to_dict(),
                'dashboard_data': dashboard_data
            }, 'Dashboard report generated successfully')
            
        except Exception as e:
            db.session.rollback()
            return handle_api_error('Failed to generate dashboard report', 'report_error', 500)
    
    @staticmethod
    def generate_pdf_report(current_user):
        """Generate comprehensive PDF report"""
        try:
            # Get all user data
            financial_data = FinancialData.get_by_user_id(current_user.id)
            risk_assessment = RiskAssessment.get_by_user_id(current_user.id)
            simulations = MonteCarloSimulation.get_by_user_id(current_user.id)
            financial_goals = FinancialGoal.get_by_user_id(current_user.id)
            
            if not financial_data:
                return handle_api_error('Financial data is required to generate PDF report', 'missing_data', 400)
            
            # Generate PDF report
            report_service = ReportService()
            pdf_path = report_service.generate_pdf_report(
                user=current_user,
                financial_data=financial_data,
                risk_assessment=risk_assessment,
                simulations=simulations,
                goals=financial_goals
            )
            
            # Save report record
            report = Report.create_report(
                user_id=current_user.id,
                report_type='pdf',
                file_path=pdf_path
            )
            
            # Log user action
            log_user_action(current_user.id, 'pdf_report_generated')
            
            return handle_api_success({
                'report': report.to_dict(),
                'download_url': f'/api/reports/{report.id}/download'
            }, 'PDF report generated successfully')
            
        except Exception as e:
            db.session.rollback()
            return handle_api_error('Failed to generate PDF report', 'report_error', 500)
    
    @staticmethod
    def get_reports(current_user):
        """Get all user reports"""
        try:
            reports = Report.get_by_user_id(current_user.id)
            
            return handle_api_success({
                'reports': [report.to_dict() for report in reports]
            }, 'Reports retrieved successfully')
            
        except Exception as e:
            return handle_api_error('Failed to retrieve reports', 'retrieve_error', 500)
    
    @staticmethod
    def get_report(current_user, report_id):
        """Get specific report"""
        try:
            report = Report.get_by_id(report_id)
            
            if not report or report.user_id != current_user.id:
                return handle_api_error('Report not found', 'not_found', 404)
            
            return handle_api_success({
                'report': report.to_dict()
            }, 'Report retrieved successfully')
            
        except Exception as e:
            return handle_api_error('Failed to retrieve report', 'retrieve_error', 500)
    
    @staticmethod
    def download_report(current_user, report_id):
        """Download report file"""
        try:
            report = Report.get_by_id(report_id)
            
            if not report or report.user_id != current_user.id:
                return handle_api_error('Report not found', 'not_found', 404)
            
            if not report.file_path or not os.path.exists(report.file_path):
                return handle_api_error('Report file not found', 'file_not_found', 404)
            
            # Log user action
            log_user_action(current_user.id, 'report_downloaded', {'report_id': report_id})
            
            return send_file(
                report.file_path,
                as_attachment=True,
                download_name=f'financial_report_{report.id}.pdf'
            )
            
        except Exception as e:
            return handle_api_error('Failed to download report', 'download_error', 500)
    
    @staticmethod
    def delete_report(current_user, report_id):
        """Delete report"""
        try:
            report = Report.get_by_id(report_id)
            
            if not report or report.user_id != current_user.id:
                return handle_api_error('Report not found', 'not_found', 404)
            
            # Delete file if exists
            if report.file_path and os.path.exists(report.file_path):
                os.remove(report.file_path)
            
            # Delete report record
            report.delete()
            
            # Log user action
            log_user_action(current_user.id, 'report_deleted', {'report_id': report_id})
            
            return handle_api_success(message='Report deleted successfully')
            
        except Exception as e:
            db.session.rollback()
            return handle_api_error('Failed to delete report', 'delete_error', 500)
    
    @staticmethod
    def get_analytics_data(current_user):
        """Get analytics data for charts and visualizations"""
        try:
            # Get historical data
            risk_history = RiskAssessment.get_history_by_user_id(current_user.id, limit=12)
            simulations = MonteCarloSimulation.get_by_user_id(current_user.id)
            goals = FinancialGoal.get_by_user_id(current_user.id)
            
            # Generate analytics
            report_service = ReportService()
            analytics_data = report_service.generate_analytics_data(
                risk_history=risk_history,
                simulations=simulations,
                goals=goals
            )
            
            return handle_api_success({
                'analytics': analytics_data
            }, 'Analytics data retrieved successfully')
            
        except Exception as e:
            return handle_api_error('Failed to retrieve analytics data', 'analytics_error', 500)
    
    @staticmethod
    def export_data(current_user, export_format='json'):
        """Export user data in specified format"""
        try:
            # Get all user data
            financial_data = FinancialData.get_by_user_id(current_user.id)
            risk_assessment = RiskAssessment.get_by_user_id(current_user.id)
            simulations = MonteCarloSimulation.get_by_user_id(current_user.id)
            goals = FinancialGoal.get_by_user_id(current_user.id)
            
            # Generate export
            report_service = ReportService()
            export_path = report_service.export_user_data(
                user=current_user,
                financial_data=financial_data,
                risk_assessment=risk_assessment,
                simulations=simulations,
                goals=goals,
                format=export_format
            )
            
            # Log user action
            log_user_action(current_user.id, 'data_exported', {'format': export_format})
            
            return send_file(
                export_path,
                as_attachment=True,
                download_name=f'financial_data_export.{export_format}'
            )
            
        except Exception as e:
            return handle_api_error('Failed to export data', 'export_error', 500)

