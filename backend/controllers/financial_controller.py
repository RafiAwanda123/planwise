"""
Financial controller for managing user financial data
"""
from flask import jsonify
from models import FinancialData, RiskProfile, AssetAllocation, FinancialGoal, db
from middlewares.validation import (
    validate_json, FinancialDataSchema, RiskProfileSchema, 
    AssetAllocationSchema, FinancialGoalSchema
)
from middlewares.error_handler import handle_api_error, handle_api_success
from middlewares.logging import log_user_action

class FinancialController:
    """Financial data controller"""
    
    @staticmethod
    @validate_json(FinancialDataSchema)
    def update_financial_data(current_user, validated_data):
        """Update user financial data"""
        try:
            financial_data = FinancialData.create_or_update(
                user_id=current_user.id,
                **validated_data
            )
            
            # Log user action
            log_user_action(current_user.id, 'financial_data_updated', validated_data)
            
            return handle_api_success({
                'financial_data': financial_data.to_dict()
            }, 'Financial data updated successfully')
            
        except Exception as e:
            db.session.rollback()
            return handle_api_error('Failed to update financial data', 'update_error', 500)
    
    @staticmethod
    def get_financial_data(current_user):
        """Get user financial data"""
        try:
            financial_data = FinancialData.get_by_user_id(current_user.id)
            
            if not financial_data:
                return handle_api_success({
                    'financial_data': None
                }, 'No financial data found')
            
            return handle_api_success({
                'financial_data': financial_data.to_dict()
            }, 'Financial data retrieved successfully')
            
        except Exception as e:
            return handle_api_error('Failed to retrieve financial data', 'retrieve_error', 500)
    
    @staticmethod
    @validate_json(RiskProfileSchema)
    def update_risk_profile(current_user, validated_data):
        """Update user risk profile"""
        try:
            risk_profile = RiskProfile.create_or_update(
                user_id=current_user.id,
                **validated_data
            )
            
            # Log user action
            log_user_action(current_user.id, 'risk_profile_updated', validated_data)
            
            return handle_api_success({
                'risk_profile': risk_profile.to_dict()
            }, 'Risk profile updated successfully')
            
        except Exception as e:
            db.session.rollback()
            return handle_api_error('Failed to update risk profile', 'update_error', 500)
    
    @staticmethod
    def get_risk_profile(current_user):
        """Get user risk profile"""
        try:
            risk_profile = RiskProfile.get_by_user_id(current_user.id)
            
            if not risk_profile:
                return handle_api_success({
                    'risk_profile': None
                }, 'No risk profile found')
            
            return handle_api_success({
                'risk_profile': risk_profile.to_dict()
            }, 'Risk profile retrieved successfully')
            
        except Exception as e:
            return handle_api_error('Failed to retrieve risk profile', 'retrieve_error', 500)
    
    @staticmethod
    @validate_json(AssetAllocationSchema)
    def update_asset_allocation(current_user, validated_data):
        """Update asset allocation"""
        try:
            asset_allocation = AssetAllocation.create_or_update(
                user_id=current_user.id,
                asset_type=validated_data['asset_type'],
                **{k: v for k, v in validated_data.items() if k != 'asset_type'}
            )
            
            # Log user action
            log_user_action(current_user.id, 'asset_allocation_updated', validated_data)
            
            return handle_api_success({
                'asset_allocation': asset_allocation.to_dict()
            }, 'Asset allocation updated successfully')
            
        except Exception as e:
            db.session.rollback()
            return handle_api_error('Failed to update asset allocation', 'update_error', 500)
    
    @staticmethod
    def get_asset_allocations(current_user):
        """Get all user asset allocations"""
        try:
            allocations = AssetAllocation.get_by_user_id(current_user.id)
            
            return handle_api_success({
                'asset_allocations': [allocation.to_dict() for allocation in allocations],
                'total_portfolio_value': float(AssetAllocation.get_total_portfolio_value(current_user.id))
            }, 'Asset allocations retrieved successfully')
            
        except Exception as e:
            return handle_api_error('Failed to retrieve asset allocations', 'retrieve_error', 500)
    
    @staticmethod
    @validate_json(FinancialGoalSchema)
    def create_financial_goal(current_user, validated_data):
        """Create new financial goal"""
        try:
            goal = FinancialGoal.create(
                user_id=current_user.id,
                **validated_data
            )
            
            # Log user action
            log_user_action(current_user.id, 'financial_goal_created', validated_data)
            
            return handle_api_success({
                'financial_goal': goal.to_dict()
            }, 'Financial goal created successfully', 201)
            
        except Exception as e:
            db.session.rollback()
            return handle_api_error('Failed to create financial goal', 'create_error', 500)
    
    @staticmethod
    def get_financial_goals(current_user):
        """Get all user financial goals"""
        try:
            goals = FinancialGoal.get_by_user_id(current_user.id)
            
            return handle_api_success({
                'financial_goals': [goal.to_dict() for goal in goals]
            }, 'Financial goals retrieved successfully')
            
        except Exception as e:
            return handle_api_error('Failed to retrieve financial goals', 'retrieve_error', 500)
    
    @staticmethod
    @validate_json(FinancialGoalSchema)
    def update_financial_goal(current_user, goal_id, validated_data):
        """Update financial goal"""
        try:
            goal = FinancialGoal.get_by_id(goal_id)
            
            if not goal or goal.user_id != current_user.id:
                return handle_api_error('Financial goal not found', 'not_found', 404)
            
            goal.update(**validated_data)
            
            # Log user action
            log_user_action(current_user.id, 'financial_goal_updated', {
                'goal_id': goal_id,
                **validated_data
            })
            
            return handle_api_success({
                'financial_goal': goal.to_dict()
            }, 'Financial goal updated successfully')
            
        except Exception as e:
            db.session.rollback()
            return handle_api_error('Failed to update financial goal', 'update_error', 500)
    
    @staticmethod
    def delete_financial_goal(current_user, goal_id):
        """Delete financial goal"""
        try:
            goal = FinancialGoal.get_by_id(goal_id)
            
            if not goal or goal.user_id != current_user.id:
                return handle_api_error('Financial goal not found', 'not_found', 404)
            
            goal.delete()
            
            # Log user action
            log_user_action(current_user.id, 'financial_goal_deleted', {'goal_id': goal_id})
            
            return handle_api_success(message='Financial goal deleted successfully')
            
        except Exception as e:
            db.session.rollback()
            return handle_api_error('Failed to delete financial goal', 'delete_error', 500)
    
    @staticmethod
    def get_financial_summary(current_user):
        """Get comprehensive financial summary"""
        try:
            # Get all financial data
            financial_data = FinancialData.get_by_user_id(current_user.id)
            risk_profile = RiskProfile.get_by_user_id(current_user.id)
            allocations = AssetAllocation.get_by_user_id(current_user.id)
            goals = FinancialGoal.get_active_goals(current_user.id)
            
            summary = {
                'financial_data': financial_data.to_dict() if financial_data else None,
                'risk_profile': risk_profile.to_dict() if risk_profile else None,
                'asset_allocations': [allocation.to_dict() for allocation in allocations],
                'financial_goals': [goal.to_dict() for goal in goals],
                'total_portfolio_value': float(AssetAllocation.get_total_portfolio_value(current_user.id))
            }
            
            return handle_api_success({
                'financial_summary': summary
            }, 'Financial summary retrieved successfully')
            
        except Exception as e:
            return handle_api_error('Failed to retrieve financial summary', 'retrieve_error', 500)

