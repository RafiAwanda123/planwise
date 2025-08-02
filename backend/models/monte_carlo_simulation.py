"""
Monte Carlo Simulation model for portfolio projections
"""
import json
from decimal import Decimal
from . import db
from .base import BaseModel

class MonteCarloSimulation(BaseModel):
    """Monte Carlo Simulation model"""
    
    __tablename__ = 'monte_carlo_simulations'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    simulation_name = db.Column(db.String(255), nullable=True)
    initial_portfolio_value = db.Column(db.Numeric(15, 2), nullable=True)
    expected_return = db.Column(db.Numeric(5, 4), nullable=True)  # e.g., 0.0700 for 7%
    volatility = db.Column(db.Numeric(5, 4), nullable=True)  # e.g., 0.1500 for 15%
    time_horizon = db.Column(db.Integer, nullable=True)  # in years
    iterations = db.Column(db.Integer, default=10000)
    success_probability = db.Column(db.Numeric(5, 2), nullable=True)  # percentage
    var_95 = db.Column(db.Numeric(15, 2), nullable=True)  # Value at Risk 95%
    var_99 = db.Column(db.Numeric(15, 2), nullable=True)  # Value at Risk 99%
    expected_value = db.Column(db.Numeric(15, 2), nullable=True)
    simulation_results = db.Column(db.Text, nullable=True)  # JSON data
    
    def __init__(self, user_id, simulation_name=None, initial_portfolio_value=0, 
                 expected_return=0, volatility=0, time_horizon=1, iterations=10000):
        self.user_id = user_id
        self.simulation_name = simulation_name or f"Simulation {self.id}"
        self.initial_portfolio_value = Decimal(str(initial_portfolio_value))
        self.expected_return = Decimal(str(expected_return))
        self.volatility = Decimal(str(volatility))
        self.time_horizon = time_horizon
        self.iterations = iterations
    
    def set_results(self, results_data):
        """Set simulation results"""
        self.success_probability = Decimal(str(results_data.get('success_probability', 0)))
        self.var_95 = Decimal(str(results_data.get('var_95', 0)))
        self.var_99 = Decimal(str(results_data.get('var_99', 0)))
        self.expected_value = Decimal(str(results_data.get('expected_value', 0)))
        
        # Store detailed results as JSON
        simulation_data = {
            'final_values': results_data.get('final_values', []),
            'percentiles': results_data.get('percentiles', {}),
            'statistics': results_data.get('statistics', {}),
            'yearly_projections': results_data.get('yearly_projections', [])
        }
        self.simulation_results = json.dumps(simulation_data)
    
    def get_results(self):
        """Get simulation results as dictionary"""
        if not self.simulation_results:
            return None
        return json.loads(self.simulation_results)
    
    @classmethod
    def get_by_user_id(cls, user_id):
        """Get all simulations by user ID"""
        return cls.query.filter_by(user_id=user_id).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def get_latest_by_user_id(cls, user_id):
        """Get latest simulation by user ID"""
        return cls.query.filter_by(user_id=user_id).order_by(cls.created_at.desc()).first()
    
    def get_summary(self):
        """Get simulation summary"""
        return {
            'simulation_name': self.simulation_name,
            'initial_value': float(self.initial_portfolio_value),
            'expected_return': float(self.expected_return) * 100,  # Convert to percentage
            'volatility': float(self.volatility) * 100,  # Convert to percentage
            'time_horizon': self.time_horizon,
            'iterations': self.iterations,
            'success_probability': float(self.success_probability) if self.success_probability else None,
            'expected_final_value': float(self.expected_value) if self.expected_value else None,
            'var_95': float(self.var_95) if self.var_95 else None,
            'var_99': float(self.var_99) if self.var_99 else None
        }
    
    def get_risk_metrics(self):
        """Get risk metrics from simulation"""
        if not self.simulation_results:
            return None
        
        results = self.get_results()
        return {
            'value_at_risk_95': float(self.var_95) if self.var_95 else None,
            'value_at_risk_99': float(self.var_99) if self.var_99 else None,
            'expected_shortfall': results.get('statistics', {}).get('expected_shortfall'),
            'maximum_drawdown': results.get('statistics', {}).get('max_drawdown'),
            'volatility_of_returns': results.get('statistics', {}).get('return_volatility')
        }
    
    def to_dict(self):
        """Convert to dictionary with additional fields"""
        data = super().to_dict()
        data.update({
            'summary': self.get_summary(),
            'risk_metrics': self.get_risk_metrics(),
            'detailed_results': self.get_results()
        })
        return data
    
    def __repr__(self):
        return f'<MonteCarloSimulation user_id={self.user_id} name={self.simulation_name}>'

