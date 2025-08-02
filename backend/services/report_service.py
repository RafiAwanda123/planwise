"""
Report Service for generating comprehensive financial reports and analytics
"""
import os
import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64

class ReportService:
    """
    Comprehensive report generation service
    Generates dashboard data, PDF reports, and analytics
    """
    
    def __init__(self):
        """Initialize report service"""
        self.report_dir = '/tmp/reports'
        os.makedirs(self.report_dir, exist_ok=True)
        
        # Set up matplotlib for report generation
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def generate_dashboard_data(self,
                              user,
                              financial_data=None,
                              risk_assessment=None,
                              simulation=None,
                              goals=None) -> Dict:
        """
        Generate comprehensive dashboard data
        
        Args:
            user: User model instance
            financial_data: FinancialData model instance
            risk_assessment: RiskAssessment model instance
            simulation: MonteCarloSimulation model instance
            goals: List of FinancialGoal instances
            
        Returns:
            Dict: Dashboard data
        """
        dashboard = {
            'user_info': {
                'name': user.full_name,
                'email': user.email,
                'last_updated': datetime.utcnow().isoformat()
            },
            'financial_summary': self._generate_financial_summary(financial_data),
            'risk_overview': self._generate_risk_overview(risk_assessment),
            'portfolio_projection': self._generate_portfolio_projection(simulation),
            'goals_progress': self._generate_goals_progress(goals),
            'key_metrics': self._generate_key_metrics(financial_data, risk_assessment),
            'recommendations': self._generate_recommendations(financial_data, risk_assessment, goals)
        }
        
        return dashboard
    
    def _generate_financial_summary(self, financial_data) -> Dict:
        """Generate financial summary section"""
        if not financial_data:
            return {'status': 'no_data'}
        
        return {
            'monthly_income': float(financial_data.monthly_income),
            'monthly_expenses': float(financial_data.monthly_expenses),
            'monthly_surplus': float(financial_data.monthly_surplus),
            'total_assets': float(financial_data.total_assets),
            'total_debt': float(financial_data.total_debt),
            'net_worth': float(financial_data.net_worth),
            'emergency_fund': float(financial_data.emergency_fund),
            'emergency_fund_months': financial_data.emergency_fund_months,
            'debt_to_income_ratio': financial_data.debt_to_income_ratio,
            'savings_rate': financial_data.savings_rate
        }
    
    def _generate_risk_overview(self, risk_assessment) -> Dict:
        """Generate risk overview section"""
        if not risk_assessment:
            return {'status': 'no_assessment'}
        
        return {
            'total_risk_score': float(risk_assessment.total_risk_score),
            'risk_level': risk_assessment.risk_level,
            'risk_breakdown': risk_assessment.get_risk_breakdown(),
            'assessment_date': risk_assessment.assessment_date.isoformat(),
            'recommendations': risk_assessment.get_recommendations()
        }
    
    def _generate_portfolio_projection(self, simulation) -> Dict:
        """Generate portfolio projection section"""
        if not simulation:
            return {'status': 'no_simulation'}
        
        return {
            'expected_value': float(simulation.expected_value) if simulation.expected_value else None,
            'success_probability': float(simulation.success_probability) if simulation.success_probability else None,
            'var_95': float(simulation.var_95) if simulation.var_95 else None,
            'time_horizon': simulation.time_horizon,
            'initial_value': float(simulation.initial_portfolio_value),
            'expected_return': float(simulation.expected_return) * 100,  # Convert to percentage
            'volatility': float(simulation.volatility) * 100  # Convert to percentage
        }
    
    def _generate_goals_progress(self, goals) -> Dict:
        """Generate goals progress section"""
        if not goals:
            return {'status': 'no_goals'}
        
        goals_data = []
        total_target = 0
        total_current = 0
        
        for goal in goals:
            goal_data = {
                'name': goal.goal_name,
                'target_amount': float(goal.target_amount),
                'current_amount': float(goal.current_amount),
                'progress_percentage': goal.progress_percentage,
                'status': goal.status,
                'priority': goal.priority,
                'is_on_track': goal.is_on_track
            }
            
            if goal.target_date:
                goal_data['target_date'] = goal.target_date.isoformat()
                goal_data['days_remaining'] = goal.days_remaining
            
            goals_data.append(goal_data)
            total_target += float(goal.target_amount)
            total_current += float(goal.current_amount)
        
        return {
            'goals': goals_data,
            'total_target': total_target,
            'total_current': total_current,
            'overall_progress': (total_current / total_target * 100) if total_target > 0 else 0
        }
    
    def _generate_key_metrics(self, financial_data, risk_assessment) -> Dict:
        """Generate key metrics section"""
        metrics = {}
        
        if financial_data:
            metrics.update({
                'liquidity_ratio': financial_data.emergency_fund_months,
                'debt_ratio': financial_data.debt_to_income_ratio,
                'savings_rate': financial_data.savings_rate,
                'net_worth_growth': 0  # Would need historical data
            })
        
        if risk_assessment:
            metrics.update({
                'overall_risk_score': float(risk_assessment.total_risk_score),
                'risk_trend': 0  # Would need historical data
            })
        
        return metrics
    
    def _generate_recommendations(self, financial_data, risk_assessment, goals) -> List[Dict]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Emergency fund recommendations
        if financial_data and financial_data.emergency_fund_months < 3:
            recommendations.append({
                'category': 'Emergency Fund',
                'priority': 'high',
                'title': 'Build Emergency Fund',
                'description': f'Increase emergency fund to cover 3-6 months of expenses. Current coverage: {financial_data.emergency_fund_months:.1f} months.'
            })
        
        # Debt recommendations
        if financial_data and financial_data.debt_to_income_ratio > 0.4:
            recommendations.append({
                'category': 'Debt Management',
                'priority': 'high',
                'title': 'Reduce Debt Levels',
                'description': f'Current debt-to-income ratio is {financial_data.debt_to_income_ratio:.1%}. Consider debt reduction strategies.'
            })
        
        # Risk-based recommendations
        if risk_assessment:
            if float(risk_assessment.total_risk_score) > 7:
                recommendations.append({
                    'category': 'Risk Management',
                    'priority': 'medium',
                    'title': 'Address High Risk Areas',
                    'description': 'Your overall risk score is high. Review specific risk areas and implement mitigation strategies.'
                })
        
        return recommendations
    
    def generate_pdf_report(self,
                           user,
                           financial_data=None,
                           risk_assessment=None,
                           simulations=None,
                           goals=None) -> str:
        """
        Generate comprehensive PDF report
        
        Args:
            user: User model instance
            financial_data: FinancialData model instance
            risk_assessment: RiskAssessment model instance
            simulations: List of MonteCarloSimulation instances
            goals: List of FinancialGoal instances
            
        Returns:
            str: Path to generated PDF file
        """
        # Create filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'financial_report_{user.id}_{timestamp}.pdf'
        filepath = os.path.join(self.report_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        story.append(Paragraph(f'Financial Risk Management Report', title_style))
        story.append(Paragraph(f'Generated for: {user.full_name}', styles['Heading2']))
        story.append(Paragraph(f'Date: {datetime.now().strftime("%B %d, %Y")}', styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Executive Summary
        story.append(Paragraph('Executive Summary', styles['Heading2']))
        summary_text = self._generate_executive_summary(financial_data, risk_assessment)
        story.append(Paragraph(summary_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Financial Overview
        if financial_data:
            story.extend(self._add_financial_overview_section(financial_data, styles))
        
        # Risk Assessment
        if risk_assessment:
            story.extend(self._add_risk_assessment_section(risk_assessment, styles))
        
        # Portfolio Projections
        if simulations:
            story.extend(self._add_portfolio_projections_section(simulations, styles))
        
        # Goals Analysis
        if goals:
            story.extend(self._add_goals_analysis_section(goals, styles))
        
        # Recommendations
        story.extend(self._add_recommendations_section(financial_data, risk_assessment, goals, styles))
        
        # Build PDF
        doc.build(story)
        
        return filepath
    
    def _generate_executive_summary(self, financial_data, risk_assessment) -> str:
        """Generate executive summary text"""
        summary_parts = []
        
        if financial_data:
            net_worth = float(financial_data.net_worth)
            if net_worth > 0:
                summary_parts.append(f"Your current net worth is ${net_worth:,.2f}.")
            else:
                summary_parts.append(f"Your current net worth is ${net_worth:,.2f}, indicating areas for improvement.")
            
            emergency_months = financial_data.emergency_fund_months
            if emergency_months >= 6:
                summary_parts.append("Your emergency fund provides excellent financial security.")
            elif emergency_months >= 3:
                summary_parts.append("Your emergency fund provides adequate financial security.")
            else:
                summary_parts.append("Your emergency fund needs strengthening for better financial security.")
        
        if risk_assessment:
            risk_level = risk_assessment.risk_level
            risk_score = float(risk_assessment.total_risk_score)
            summary_parts.append(f"Your overall risk level is {risk_level} with a risk score of {risk_score:.1f}/10.")
        
        return " ".join(summary_parts) if summary_parts else "Comprehensive financial analysis requires more data input."
    
    def _add_financial_overview_section(self, financial_data, styles) -> List:
        """Add financial overview section to PDF"""
        section = []
        
        section.append(Paragraph('Financial Overview', styles['Heading2']))
        
        # Create financial data table
        financial_table_data = [
            ['Metric', 'Amount', 'Status'],
            ['Monthly Income', f'${float(financial_data.monthly_income):,.2f}', ''],
            ['Monthly Expenses', f'${float(financial_data.monthly_expenses):,.2f}', ''],
            ['Monthly Surplus', f'${float(financial_data.monthly_surplus):,.2f}', 
             'Positive' if financial_data.monthly_surplus > 0 else 'Negative'],
            ['Total Assets', f'${float(financial_data.total_assets):,.2f}', ''],
            ['Total Debt', f'${float(financial_data.total_debt):,.2f}', ''],
            ['Net Worth', f'${float(financial_data.net_worth):,.2f}', 
             'Positive' if financial_data.net_worth > 0 else 'Negative'],
            ['Emergency Fund', f'${float(financial_data.emergency_fund):,.2f}', 
             f'{financial_data.emergency_fund_months:.1f} months coverage']
        ]
        
        financial_table = Table(financial_table_data)
        financial_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        section.append(financial_table)
        section.append(Spacer(1, 20))
        
        return section
    
    def _add_risk_assessment_section(self, risk_assessment, styles) -> List:
        """Add risk assessment section to PDF"""
        section = []
        
        section.append(Paragraph('Risk Assessment', styles['Heading2']))
        
        # Risk breakdown table
        risk_breakdown = risk_assessment.get_risk_breakdown()
        risk_table_data = [['Risk Category', 'Score', 'Weight', 'Weighted Score', 'Description']]
        
        for risk_type, details in risk_breakdown.items():
            risk_table_data.append([
                risk_type.replace('_', ' ').title(),
                f"{details['score']:.1f}",
                f"{details['weight']:.0%}",
                f"{details['weighted_score']:.2f}",
                details['description'][:50] + '...' if len(details['description']) > 50 else details['description']
            ])
        
        risk_table_data.append([
            'Total Risk Score',
            f"{float(risk_assessment.total_risk_score):.1f}",
            '100%',
            f"{float(risk_assessment.total_risk_score):.1f}",
            f"Overall risk level: {risk_assessment.risk_level.upper()}"
        ])
        
        risk_table = Table(risk_table_data, colWidths=[1.5*inch, 0.8*inch, 0.8*inch, 1*inch, 2.5*inch])
        risk_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        section.append(risk_table)
        section.append(Spacer(1, 20))
        
        return section
    
    def _add_portfolio_projections_section(self, simulations, styles) -> List:
        """Add portfolio projections section to PDF"""
        section = []
        
        section.append(Paragraph('Portfolio Projections', styles['Heading2']))
        
        if simulations:
            latest_simulation = simulations[0]  # Assuming first is latest
            
            projection_text = f"""
            Based on Monte Carlo simulation with {latest_simulation.iterations:,} iterations:
            
            • Initial Portfolio Value: ${float(latest_simulation.initial_portfolio_value):,.2f}
            • Expected Annual Return: {float(latest_simulation.expected_return)*100:.1f}%
            • Volatility: {float(latest_simulation.volatility)*100:.1f}%
            • Time Horizon: {latest_simulation.time_horizon} years
            • Expected Final Value: ${float(latest_simulation.expected_value):,.2f}
            • Success Probability: {float(latest_simulation.success_probability):.1f}%
            • Value at Risk (95%): ${float(latest_simulation.var_95):,.2f}
            """
            
            section.append(Paragraph(projection_text, styles['Normal']))
        
        section.append(Spacer(1, 20))
        return section
    
    def _add_goals_analysis_section(self, goals, styles) -> List:
        """Add goals analysis section to PDF"""
        section = []
        
        section.append(Paragraph('Financial Goals Analysis', styles['Heading2']))
        
        if goals:
            goals_table_data = [['Goal', 'Target', 'Current', 'Progress', 'Status']]
            
            for goal in goals:
                goals_table_data.append([
                    goal.goal_name,
                    f'${float(goal.target_amount):,.2f}',
                    f'${float(goal.current_amount):,.2f}',
                    f'{goal.progress_percentage:.1f}%',
                    goal.status.title()
                ])
            
            goals_table = Table(goals_table_data)
            goals_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            section.append(goals_table)
        else:
            section.append(Paragraph('No financial goals have been set.', styles['Normal']))
        
        section.append(Spacer(1, 20))
        return section
    
    def _add_recommendations_section(self, financial_data, risk_assessment, goals, styles) -> List:
        """Add recommendations section to PDF"""
        section = []
        
        section.append(Paragraph('Recommendations', styles['Heading2']))
        
        recommendations = self._generate_recommendations(financial_data, risk_assessment, goals)
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                rec_text = f"{i}. {rec['title']} ({rec['priority'].upper()} PRIORITY): {rec['description']}"
                section.append(Paragraph(rec_text, styles['Normal']))
                section.append(Spacer(1, 10))
        else:
            section.append(Paragraph('No specific recommendations at this time. Continue monitoring your financial health regularly.', styles['Normal']))
        
        return section
    
    def generate_analytics_data(self, risk_history=None, simulations=None, goals=None) -> Dict:
        """Generate analytics data for charts and visualizations"""
        analytics = {
            'risk_trends': self._analyze_risk_trends(risk_history),
            'simulation_analysis': self._analyze_simulations(simulations),
            'goals_analytics': self._analyze_goals(goals),
            'charts_data': self._generate_charts_data(risk_history, simulations, goals)
        }
        
        return analytics
    
    def _analyze_risk_trends(self, risk_history) -> Dict:
        """Analyze risk assessment trends"""
        if not risk_history:
            return {'status': 'no_data'}
        
        dates = [assessment.assessment_date for assessment in risk_history]
        scores = [float(assessment.total_risk_score) for assessment in risk_history]
        
        return {
            'dates': [date.isoformat() for date in dates],
            'scores': scores,
            'trend': 'improving' if len(scores) > 1 and scores[-1] < scores[0] else 'stable'
        }
    
    def _analyze_simulations(self, simulations) -> Dict:
        """Analyze Monte Carlo simulations"""
        if not simulations:
            return {'status': 'no_data'}
        
        return {
            'total_simulations': len(simulations),
            'average_success_probability': sum(float(sim.success_probability or 0) for sim in simulations) / len(simulations),
            'simulation_dates': [sim.created_at.isoformat() for sim in simulations]
        }
    
    def _analyze_goals(self, goals) -> Dict:
        """Analyze financial goals"""
        if not goals:
            return {'status': 'no_goals'}
        
        total_goals = len(goals)
        completed_goals = len([g for g in goals if g.status == 'completed'])
        on_track_goals = len([g for g in goals if g.is_on_track])
        
        return {
            'total_goals': total_goals,
            'completed_goals': completed_goals,
            'on_track_goals': on_track_goals,
            'completion_rate': (completed_goals / total_goals * 100) if total_goals > 0 else 0
        }
    
    def _generate_charts_data(self, risk_history, simulations, goals) -> Dict:
        """Generate data for frontend charts"""
        charts = {}
        
        # Risk trend chart data
        if risk_history:
            charts['risk_trend'] = {
                'labels': [assessment.assessment_date.strftime('%Y-%m') for assessment in risk_history],
                'data': [float(assessment.total_risk_score) for assessment in risk_history]
            }
        
        # Goals progress chart data
        if goals:
            charts['goals_progress'] = {
                'labels': [goal.goal_name for goal in goals],
                'data': [goal.progress_percentage for goal in goals]
            }
        
        return charts
    
    def export_user_data(self, user, financial_data=None, risk_assessment=None, 
                        simulations=None, goals=None, format='json') -> str:
        """Export user data in specified format"""
        
        # Compile all user data
        export_data = {
            'user_info': {
                'name': user.full_name,
                'email': user.email,
                'export_date': datetime.utcnow().isoformat()
            },
            'financial_data': financial_data.to_dict() if financial_data else None,
            'risk_assessment': risk_assessment.to_dict() if risk_assessment else None,
            'simulations': [sim.to_dict() for sim in simulations] if simulations else [],
            'goals': [goal.to_dict() for goal in goals] if goals else []
        }
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'financial_data_export_{user.id}_{timestamp}.{format}'
        filepath = os.path.join(self.report_dir, filename)
        
        if format == 'json':
            with open(filepath, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
        elif format == 'csv':
            # Convert to DataFrame and export as CSV
            df = pd.json_normalize(export_data)
            df.to_csv(filepath, index=False)
        
        return filepath

