"""
Report model for storing generated reports
"""
import json
from datetime import datetime
from . import db
from .base import BaseModel

class Report(BaseModel):
    """Report model"""
    
    __tablename__ = 'reports'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    report_type = db.Column(db.String(50), nullable=False)  # dashboard, pdf, detailed
    report_data = db.Column(db.Text, nullable=True)  # JSON data
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    file_path = db.Column(db.String(500), nullable=True)
    
    def __init__(self, user_id, report_type, report_data=None, file_path=None):
        self.user_id = user_id
        self.report_type = report_type
        self.set_report_data(report_data)
        self.file_path = file_path
        self.generated_at = datetime.utcnow()
    
    def set_report_data(self, data):
        """Set report data as JSON"""
        if data:
            self.report_data = json.dumps(data) if isinstance(data, dict) else data
    
    def get_report_data(self):
        """Get report data as dictionary"""
        if not self.report_data:
            return None
        try:
            return json.loads(self.report_data)
        except json.JSONDecodeError:
            return self.report_data
    
    @classmethod
    def get_by_user_id(cls, user_id):
        """Get all reports by user ID"""
        return cls.query.filter_by(user_id=user_id).order_by(cls.generated_at.desc()).all()
    
    @classmethod
    def get_by_type(cls, user_id, report_type):
        """Get reports by user ID and type"""
        return cls.query.filter_by(user_id=user_id, report_type=report_type).order_by(cls.generated_at.desc()).all()
    
    @classmethod
    def get_latest_by_type(cls, user_id, report_type):
        """Get latest report by user ID and type"""
        return cls.query.filter_by(user_id=user_id, report_type=report_type).order_by(cls.generated_at.desc()).first()
    
    @classmethod
    def create_report(cls, user_id, report_type, report_data=None, file_path=None):
        """Create new report"""
        report = cls(
            user_id=user_id,
            report_type=report_type,
            report_data=report_data,
            file_path=file_path
        )
        return report.save()
    
    def update_file_path(self, file_path):
        """Update file path"""
        self.file_path = file_path
        return self.save()
    
    def to_dict(self):
        """Convert to dictionary"""
        data = super().to_dict()
        data['report_data'] = self.get_report_data()
        return data
    
    def __repr__(self):
        return f'<Report user_id={self.user_id} type={self.report_type}>'

