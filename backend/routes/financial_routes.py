"""
Financial data routes
"""
from flask import Blueprint
from controllers.financial_controller import FinancialController
from utils.auth import auth_required

# Create blueprint
financial_bp = Blueprint('financial', __name__, url_prefix='/api/financial')

# Financial data routes
@financial_bp.route('/data', methods=['GET'])
@auth_required
def get_financial_data(current_user):
    """Get financial data endpoint"""
    return FinancialController.get_financial_data(current_user)

@financial_bp.route('/data', methods=['POST', 'PUT'])
@auth_required
def update_financial_data(current_user):
    """Update financial data endpoint"""
    return FinancialController.update_financial_data(current_user)

# Risk profile routes
@financial_bp.route('/risk-profile', methods=['GET'])
@auth_required
def get_risk_profile(current_user):
    """Get risk profile endpoint"""
    return FinancialController.get_risk_profile(current_user)

@financial_bp.route('/risk-profile', methods=['POST', 'PUT'])
@auth_required
def update_risk_profile(current_user):
    """Update risk profile endpoint"""
    return FinancialController.update_risk_profile(current_user)

# Asset allocation routes
@financial_bp.route('/asset-allocations', methods=['GET'])
@auth_required
def get_asset_allocations(current_user):
    """Get asset allocations endpoint"""
    return FinancialController.get_asset_allocations(current_user)

@financial_bp.route('/asset-allocations', methods=['POST', 'PUT'])
@auth_required
def update_asset_allocation(current_user):
    """Update asset allocation endpoint"""
    return FinancialController.update_asset_allocation(current_user)

# Financial goals routes
@financial_bp.route('/goals', methods=['GET'])
@auth_required
def get_financial_goals(current_user):
    """Get financial goals endpoint"""
    return FinancialController.get_financial_goals(current_user)

@financial_bp.route('/goals', methods=['POST'])
@auth_required
def create_financial_goal(current_user):
    """Create financial goal endpoint"""
    return FinancialController.create_financial_goal(current_user)

@financial_bp.route('/goals/<int:goal_id>', methods=['PUT'])
@auth_required
def update_financial_goal(current_user, goal_id):
    """Update financial goal endpoint"""
    return FinancialController.update_financial_goal(current_user, goal_id)

@financial_bp.route('/goals/<int:goal_id>', methods=['DELETE'])
@auth_required
def delete_financial_goal(current_user, goal_id):
    """Delete financial goal endpoint"""
    return FinancialController.delete_financial_goal(current_user, goal_id)

# Summary route
@financial_bp.route('/summary', methods=['GET'])
@auth_required
def get_financial_summary(current_user):
    """Get financial summary endpoint"""
    return FinancialController.get_financial_summary(current_user)

