"""
Risk controller for risk assessment and Monte Carlo simulations
"""
from flask import jsonify
from models import RiskAssessment, MonteCarloSimulation, FinancialData, RiskProfile, db
from middlewares.validation import validate_json, MonteCarloSimulationSchema
from middlewares.error_handler import handle_api_error, handle_api_success
from middlewares.logging import log_user_action
from services.risk_engine import RiskEngine
from services.monte_carlo_service import MonteCarloService

class RiskController:
    """Risk assessment and simulation controller"""
    
    @staticmethod
    def assess_risk(current_user):
        """Perform comprehensive risk assessment"""
        try:
            # Get user financial data
            financial_data = FinancialData.get_by_user_id(current_user.id)
            risk_profile = RiskProfile.get_by_user_id(current_user.id)
            
            if not financial_data:
                return handle_api_error('Financial data is required for risk assessment', 'missing_data', 400)
            
            # Calculate risk scores using Risk Engine
            risk_engine = RiskEngine(financial_data, risk_profile)
            risk_scores = risk_engine.calculate_all_risks()
            
            # Create risk assessment record
            assessment = RiskAssessment.create_assessment(
                user_id=current_user.id,
                **risk_scores
            )
            
            # Log user action
            log_user_action(current_user.id, 'risk_assessment_performed', risk_scores)
            
            return handle_api_success({
                'risk_assessment': assessment.to_dict()
            }, 'Risk assessment completed successfully')
            
        except Exception as e:
            db.session.rollback()
            return handle_api_error('Failed to perform risk assessment', 'assessment_error', 500)
    
    @staticmethod
    def get_risk_assessment(current_user):
        """Get latest risk assessment"""
        try:
            assessment = RiskAssessment.get_by_user_id(current_user.id)
            
            if not assessment:
                return handle_api_success({
                    'risk_assessment': None
                }, 'No risk assessment found')
            
            return handle_api_success({
                'risk_assessment': assessment.to_dict()
            }, 'Risk assessment retrieved successfully')
            
        except Exception as e:
            return handle_api_error('Failed to retrieve risk assessment', 'retrieve_error', 500)
    
    @staticmethod
    def get_risk_history(current_user):
        """Get risk assessment history"""
        try:
            history = RiskAssessment.get_history_by_user_id(current_user.id, limit=10)
            
            return handle_api_success({
                'risk_history': [assessment.to_dict() for assessment in history]
            }, 'Risk history retrieved successfully')
            
        except Exception as e:
            return handle_api_error('Failed to retrieve risk history', 'retrieve_error', 500)
    
    @staticmethod
    def get_asset_allocation_recommendation(current_user):
        """Get asset allocation recommendation based on risk profile"""
        try:
            # Get user data
            financial_data = FinancialData.get_by_user_id(current_user.id)
            risk_profile = RiskProfile.get_by_user_id(current_user.id)
            risk_assessment = RiskAssessment.get_by_user_id(current_user.id)
            
            if not all([financial_data, risk_profile]):
                return handle_api_error('Financial data and risk profile are required', 'missing_data', 400)
            
            # Generate recommendations using Risk Engine
            risk_engine = RiskEngine(financial_data, risk_profile, risk_assessment)
            recommendations = risk_engine.generate_asset_allocation_recommendations()
            
            # Log user action
            log_user_action(current_user.id, 'asset_allocation_recommendation_generated')
            
            return handle_api_success({
                'recommendations': recommendations
            }, 'Asset allocation recommendations generated successfully')
            
        except Exception as e:
            return handle_api_error('Failed to generate recommendations', 'recommendation_error', 500)
    
    @staticmethod
    @validate_json(MonteCarloSimulationSchema)
    def run_monte_carlo_simulation(current_user, validated_data):
        """Run Monte Carlo simulation"""
        try:
            # Create simulation record
            simulation = MonteCarloSimulation.create(
                user_id=current_user.id,
                **validated_data
            )
            
            # Run Monte Carlo simulation
            monte_carlo_service = MonteCarloService()
            results = monte_carlo_service.run_simulation(
                initial_value=float(validated_data['initial_portfolio_value']),
                expected_return=float(validated_data['expected_return']),
                volatility=float(validated_data['volatility']),
                time_horizon=validated_data['time_horizon'],
                iterations=validated_data.get('iterations', 10000)
            )
            
            # Update simulation with results
            simulation.set_results(results)
            simulation.save()
            
            # Log user action
            log_user_action(current_user.id, 'monte_carlo_simulation_run', {
                'simulation_id': simulation.id,
                'parameters': validated_data
            })
            
            return handle_api_success({
                'simulation': simulation.to_dict()
            }, 'Monte Carlo simulation completed successfully', 201)
            
        except Exception as e:
            db.session.rollback()
            return handle_api_error('Failed to run Monte Carlo simulation', 'simulation_error', 500)
    
    @staticmethod
    def get_monte_carlo_simulations(current_user):
        """Get all user Monte Carlo simulations"""
        try:
            simulations = MonteCarloSimulation.get_by_user_id(current_user.id)
            
            return handle_api_success({
                'simulations': [simulation.to_dict() for simulation in simulations]
            }, 'Monte Carlo simulations retrieved successfully')
            
        except Exception as e:
            return handle_api_error('Failed to retrieve simulations', 'retrieve_error', 500)
    
    @staticmethod
    def get_monte_carlo_simulation(current_user, simulation_id):
        """Get specific Monte Carlo simulation"""
        try:
            simulation = MonteCarloSimulation.get_by_id(simulation_id)
            
            if not simulation or simulation.user_id != current_user.id:
                return handle_api_error('Simulation not found', 'not_found', 404)
            
            return handle_api_success({
                'simulation': simulation.to_dict()
            }, 'Monte Carlo simulation retrieved successfully')
            
        except Exception as e:
            return handle_api_error('Failed to retrieve simulation', 'retrieve_error', 500)
    
    @staticmethod
    def delete_monte_carlo_simulation(current_user, simulation_id):
        """Delete Monte Carlo simulation"""
        try:
            simulation = MonteCarloSimulation.get_by_id(simulation_id)
            
            if not simulation or simulation.user_id != current_user.id:
                return handle_api_error('Simulation not found', 'not_found', 404)
            
            simulation.delete()
            
            # Log user action
            log_user_action(current_user.id, 'monte_carlo_simulation_deleted', {
                'simulation_id': simulation_id
            })
            
            return handle_api_success(message='Monte Carlo simulation deleted successfully')
            
        except Exception as e:
            db.session.rollback()
            return handle_api_error('Failed to delete simulation', 'delete_error', 500)
    
    @staticmethod
    def get_risk_dashboard(current_user):
        """Get comprehensive risk dashboard data"""
        try:
            # Get all risk-related data
            risk_assessment = RiskAssessment.get_by_user_id(current_user.id)
            latest_simulation = MonteCarloSimulation.get_latest_by_user_id(current_user.id)
            financial_data = FinancialData.get_by_user_id(current_user.id)
            risk_profile = RiskProfile.get_by_user_id(current_user.id)
            
            # Generate recommendations if we have the required data
            recommendations = None
            if financial_data and risk_profile:
                risk_engine = RiskEngine(financial_data, risk_profile, risk_assessment)
                recommendations = risk_engine.generate_asset_allocation_recommendations()
            
            dashboard_data = {
                'risk_assessment': risk_assessment.to_dict() if risk_assessment else None,
                'latest_simulation': latest_simulation.to_dict() if latest_simulation else None,
                'recommendations': recommendations,
                'risk_profile': risk_profile.to_dict() if risk_profile else None,
                'financial_summary': financial_data.to_dict() if financial_data else None
            }
            
            return handle_api_success({
                'dashboard': dashboard_data
            }, 'Risk dashboard data retrieved successfully')
            
        except Exception as e:
            return handle_api_error('Failed to retrieve dashboard data', 'dashboard_error', 500)

