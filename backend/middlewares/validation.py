"""
Validation middleware for request validation
"""
from functools import wraps
from flask import request, jsonify
from marshmallow import Schema, fields, ValidationError, validate

# Base validation schemas
class UserRegistrationSchema(Schema):
    """User registration validation schema"""
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    role = fields.Str(missing='user', validate=validate.OneOf(['user', 'admin']))

class UserLoginSchema(Schema):
    """User login validation schema"""
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class RiskProfileSchema(Schema):
    """Risk profile validation schema"""
    risk_tolerance = fields.Str(validate=validate.OneOf(['conservative', 'moderate', 'aggressive']))
    investment_experience = fields.Str(validate=validate.OneOf(['beginner', 'intermediate', 'advanced']))
    time_horizon = fields.Int(validate=validate.Range(min=1, max=50))
    age = fields.Int(validate=validate.Range(min=18, max=100))
    employment_status = fields.Str(validate=validate.Length(max=50))

class FinancialDataSchema(Schema):
    """Financial data validation schema"""
    monthly_income = fields.Decimal(required=True, validate=validate.Range(min=0))
    monthly_expenses = fields.Decimal(required=True, validate=validate.Range(min=0))
    total_assets = fields.Decimal(missing=0, validate=validate.Range(min=0))
    total_debt = fields.Decimal(missing=0, validate=validate.Range(min=0))
    emergency_fund = fields.Decimal(missing=0, validate=validate.Range(min=0))
    insurance_coverage = fields.Decimal(missing=0, validate=validate.Range(min=0))

class AssetAllocationSchema(Schema):
    """Asset allocation validation schema"""
    asset_type = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    current_amount = fields.Decimal(missing=0, validate=validate.Range(min=0))
    target_percentage = fields.Decimal(missing=0, validate=validate.Range(min=0, max=100))
    recommended_percentage = fields.Decimal(missing=0, validate=validate.Range(min=0, max=100))

class FinancialGoalSchema(Schema):
    """Financial goal validation schema"""
    goal_name = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    target_amount = fields.Decimal(required=True, validate=validate.Range(min=0))
    current_amount = fields.Decimal(missing=0, validate=validate.Range(min=0))
    target_date = fields.Date()
    priority = fields.Str(missing='medium', validate=validate.OneOf(['low', 'medium', 'high']))
    status = fields.Str(missing='active', validate=validate.OneOf(['active', 'completed', 'paused']))

class MonteCarloSimulationSchema(Schema):
    """Monte Carlo simulation validation schema"""
    simulation_name = fields.Str(validate=validate.Length(max=255))
    initial_portfolio_value = fields.Decimal(required=True, validate=validate.Range(min=0))
    expected_return = fields.Decimal(required=True, validate=validate.Range(min=-1, max=1))
    volatility = fields.Decimal(required=True, validate=validate.Range(min=0, max=1))
    time_horizon = fields.Int(required=True, validate=validate.Range(min=1, max=50))
    iterations = fields.Int(missing=10000, validate=validate.Range(min=1000, max=100000))

# Validation decorator
def validate_json(schema_class):
    """Decorator to validate JSON request data"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({
                    'success': False,
                    'message': 'Content-Type must be application/json',
                    'error': 'invalid_content_type'
                }), 400
            
            try:
                schema = schema_class()
                validated_data = schema.load(request.get_json())
                return f(validated_data, *args, **kwargs)
            except ValidationError as err:
                return jsonify({
                    'success': False,
                    'message': 'Validation error',
                    'errors': err.messages,
                    'error': 'validation_error'
                }), 400
            except Exception as err:
                return jsonify({
                    'success': False,
                    'message': 'Invalid JSON data',
                    'error': 'invalid_json'
                }), 400
        
        return decorated_function
    return decorator

def validate_query_params(schema_class):
    """Decorator to validate query parameters"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                schema = schema_class()
                validated_data = schema.load(request.args)
                return f(validated_data, *args, **kwargs)
            except ValidationError as err:
                return jsonify({
                    'success': False,
                    'message': 'Query parameter validation error',
                    'errors': err.messages,
                    'error': 'validation_error'
                }), 400
        
        return decorated_function
    return decorator

# Custom validators
def validate_positive_number(value):
    """Validate that a number is positive"""
    if value <= 0:
        raise ValidationError('Value must be positive')

def validate_percentage(value):
    """Validate that a value is a valid percentage (0-100)"""
    if not 0 <= value <= 100:
        raise ValidationError('Value must be between 0 and 100')

def validate_risk_score(value):
    """Validate that a risk score is between 0 and 10"""
    if not 0 <= value <= 10:
        raise ValidationError('Risk score must be between 0 and 10')

