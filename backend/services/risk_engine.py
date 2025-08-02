"""
Risk Engine Module for comprehensive financial risk assessment
Based on ISO 31000:2018 framework for risk management
"""
import numpy as np
from typing import Dict, Optional, List, Tuple
from decimal import Decimal

class RiskEngine:
    """
    Comprehensive Risk Engine for financial risk assessment
    Implements ISO 31000:2018 framework principles
    """
    
    # Risk weights for total score calculation
    RISK_WEIGHTS = {
        'liquidity': 0.25,      # Emergency fund vs expenses
        'credit': 0.20,         # Debt levels and creditworthiness
        'market': 0.25,         # Investment portfolio volatility
        'inflation': 0.15,      # Purchasing power erosion
        'protection': 0.15      # Insurance coverage adequacy
    }
    
    # Risk thresholds for scoring
    LIQUIDITY_THRESHOLDS = {
        'excellent': 6.0,    # 6+ months emergency fund
        'good': 3.0,         # 3-6 months emergency fund
        'fair': 1.0,         # 1-3 months emergency fund
        'poor': 0.0          # <1 month emergency fund
    }
    
    DEBT_RATIO_THRESHOLDS = {
        'excellent': 0.20,   # <20% debt-to-income
        'good': 0.40,        # 20-40% debt-to-income
        'fair': 0.60,        # 40-60% debt-to-income
        'poor': 1.0          # >60% debt-to-income
    }
    
    def __init__(self, financial_data, risk_profile=None, risk_assessment=None):
        """
        Initialize Risk Engine with user financial data
        
        Args:
            financial_data: FinancialData model instance
            risk_profile: RiskProfile model instance (optional)
            risk_assessment: Previous RiskAssessment (optional)
        """
        self.financial_data = financial_data
        self.risk_profile = risk_profile
        self.risk_assessment = risk_assessment
    
    def calculate_liquidity_risk(self) -> float:
        """
        Calculate liquidity risk score (0-10)
        Based on emergency fund coverage and cash flow
        
        Returns:
            float: Risk score from 0 (low risk) to 10 (high risk)
        """
        if not self.financial_data:
            return 8.0  # High risk if no data
        
        # Emergency fund months coverage
        emergency_months = self.financial_data.emergency_fund_months
        
        # Base score from emergency fund coverage
        if emergency_months >= self.LIQUIDITY_THRESHOLDS['excellent']:
            base_score = 1.0
        elif emergency_months >= self.LIQUIDITY_THRESHOLDS['good']:
            base_score = 3.0
        elif emergency_months >= self.LIQUIDITY_THRESHOLDS['fair']:
            base_score = 6.0
        else:
            base_score = 9.0
        
        # Adjust for cash flow
        monthly_surplus = float(self.financial_data.monthly_surplus)
        if monthly_surplus < 0:
            base_score += 1.0  # Negative cash flow increases risk
        elif monthly_surplus < float(self.financial_data.monthly_expenses) * 0.1:
            base_score += 0.5  # Low surplus increases risk slightly
        
        return min(base_score, 10.0)
    
    def calculate_credit_risk(self) -> float:
        """
        Calculate credit risk score (0-10)
        Based on debt levels and debt service capacity
        
        Returns:
            float: Risk score from 0 (low risk) to 10 (high risk)
        """
        if not self.financial_data:
            return 5.0  # Moderate risk if no data
        
        # Debt-to-income ratio
        debt_ratio = self.financial_data.debt_to_income_ratio
        
        # Base score from debt ratio
        if debt_ratio <= self.DEBT_RATIO_THRESHOLDS['excellent']:
            base_score = 1.0
        elif debt_ratio <= self.DEBT_RATIO_THRESHOLDS['good']:
            base_score = 3.0
        elif debt_ratio <= self.DEBT_RATIO_THRESHOLDS['fair']:
            base_score = 6.0
        else:
            base_score = 9.0
        
        # Adjust for debt service capacity
        monthly_income = float(self.financial_data.monthly_income)
        if monthly_income > 0:
            debt_service_ratio = float(self.financial_data.total_debt) / (monthly_income * 12)
            if debt_service_ratio > 0.5:
                base_score += 1.0
        
        return min(base_score, 10.0)
    
    def calculate_market_risk(self) -> float:
        """
        Calculate market risk score (0-10)
        Based on portfolio composition and volatility exposure
        
        Returns:
            float: Risk score from 0 (low risk) to 10 (high risk)
        """
        # Base market risk assessment
        base_score = 5.0  # Default moderate risk
        
        # Adjust based on risk profile if available
        if self.risk_profile:
            if self.risk_profile.risk_tolerance == 'conservative':
                base_score = 3.0
            elif self.risk_profile.risk_tolerance == 'aggressive':
                base_score = 7.0
            
            # Adjust for investment experience
            if self.risk_profile.investment_experience == 'beginner':
                base_score += 1.0
            elif self.risk_profile.investment_experience == 'advanced':
                base_score -= 1.0
            
            # Adjust for time horizon
            if self.risk_profile.time_horizon:
                if self.risk_profile.time_horizon < 3:
                    base_score += 1.0  # Short horizon increases risk
                elif self.risk_profile.time_horizon > 10:
                    base_score -= 1.0  # Long horizon reduces risk
        
        # Adjust for asset concentration
        if self.financial_data:
            asset_to_income_ratio = float(self.financial_data.total_assets) / max(float(self.financial_data.monthly_income) * 12, 1)
            if asset_to_income_ratio > 5:
                base_score -= 0.5  # Higher assets reduce market risk impact
            elif asset_to_income_ratio < 1:
                base_score += 0.5  # Lower assets increase market risk impact
        
        return max(0.0, min(base_score, 10.0))
    
    def calculate_inflation_risk(self) -> float:
        """
        Calculate inflation risk score (0-10)
        Based on asset composition and inflation protection
        
        Returns:
            float: Risk score from 0 (low risk) to 10 (high risk)
        """
        base_score = 6.0  # Default moderate-high inflation risk
        
        # Adjust based on cash holdings
        if self.financial_data:
            cash_ratio = float(self.financial_data.emergency_fund) / max(float(self.financial_data.total_assets), 1)
            if cash_ratio > 0.5:
                base_score += 1.0  # High cash exposure increases inflation risk
            elif cash_ratio < 0.1:
                base_score -= 1.0  # Low cash exposure reduces inflation risk
        
        # Adjust based on age (younger people have more time to recover)
        if self.risk_profile and self.risk_profile.age:
            if self.risk_profile.age < 35:
                base_score -= 1.0
            elif self.risk_profile.age > 55:
                base_score += 1.0
        
        return max(0.0, min(base_score, 10.0))
    
    def calculate_protection_risk(self) -> float:
        """
        Calculate protection risk score (0-10)
        Based on insurance coverage adequacy
        
        Returns:
            float: Risk score from 0 (low risk) to 10 (high risk)
        """
        if not self.financial_data:
            return 8.0  # High risk if no data
        
        # Insurance coverage ratio to annual income
        annual_income = float(self.financial_data.monthly_income) * 12
        if annual_income == 0:
            return 7.0
        
        insurance_ratio = float(self.financial_data.insurance_coverage) / annual_income
        
        # Score based on coverage ratio
        if insurance_ratio >= 10:  # 10x annual income
            base_score = 1.0
        elif insurance_ratio >= 5:   # 5x annual income
            base_score = 3.0
        elif insurance_ratio >= 2:   # 2x annual income
            base_score = 6.0
        else:
            base_score = 9.0
        
        # Adjust for dependents (if we had this data)
        # For now, assume moderate adjustment based on age
        if self.risk_profile and self.risk_profile.age:
            if 25 <= self.risk_profile.age <= 45:  # Likely to have dependents
                base_score += 0.5
        
        return min(base_score, 10.0)
    
    def calculate_all_risks(self) -> Dict[str, float]:
        """
        Calculate all risk scores
        
        Returns:
            Dict[str, float]: Dictionary with all risk scores
        """
        risks = {
            'liquidity_risk_score': self.calculate_liquidity_risk(),
            'credit_risk_score': self.calculate_credit_risk(),
            'market_risk_score': self.calculate_market_risk(),
            'inflation_risk_score': self.calculate_inflation_risk(),
            'protection_risk_score': self.calculate_protection_risk()
        }
        
        # Calculate total weighted score
        total_score = sum(
            risks[f'{risk_type}_risk_score'] * weight 
            for risk_type, weight in self.RISK_WEIGHTS.items()
        )
        
        risks['total_risk_score'] = round(total_score, 1)
        
        return risks
    
    def get_risk_level(self, total_score: float) -> str:
        """
        Determine risk level based on total score
        
        Args:
            total_score: Total risk score
            
        Returns:
            str: Risk level ('low', 'moderate', 'high')
        """
        if total_score <= 3.0:
            return 'low'
        elif total_score <= 7.0:
            return 'moderate'
        else:
            return 'high'
    
    def generate_asset_allocation_recommendations(self) -> Dict:
        """
        Generate asset allocation recommendations based on risk assessment
        
        Returns:
            Dict: Asset allocation recommendations
        """
        if not self.financial_data or not self.risk_profile:
            return {'error': 'Insufficient data for recommendations'}
        
        # Calculate current risk scores
        risk_scores = self.calculate_all_risks()
        total_risk = risk_scores['total_risk_score']
        risk_level = self.get_risk_level(total_risk)
        
        # Base allocations by risk level
        if risk_level == 'low':
            base_allocation = {
                'stocks': 30,
                'bonds': 50,
                'cash': 15,
                'real_estate': 5
            }
        elif risk_level == 'moderate':
            base_allocation = {
                'stocks': 60,
                'bonds': 30,
                'cash': 5,
                'real_estate': 5
            }
        else:  # high risk tolerance
            base_allocation = {
                'stocks': 80,
                'bonds': 15,
                'cash': 3,
                'real_estate': 2
            }
        
        # Adjust based on age and time horizon
        if self.risk_profile.age:
            # Rule of thumb: bond allocation = age
            bond_target = min(self.risk_profile.age, 70)
            stock_target = 100 - bond_target
            
            # Blend with risk-based allocation
            base_allocation['bonds'] = (base_allocation['bonds'] + bond_target) / 2
            base_allocation['stocks'] = (base_allocation['stocks'] + stock_target) / 2
        
        # Adjust for specific risks
        if risk_scores['liquidity_risk_score'] > 7:
            # Increase cash allocation for liquidity risk
            base_allocation['cash'] += 5
            base_allocation['stocks'] -= 3
            base_allocation['bonds'] -= 2
        
        if risk_scores['inflation_risk_score'] > 7:
            # Increase real estate and stocks for inflation protection
            base_allocation['real_estate'] += 3
            base_allocation['stocks'] += 2
            base_allocation['cash'] -= 3
            base_allocation['bonds'] -= 2
        
        # Normalize to 100%
        total = sum(base_allocation.values())
        normalized_allocation = {
            asset: round(allocation / total * 100, 1)
            for asset, allocation in base_allocation.items()
        }
        
        return {
            'recommended_allocation': normalized_allocation,
            'risk_level': risk_level,
            'total_risk_score': total_risk,
            'rationale': self._generate_allocation_rationale(risk_scores, normalized_allocation)
        }
    
    def _generate_allocation_rationale(self, risk_scores: Dict, allocation: Dict) -> List[str]:
        """
        Generate rationale for asset allocation recommendations
        
        Args:
            risk_scores: Dictionary of risk scores
            allocation: Recommended allocation
            
        Returns:
            List[str]: List of rationale statements
        """
        rationale = []
        
        # Overall risk level rationale
        total_risk = risk_scores['total_risk_score']
        if total_risk <= 3:
            rationale.append("Conservative allocation recommended due to low overall risk tolerance")
        elif total_risk <= 7:
            rationale.append("Balanced allocation recommended for moderate risk profile")
        else:
            rationale.append("Growth-oriented allocation suitable for higher risk tolerance")
        
        # Specific risk adjustments
        if risk_scores['liquidity_risk_score'] > 7:
            rationale.append(f"Increased cash allocation ({allocation['cash']}%) to address liquidity concerns")
        
        if risk_scores['credit_risk_score'] > 7:
            rationale.append("Conservative approach recommended due to high debt levels")
        
        if risk_scores['inflation_risk_score'] > 7:
            rationale.append(f"Increased equity and real estate allocation to combat inflation risk")
        
        if risk_scores['protection_risk_score'] > 7:
            rationale.append("Consider increasing insurance coverage before aggressive investing")
        
        return rationale
    
    def generate_risk_mitigation_strategies(self) -> Dict[str, List[str]]:
        """
        Generate specific risk mitigation strategies
        
        Returns:
            Dict[str, List[str]]: Risk mitigation strategies by category
        """
        risk_scores = self.calculate_all_risks()
        strategies = {}
        
        # Liquidity risk strategies
        if risk_scores['liquidity_risk_score'] > 5:
            strategies['liquidity'] = [
                "Build emergency fund to cover 3-6 months of expenses",
                "Consider high-yield savings account for emergency fund",
                "Reduce discretionary spending to improve cash flow",
                "Consider side income sources for additional cash flow"
            ]
        
        # Credit risk strategies
        if risk_scores['credit_risk_score'] > 5:
            strategies['credit'] = [
                "Focus on debt reduction, starting with highest interest rates",
                "Consider debt consolidation if beneficial",
                "Avoid taking on additional debt",
                "Improve credit score through timely payments"
            ]
        
        # Market risk strategies
        if risk_scores['market_risk_score'] > 5:
            strategies['market'] = [
                "Diversify investment portfolio across asset classes",
                "Consider dollar-cost averaging for regular investments",
                "Review and rebalance portfolio regularly",
                "Avoid emotional investment decisions"
            ]
        
        # Inflation risk strategies
        if risk_scores['inflation_risk_score'] > 5:
            strategies['inflation'] = [
                "Consider inflation-protected securities (TIPS)",
                "Invest in real assets like real estate or commodities",
                "Maintain some equity exposure for long-term growth",
                "Review and adjust investment strategy regularly"
            ]
        
        # Protection risk strategies
        if risk_scores['protection_risk_score'] > 5:
            strategies['protection'] = [
                "Review and increase life insurance coverage",
                "Consider disability insurance for income protection",
                "Ensure adequate health insurance coverage",
                "Review beneficiaries on all accounts and policies"
            ]
        
        return strategies

