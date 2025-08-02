"""
Asset Allocation model for portfolio management
"""
from decimal import Decimal
from . import db
from .base import BaseModel

class AssetAllocation(BaseModel):
    """Asset Allocation model"""
    
    __tablename__ = 'asset_allocations'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    asset_type = db.Column(db.String(50), nullable=False)  # stocks, bonds, cash, real_estate, etc.
    current_amount = db.Column(db.Numeric(15, 2), default=0)
    target_percentage = db.Column(db.Numeric(5, 2), default=0)
    recommended_percentage = db.Column(db.Numeric(5, 2), default=0)
    
    def __init__(self, user_id, asset_type, current_amount=0, 
                 target_percentage=0, recommended_percentage=0):
        self.user_id = user_id
        self.asset_type = asset_type
        self.current_amount = Decimal(str(current_amount))
        self.target_percentage = Decimal(str(target_percentage))
        self.recommended_percentage = Decimal(str(recommended_percentage))
    
    @classmethod
    def get_by_user_id(cls, user_id):
        """Get all asset allocations by user ID"""
        return cls.query.filter_by(user_id=user_id).all()
    
    @classmethod
    def get_by_user_and_type(cls, user_id, asset_type):
        """Get asset allocation by user ID and asset type"""
        return cls.query.filter_by(user_id=user_id, asset_type=asset_type).first()
    
    @classmethod
    def create_or_update(cls, user_id, asset_type, **kwargs):
        """Create or update asset allocation"""
        allocation = cls.get_by_user_and_type(user_id, asset_type)
        if allocation:
            allocation.update(**kwargs)
            return allocation
        else:
            return cls.create(user_id=user_id, asset_type=asset_type, **kwargs)
    
    @classmethod
    def get_total_portfolio_value(cls, user_id):
        """Get total portfolio value for user"""
        allocations = cls.get_by_user_id(user_id)
        return sum(allocation.current_amount for allocation in allocations)
    
    @property
    def current_percentage(self):
        """Calculate current percentage of total portfolio"""
        total_value = self.get_total_portfolio_value(self.user_id)
        if total_value == 0:
            return 0
        return float(self.current_amount / total_value * 100)
    
    @property
    def rebalance_amount(self):
        """Calculate amount needed to rebalance to target"""
        total_value = self.get_total_portfolio_value(self.user_id)
        target_amount = total_value * (self.target_percentage / 100)
        return float(target_amount - self.current_amount)
    
    def to_dict(self):
        """Convert to dictionary with calculated fields"""
        data = super().to_dict()
        data.update({
            'current_percentage': self.current_percentage,
            'rebalance_amount': self.rebalance_amount
        })
        return data
    
    def __repr__(self):
        return f'<AssetAllocation user_id={self.user_id} type={self.asset_type}>'

