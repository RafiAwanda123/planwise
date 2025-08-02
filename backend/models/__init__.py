"""
Models package initialization
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

# Import all models
from .user import User
from .risk_profile import RiskProfile
from .financial_data import FinancialData
from .asset_allocation import AssetAllocation
from .financial_goal import FinancialGoal
from .risk_assessment import RiskAssessment
from .monte_carlo_simulation import MonteCarloSimulation
from .report import Report

__all__ = [
    'db',
    'migrate',
    'User',
    'RiskProfile',
    'FinancialData',
    'AssetAllocation',
    'FinancialGoal',
    'RiskAssessment',
    'MonteCarloSimulation',
    'Report'
]

