"""
User model for authentication and user management
"""
from flask_bcrypt import generate_password_hash, check_password_hash
from . import db
from .base import BaseModel

class User(BaseModel):
    """User model"""
    
    __tablename__ = 'users'
    
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), default='user')
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    risk_profile = db.relationship('RiskProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    financial_data = db.relationship('FinancialData', backref='user', uselist=False, cascade='all, delete-orphan')
    asset_allocations = db.relationship('AssetAllocation', backref='user', cascade='all, delete-orphan')
    financial_goals = db.relationship('FinancialGoal', backref='user', cascade='all, delete-orphan')
    risk_assessments = db.relationship('RiskAssessment', backref='user', cascade='all, delete-orphan')
    monte_carlo_simulations = db.relationship('MonteCarloSimulation', backref='user', cascade='all, delete-orphan')
    reports = db.relationship('Report', backref='user', cascade='all, delete-orphan')
    
    def __init__(self, email, password, first_name, last_name, role='user'):
        self.email = email.lower().strip()
        self.set_password(password)
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.role = role
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    @property
    def full_name(self):
        """Get full name"""
        return f"{self.first_name} {self.last_name}"
    
    def to_dict(self, include_sensitive=False):
        """Convert to dictionary"""
        data = super().to_dict()
        # Remove sensitive information
        if not include_sensitive:
            data.pop('password_hash', None)
        return data
    
    @classmethod
    def get_by_email(cls, email):
        """Get user by email"""
        return cls.query.filter_by(email=email.lower().strip()).first()
    
    @classmethod
    def create_user(cls, email, password, first_name, last_name, role='user'):
        """Create new user"""
        # Check if user already exists
        if cls.get_by_email(email):
            raise ValueError("User with this email already exists")
        
        user = cls(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role
        )
        return user.save()
    
    def deactivate(self):
        """Deactivate user account"""
        self.is_active = False
        return self.save()
    
    def activate(self):
        """Activate user account"""
        self.is_active = True
        return self.save()
    
    def __repr__(self):
        return f'<User {self.email}>'

