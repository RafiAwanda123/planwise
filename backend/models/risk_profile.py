"""
Risk Profile model for user risk assessment
"""
from . import db
from .base import BaseModel

class RiskProfile(BaseModel):
    """Risk Profile model"""
    
    __tablename__ = 'risk_profiles'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    risk_tolerance = db.Column(db.Enum('conservative', 'moderate', 'aggressive', name='risk_tolerance_enum'), nullable=True)
    investment_experience = db.Column(db.Enum('beginner', 'intermediate', 'advanced', name='investment_experience_enum'), nullable=True)
    time_horizon = db.Column(db.Integer, nullable=True)  # in years
    age = db.Column(db.Integer, nullable=True)
    employment_status = db.Column(db.String(50), nullable=True)
    
    def __init__(self, user_id, risk_tolerance=None, investment_experience=None, 
                 time_horizon=None, age=None, employment_status=None):
        self.user_id = user_id
        self.risk_tolerance = risk_tolerance
        self.investment_experience = investment_experience
        self.time_horizon = time_horizon
        self.age = age
        self.employment_status = employment_status
    
    @classmethod
    def get_by_user_id(cls, user_id):
        """Get risk profile by user ID"""
        return cls.query.filter_by(user_id=user_id).first()
    
    @classmethod
    def create_or_update(cls, user_id, **kwargs):
        """Create or update risk profile"""
        profile = cls.get_by_user_id(user_id)
        if profile:
            profile.update(**kwargs)
            return profile
        else:
            return cls.create(user_id=user_id, **kwargs)
    
    def get_risk_score(self):
        """Calculate risk score based on profile"""
        score = 0
        
        # Risk tolerance scoring
        if self.risk_tolerance == 'conservative':
            score += 1
        elif self.risk_tolerance == 'moderate':
            score += 2
        elif self.risk_tolerance == 'aggressive':
            score += 3
        
        # Investment experience scoring
        if self.investment_experience == 'beginner':
            score += 1
        elif self.investment_experience == 'intermediate':
            score += 2
        elif self.investment_experience == 'advanced':
            score += 3
        
        # Time horizon scoring
        if self.time_horizon:
            if self.time_horizon <= 3:
                score += 1
            elif self.time_horizon <= 10:
                score += 2
            else:
                score += 3
        
        # Age scoring (younger = higher risk capacity)
        if self.age:
            if self.age >= 60:
                score += 1
            elif self.age >= 40:
                score += 2
            else:
                score += 3
        
        return min(score, 10)  # Cap at 10
    
    def get_risk_level(self):
        """Get risk level based on score"""
        score = self.get_risk_score()
        if score <= 3:
            return 'low'
        elif score <= 7:
            return 'moderate'
        else:
            return 'high'
    
    def __repr__(self):
        return f'<RiskProfile user_id={self.user_id} tolerance={self.risk_tolerance}>'

