"""
Risk assessment and simulation routes
"""
from flask import Blueprint
from controllers.risk_controller import RiskController
from utils.auth import auth_required

# Create blueprint
risk_bp = Blueprint('risk', __name__, url_prefix='/api/risk')

# Risk assessment routes
@risk_bp.route('/assess', methods=['POST'])
@auth_required
def assess_risk(current_user):
    """Perform risk assessment endpoint"""
    return RiskController.assess_risk(current_user)

@risk_bp.route('/assessment', methods=['GET'])
@auth_required
def get_risk_assessment(current_user):
    """Get latest risk assessment endpoint"""
    return RiskController.get_risk_assessment(current_user)

@risk_bp.route('/history', methods=['GET'])
@auth_required
def get_risk_history(current_user):
    """Get risk assessment history endpoint"""
    return RiskController.get_risk_history(current_user)

# Asset allocation recommendation routes
@risk_bp.route('/recommendations/asset-allocation', methods=['GET'])
@auth_required
def get_asset_allocation_recommendation(current_user):
    """Get asset allocation recommendations endpoint"""
    return RiskController.get_asset_allocation_recommendation(current_user)

# Monte Carlo simulation routes
@risk_bp.route('/simulations', methods=['GET'])
@auth_required
def get_monte_carlo_simulations(current_user):
    """Get Monte Carlo simulations endpoint"""
    return RiskController.get_monte_carlo_simulations(current_user)

@risk_bp.route('/simulations', methods=['POST'])
@auth_required
def run_monte_carlo_simulation(current_user):
    """Run Monte Carlo simulation endpoint"""
    return RiskController.run_monte_carlo_simulation(current_user)

@risk_bp.route('/simulations/<int:simulation_id>', methods=['GET'])
@auth_required
def get_monte_carlo_simulation(current_user, simulation_id):
    """Get specific Monte Carlo simulation endpoint"""
    return RiskController.get_monte_carlo_simulation(current_user, simulation_id)

@risk_bp.route('/simulations/<int:simulation_id>', methods=['DELETE'])
@auth_required
def delete_monte_carlo_simulation(current_user, simulation_id):
    """Delete Monte Carlo simulation endpoint"""
    return RiskController.delete_monte_carlo_simulation(current_user, simulation_id)

# Dashboard route
@risk_bp.route('/dashboard', methods=['GET'])
@auth_required
def get_risk_dashboard(current_user):
    """Get risk dashboard data endpoint"""
    return RiskController.get_risk_dashboard(current_user)

