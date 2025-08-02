"""
Financial Goal model for user financial objectives
"""
from datetime import datetime, date
from decimal import Decimal
from . import db
from .base import BaseModel

class FinancialGoal(BaseModel):
    """Financial Goal model"""
    
    __tablename__ = 'financial_goals'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    goal_name = db.Column(db.String(255), nullable=False)
    target_amount = db.Column(db.Numeric(15, 2), nullable=False)
    current_amount = db.Column(db.Numeric(15, 2), default=0)
    target_date = db.Column(db.Date, nullable=True)
    priority = db.Column(db.Enum('low', 'medium', 'high', name='priority_enum'), nullable=True)
    status = db.Column(db.Enum('active', 'completed', 'paused', name='status_enum'), default='active')
    
    def __init__(self, user_id, goal_name, target_amount, current_amount=0, 
                 target_date=None, priority='medium', status='active'):
        self.user_id = user_id
        self.goal_name = goal_name
        self.target_amount = Decimal(str(target_amount))
        self.current_amount = Decimal(str(current_amount))
        self.target_date = target_date
        self.priority = priority
        self.status = status
    
    @property
    def progress_percentage(self):
        """Calculate progress percentage"""
        if self.target_amount == 0:
            return 0
        return float(self.current_amount / self.target_amount * 100)
    
    @property
    def remaining_amount(self):
        """Calculate remaining amount needed"""
        return float(self.target_amount - self.current_amount)
    
    @property
    def days_remaining(self):
        """Calculate days remaining to target date"""
        if not self.target_date:
            return None
        today = date.today()
        if self.target_date <= today:
            return 0
        return (self.target_date - today).days
    
    @property
    def monthly_savings_needed(self):
        """Calculate monthly savings needed to reach goal"""
        if not self.target_date or self.days_remaining is None or self.days_remaining <= 0:
            return None
        
        months_remaining = self.days_remaining / 30.44  # Average days per month
        if months_remaining <= 0:
            return None
        
        return float(self.remaining_amount / months_remaining)
    
    @property
    def is_on_track(self):
        """Check if goal is on track based on time and progress"""
        if not self.target_date or self.days_remaining is None:
            return None
        
        total_days = (self.target_date - self.created_at.date()).days
        if total_days <= 0:
            return False
        
        expected_progress = ((total_days - self.days_remaining) / total_days) * 100
        return self.progress_percentage >= expected_progress * 0.9  # 10% tolerance
    
    @classmethod
    def get_by_user_id(cls, user_id):
        """Get all goals by user ID"""
        return cls.query.filter_by(user_id=user_id).all()
    
    @classmethod
    def get_active_goals(cls, user_id):
        """Get active goals by user ID"""
        return cls.query.filter_by(user_id=user_id, status='active').all()
    
    @classmethod
    def get_by_priority(cls, user_id, priority):
        """Get goals by user ID and priority"""
        return cls.query.filter_by(user_id=user_id, priority=priority).all()
    
    def update_progress(self, amount):
        """Update current amount"""
        self.current_amount = Decimal(str(amount))
        if self.current_amount >= self.target_amount:
            self.status = 'completed'
        return self.save()
    
    def add_contribution(self, amount):
        """Add contribution to current amount"""
        self.current_amount += Decimal(str(amount))
        if self.current_amount >= self.target_amount:
            self.status = 'completed'
        return self.save()
    
    def to_dict(self):
        """Convert to dictionary with calculated fields"""
        data = super().to_dict()
        data.update({
            'progress_percentage': self.progress_percentage,
            'remaining_amount': self.remaining_amount,
            'days_remaining': self.days_remaining,
            'monthly_savings_needed': self.monthly_savings_needed,
            'is_on_track': self.is_on_track
        })
        # Convert date to string
        if self.target_date:
            data['target_date'] = self.target_date.isoformat()
        return data
    
    def __repr__(self):
        return f'<FinancialGoal user_id={self.user_id} name={self.goal_name}>'

