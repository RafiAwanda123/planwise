"""
Risk Assessment model for storing risk evaluation results
"""
from decimal import Decimal
from datetime import datetime
from . import db
from .base import BaseModel

class RiskAssessment(BaseModel):
    """Risk Assessment model"""
    
    __tablename__ = 'risk_assessments'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    liquidity_risk_score = db.Column(db.Numeric(3, 1), default=0)
    credit_risk_score = db.Column(db.Numeric(3, 1), default=0)
    market_risk_score = db.Column(db.Numeric(3, 1), default=0)
    inflation_risk_score = db.Column(db.Numeric(3, 1), default=0)
    protection_risk_score = db.Column(db.Numeric(3, 1), default=0)
    total_risk_score = db.Column(db.Numeric(3, 1), default=0)
    risk_level = db.Column(db.Enum('low', 'moderate', 'high', name='risk_level_enum'), nullable=True)
    assessment_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Risk weights for total score calculation
    RISK_WEIGHTS = {
        'liquidity': 0.25,
        'credit': 0.20,
        'market': 0.25,
        'inflation': 0.15,
        'protection': 0.15
    }
    
    def __init__(self, user_id, liquidity_risk_score=0, credit_risk_score=0, 
                 market_risk_score=0, inflation_risk_score=0, protection_risk_score=0):
        self.user_id = user_id
        self.liquidity_risk_score = Decimal(str(liquidity_risk_score))
        self.credit_risk_score = Decimal(str(credit_risk_score))
        self.market_risk_score = Decimal(str(market_risk_score))
        self.inflation_risk_score = Decimal(str(inflation_risk_score))
        self.protection_risk_score = Decimal(str(protection_risk_score))
        self.calculate_total_score()
        self.assessment_date = datetime.utcnow()
    
    def calculate_total_score(self):
        """Calculate total risk score using weighted average"""
        total = (
            float(self.liquidity_risk_score) * self.RISK_WEIGHTS['liquidity'] +
            float(self.credit_risk_score) * self.RISK_WEIGHTS['credit'] +
            float(self.market_risk_score) * self.RISK_WEIGHTS['market'] +
            float(self.inflation_risk_score) * self.RISK_WEIGHTS['inflation'] +
            float(self.protection_risk_score) * self.RISK_WEIGHTS['protection']
        )
        self.total_risk_score = Decimal(str(round(total, 1)))
        self.risk_level = self.get_risk_level()
    
    def get_risk_level(self):
        """Determine risk level based on total score"""
        score = float(self.total_risk_score)
        if score <= 3.0:
            return 'low'
        elif score <= 7.0:
            return 'moderate'
        else:
            return 'high'
    
    @classmethod
    def get_by_user_id(cls, user_id):
        """Get latest risk assessment by user ID"""
        return cls.query.filter_by(user_id=user_id).order_by(cls.assessment_date.desc()).first()
    
    @classmethod
    def get_history_by_user_id(cls, user_id, limit=10):
        """Get risk assessment history by user ID"""
        return cls.query.filter_by(user_id=user_id).order_by(cls.assessment_date.desc()).limit(limit).all()
    
    @classmethod
    def create_assessment(cls, user_id, **risk_scores):
        """Create new risk assessment"""
        assessment = cls(user_id=user_id, **risk_scores)
        return assessment.save()
    
    def get_risk_breakdown(self):
        """Get detailed risk breakdown"""
        return {
            'liquidity': {
                'score': float(self.liquidity_risk_score),
                'weight': self.RISK_WEIGHTS['liquidity'],
                'weighted_score': float(self.liquidity_risk_score) * self.RISK_WEIGHTS['liquidity'],
                'description': 'Risk of not having enough liquid assets for emergencies'
            },
            'credit': {
                'score': float(self.credit_risk_score),
                'weight': self.RISK_WEIGHTS['credit'],
                'weighted_score': float(self.credit_risk_score) * self.RISK_WEIGHTS['credit'],
                'description': 'Risk related to debt levels and creditworthiness'
            },
            'market': {
                'score': float(self.market_risk_score),
                'weight': self.RISK_WEIGHTS['market'],
                'weighted_score': float(self.market_risk_score) * self.RISK_WEIGHTS['market'],
                'description': 'Risk from market volatility and investment losses'
            },
            'inflation': {
                'score': float(self.inflation_risk_score),
                'weight': self.RISK_WEIGHTS['inflation'],
                'weighted_score': float(self.inflation_risk_score) * self.RISK_WEIGHTS['inflation'],
                'description': 'Risk of purchasing power erosion due to inflation'
            },
            'protection': {
                'score': float(self.protection_risk_score),
                'weight': self.RISK_WEIGHTS['protection'],
                'weighted_score': float(self.protection_risk_score) * self.RISK_WEIGHTS['protection'],
                'description': 'Risk from inadequate insurance coverage'
            }
        }
    
    def get_recommendations(self):
        """Get risk-based recommendations"""
        recommendations = []
        
        if float(self.liquidity_risk_score) > 6:
            recommendations.append("Build emergency fund to cover 3-6 months of expenses")
        
        if float(self.credit_risk_score) > 6:
            recommendations.append("Reduce debt levels and improve debt-to-income ratio")
        
        if float(self.market_risk_score) > 6:
            recommendations.append("Diversify investments and consider lower-risk assets")
        
        if float(self.inflation_risk_score) > 6:
            recommendations.append("Consider inflation-protected investments")
        
        if float(self.protection_risk_score) > 6:
            recommendations.append("Review and increase insurance coverage")
        
        return recommendations
    
    def to_dict(self):
        """Convert to dictionary with additional fields"""
        data = super().to_dict()
        data.update({
            'risk_breakdown': self.get_risk_breakdown(),
            'recommendations': self.get_recommendations()
        })
        return data
    
    def __repr__(self):
        return f'<RiskAssessment user_id={self.user_id} score={self.total_risk_score}>'

