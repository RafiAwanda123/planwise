"""
Financial Data model for user financial information
"""
from decimal import Decimal
from . import db
from .base import BaseModel

class FinancialData(BaseModel):
    """Financial Data model"""
    
    __tablename__ = 'financial_data'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    monthly_income = db.Column(db.Numeric(15, 2), nullable=False)
    monthly_expenses = db.Column(db.Numeric(15, 2), nullable=False)
    total_assets = db.Column(db.Numeric(15, 2), default=0)
    total_debt = db.Column(db.Numeric(15, 2), default=0)
    emergency_fund = db.Column(db.Numeric(15, 2), default=0)
    insurance_coverage = db.Column(db.Numeric(15, 2), default=0)
    
    def __init__(self, user_id, monthly_income, monthly_expenses, 
                 total_assets=0, total_debt=0, emergency_fund=0, insurance_coverage=0):
        self.user_id = user_id
        self.monthly_income = Decimal(str(monthly_income))
        self.monthly_expenses = Decimal(str(monthly_expenses))
        self.total_assets = Decimal(str(total_assets))
        self.total_debt = Decimal(str(total_debt))
        self.emergency_fund = Decimal(str(emergency_fund))
        self.insurance_coverage = Decimal(str(insurance_coverage))
    
    @property
    def monthly_surplus(self):
        """Calculate monthly surplus/deficit"""
        return self.monthly_income - self.monthly_expenses
    
    @property
    def net_worth(self):
        """Calculate net worth"""
        return self.total_assets - self.total_debt
    
    @property
    def debt_to_income_ratio(self):
        """Calculate debt to income ratio"""
        if self.monthly_income == 0:
            return 0
        return float(self.total_debt / (self.monthly_income * 12))
    
    @property
    def emergency_fund_months(self):
        """Calculate emergency fund in months of expenses"""
        if self.monthly_expenses == 0:
            return 0
        return float(self.emergency_fund / self.monthly_expenses)
    
    @property
    def savings_rate(self):
        """Calculate savings rate"""
        if self.monthly_income == 0:
            return 0
        return float(self.monthly_surplus / self.monthly_income)
    
    @classmethod
    def get_by_user_id(cls, user_id):
        """Get financial data by user ID"""
        return cls.query.filter_by(user_id=user_id).first()
    
    @classmethod
    def create_or_update(cls, user_id, **kwargs):
        """Create or update financial data"""
        financial_data = cls.get_by_user_id(user_id)
        if financial_data:
            financial_data.update(**kwargs)
            return financial_data
        else:
            return cls.create(user_id=user_id, **kwargs)
    
    def calculate_liquidity_risk(self):
        """Calculate liquidity risk score (0-10)"""
        # Based on emergency fund coverage
        months_coverage = self.emergency_fund_months
        
        if months_coverage >= 6:
            return 2.0  # Low risk
        elif months_coverage >= 3:
            return 5.0  # Moderate risk
        else:
            return 8.0  # High risk
    
    def calculate_debt_risk(self):
        """Calculate debt risk score (0-10)"""
        debt_ratio = self.debt_to_income_ratio
        
        if debt_ratio <= 0.2:
            return 2.0  # Low risk
        elif debt_ratio <= 0.4:
            return 5.0  # Moderate risk
        else:
            return 8.0  # High risk
    
    def calculate_income_stability_risk(self):
        """Calculate income stability risk score (0-10)"""
        # This would need more data, for now use savings rate as proxy
        savings_rate = self.savings_rate
        
        if savings_rate >= 0.2:
            return 2.0  # Low risk
        elif savings_rate >= 0.1:
            return 5.0  # Moderate risk
        else:
            return 8.0  # High risk
    
    def to_dict(self):
        """Convert to dictionary with calculated fields"""
        data = super().to_dict()
        data.update({
            'monthly_surplus': float(self.monthly_surplus),
            'net_worth': float(self.net_worth),
            'debt_to_income_ratio': self.debt_to_income_ratio,
            'emergency_fund_months': self.emergency_fund_months,
            'savings_rate': self.savings_rate
        })
        return data
    
    def __repr__(self):
        return f'<FinancialData user_id={self.user_id} income={self.monthly_income}>'

