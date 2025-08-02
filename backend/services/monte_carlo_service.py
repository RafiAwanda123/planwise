"""
Monte Carlo Simulation Service for portfolio projections and risk analysis
Implements actuarial models for financial planning
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from scipy import stats
import json

class MonteCarloService:
    """
    Monte Carlo simulation service for financial portfolio analysis
    Implements Value at Risk (VaR) and Expected Shortfall calculations
    """
    
    def __init__(self):
        """Initialize Monte Carlo service"""
        self.random_seed = 42  # For reproducible results
        np.random.seed(self.random_seed)
    
    def run_simulation(self, 
                      initial_value: float,
                      expected_return: float,
                      volatility: float,
                      time_horizon: int,
                      iterations: int = 10000,
                      monthly_contribution: float = 0.0) -> Dict:
        """
        Run Monte Carlo simulation for portfolio projections
        
        Args:
            initial_value: Initial portfolio value
            expected_return: Expected annual return (as decimal, e.g., 0.07 for 7%)
            volatility: Annual volatility (as decimal, e.g., 0.15 for 15%)
            time_horizon: Time horizon in years
            iterations: Number of simulation iterations
            monthly_contribution: Monthly contribution amount
            
        Returns:
            Dict: Simulation results including VaR, expected value, and distributions
        """
        # Convert annual parameters to monthly
        monthly_return = expected_return / 12
        monthly_volatility = volatility / np.sqrt(12)
        total_months = time_horizon * 12
        
        # Initialize results array
        final_values = np.zeros(iterations)
        yearly_projections = []
        
        # Run simulations
        for i in range(iterations):
            portfolio_value = initial_value
            yearly_values = [initial_value]
            
            for month in range(total_months):
                # Generate random return for this month
                monthly_random_return = np.random.normal(monthly_return, monthly_volatility)
                
                # Update portfolio value
                portfolio_value = portfolio_value * (1 + monthly_random_return) + monthly_contribution
                
                # Store yearly values
                if (month + 1) % 12 == 0:
                    yearly_values.append(portfolio_value)
            
            final_values[i] = portfolio_value
            
            # Store first simulation's yearly progression for visualization
            if i == 0:
                yearly_projections = yearly_values
        
        # Calculate statistics
        results = self._calculate_simulation_statistics(
            final_values, initial_value, yearly_projections, time_horizon
        )
        
        return results
    
    def _calculate_simulation_statistics(self, 
                                       final_values: np.ndarray,
                                       initial_value: float,
                                       yearly_projections: List[float],
                                       time_horizon: int) -> Dict:
        """
        Calculate comprehensive statistics from simulation results
        
        Args:
            final_values: Array of final portfolio values from all simulations
            initial_value: Initial portfolio value
            yearly_projections: Yearly progression from first simulation
            time_horizon: Time horizon in years
            
        Returns:
            Dict: Comprehensive simulation statistics
        """
        # Basic statistics
        mean_final_value = np.mean(final_values)
        median_final_value = np.median(final_values)
        std_final_value = np.std(final_values)
        
        # Percentiles for risk analysis
        percentiles = {
            '1': np.percentile(final_values, 1),
            '5': np.percentile(final_values, 5),
            '10': np.percentile(final_values, 10),
            '25': np.percentile(final_values, 25),
            '50': np.percentile(final_values, 50),
            '75': np.percentile(final_values, 75),
            '90': np.percentile(final_values, 90),
            '95': np.percentile(final_values, 95),
            '99': np.percentile(final_values, 99)
        }
        
        # Value at Risk calculations
        var_95 = initial_value - percentiles['5']  # 95% VaR
        var_99 = initial_value - percentiles['1']  # 99% VaR
        
        # Expected Shortfall (Conditional VaR)
        var_5_threshold = percentiles['5']
        losses_beyond_var = final_values[final_values <= var_5_threshold]
        expected_shortfall = np.mean(losses_beyond_var) if len(losses_beyond_var) > 0 else 0
        
        # Success probability (probability of positive returns)
        success_probability = (np.sum(final_values > initial_value) / len(final_values)) * 100
        
        # Maximum drawdown calculation
        max_drawdown = self._calculate_max_drawdown(yearly_projections)
        
        # Return statistics
        total_return = (mean_final_value - initial_value) / initial_value
        annualized_return = (mean_final_value / initial_value) ** (1/time_horizon) - 1
        
        # Risk-adjusted metrics
        sharpe_ratio = self._calculate_sharpe_ratio(final_values, initial_value, time_horizon)
        
        # Distribution analysis
        skewness = stats.skew(final_values)
        kurtosis = stats.kurtosis(final_values)
        
        return {
            'final_values': final_values.tolist(),
            'expected_value': mean_final_value,
            'median_value': median_final_value,
            'standard_deviation': std_final_value,
            'var_95': var_95,
            'var_99': var_99,
            'expected_shortfall': expected_shortfall,
            'success_probability': success_probability,
            'percentiles': percentiles,
            'yearly_projections': yearly_projections,
            'statistics': {
                'total_return': total_return,
                'annualized_return': annualized_return,
                'max_drawdown': max_drawdown,
                'sharpe_ratio': sharpe_ratio,
                'skewness': skewness,
                'kurtosis': kurtosis,
                'return_volatility': std_final_value / initial_value
            }
        }
    
    def _calculate_max_drawdown(self, values: List[float]) -> float:
        """
        Calculate maximum drawdown from a series of values
        
        Args:
            values: List of portfolio values over time
            
        Returns:
            float: Maximum drawdown as a percentage
        """
        if len(values) < 2:
            return 0.0
        
        peak = values[0]
        max_drawdown = 0.0
        
        for value in values[1:]:
            if value > peak:
                peak = value
            else:
                drawdown = (peak - value) / peak
                max_drawdown = max(max_drawdown, drawdown)
        
        return max_drawdown * 100  # Return as percentage
    
    def _calculate_sharpe_ratio(self, 
                               final_values: np.ndarray,
                               initial_value: float,
                               time_horizon: int,
                               risk_free_rate: float = 0.02) -> float:
        """
        Calculate Sharpe ratio for the simulation
        
        Args:
            final_values: Array of final portfolio values
            initial_value: Initial portfolio value
            time_horizon: Time horizon in years
            risk_free_rate: Risk-free rate (default 2%)
            
        Returns:
            float: Sharpe ratio
        """
        # Calculate returns
        returns = (final_values / initial_value) ** (1/time_horizon) - 1
        
        # Calculate excess return
        excess_return = np.mean(returns) - risk_free_rate
        
        # Calculate return volatility
        return_volatility = np.std(returns)
        
        # Calculate Sharpe ratio
        if return_volatility == 0:
            return 0.0
        
        return excess_return / return_volatility
    
    def run_goal_based_simulation(self,
                                 initial_value: float,
                                 target_value: float,
                                 expected_return: float,
                                 volatility: float,
                                 time_horizon: int,
                                 monthly_contribution: float = 0.0,
                                 iterations: int = 10000) -> Dict:
        """
        Run goal-based Monte Carlo simulation
        
        Args:
            initial_value: Initial portfolio value
            target_value: Target goal value
            expected_return: Expected annual return
            volatility: Annual volatility
            time_horizon: Time horizon in years
            monthly_contribution: Monthly contribution
            iterations: Number of iterations
            
        Returns:
            Dict: Goal-based simulation results
        """
        # Run standard simulation
        results = self.run_simulation(
            initial_value, expected_return, volatility, 
            time_horizon, iterations, monthly_contribution
        )
        
        # Calculate goal-specific metrics
        final_values = np.array(results['final_values'])
        
        # Probability of reaching goal
        goal_success_probability = (np.sum(final_values >= target_value) / len(final_values)) * 100
        
        # Shortfall analysis
        shortfall_values = final_values[final_values < target_value]
        if len(shortfall_values) > 0:
            average_shortfall = target_value - np.mean(shortfall_values)
            worst_case_shortfall = target_value - np.min(shortfall_values)
        else:
            average_shortfall = 0
            worst_case_shortfall = 0
        
        # Required return for goal achievement
        required_return = self._calculate_required_return(
            initial_value, target_value, time_horizon, monthly_contribution
        )
        
        # Add goal-specific results
        results.update({
            'target_value': target_value,
            'goal_success_probability': goal_success_probability,
            'average_shortfall': average_shortfall,
            'worst_case_shortfall': worst_case_shortfall,
            'required_return': required_return,
            'goal_analysis': {
                'probability_ranges': self._calculate_probability_ranges(final_values, target_value),
                'contribution_sensitivity': self._analyze_contribution_sensitivity(
                    initial_value, target_value, expected_return, volatility, time_horizon
                )
            }
        })
        
        return results
    
    def _calculate_required_return(self,
                                  initial_value: float,
                                  target_value: float,
                                  time_horizon: int,
                                  monthly_contribution: float) -> float:
        """
        Calculate required return to achieve target value
        
        Args:
            initial_value: Initial portfolio value
            target_value: Target goal value
            time_horizon: Time horizon in years
            monthly_contribution: Monthly contribution
            
        Returns:
            float: Required annual return
        """
        if monthly_contribution == 0:
            # Simple compound growth
            return (target_value / initial_value) ** (1/time_horizon) - 1
        else:
            # With regular contributions - use iterative approach
            # This is a simplified calculation
            total_contributions = monthly_contribution * 12 * time_horizon
            adjusted_target = target_value - total_contributions
            return (adjusted_target / initial_value) ** (1/time_horizon) - 1
    
    def _calculate_probability_ranges(self, 
                                    final_values: np.ndarray,
                                    target_value: float) -> Dict:
        """
        Calculate probability ranges for different outcome levels
        
        Args:
            final_values: Array of final portfolio values
            target_value: Target goal value
            
        Returns:
            Dict: Probability ranges
        """
        total_simulations = len(final_values)
        
        return {
            'exceed_target_by_50%': (np.sum(final_values >= target_value * 1.5) / total_simulations) * 100,
            'exceed_target_by_25%': (np.sum(final_values >= target_value * 1.25) / total_simulations) * 100,
            'achieve_target': (np.sum(final_values >= target_value) / total_simulations) * 100,
            'within_25%_of_target': (np.sum(final_values >= target_value * 0.75) / total_simulations) * 100,
            'within_50%_of_target': (np.sum(final_values >= target_value * 0.5) / total_simulations) * 100
        }
    
    def _analyze_contribution_sensitivity(self,
                                        initial_value: float,
                                        target_value: float,
                                        expected_return: float,
                                        volatility: float,
                                        time_horizon: int) -> Dict:
        """
        Analyze sensitivity to different contribution levels
        
        Args:
            initial_value: Initial portfolio value
            target_value: Target goal value
            expected_return: Expected annual return
            volatility: Annual volatility
            time_horizon: Time horizon in years
            
        Returns:
            Dict: Contribution sensitivity analysis
        """
        contribution_levels = [0, 100, 250, 500, 1000, 2000]
        sensitivity_results = {}
        
        for contribution in contribution_levels:
            # Run quick simulation with fewer iterations for sensitivity
            results = self.run_goal_based_simulation(
                initial_value, target_value, expected_return, volatility,
                time_horizon, contribution, iterations=1000
            )
            
            sensitivity_results[f'monthly_{contribution}'] = {
                'success_probability': results['goal_success_probability'],
                'expected_value': results['expected_value']
            }
        
        return sensitivity_results
    
    def calculate_retirement_projections(self,
                                       current_age: int,
                                       retirement_age: int,
                                       current_savings: float,
                                       monthly_contribution: float,
                                       expected_return: float,
                                       volatility: float,
                                       inflation_rate: float = 0.03) -> Dict:
        """
        Calculate retirement-specific projections
        
        Args:
            current_age: Current age
            retirement_age: Target retirement age
            current_savings: Current retirement savings
            monthly_contribution: Monthly contribution
            expected_return: Expected annual return
            volatility: Annual volatility
            inflation_rate: Expected inflation rate
            
        Returns:
            Dict: Retirement projection results
        """
        time_horizon = retirement_age - current_age
        
        if time_horizon <= 0:
            return {'error': 'Invalid time horizon for retirement'}
        
        # Run simulation
        results = self.run_simulation(
            current_savings, expected_return, volatility,
            time_horizon, monthly_contribution=monthly_contribution
        )
        
        # Adjust for inflation
        inflation_factor = (1 + inflation_rate) ** time_horizon
        real_values = np.array(results['final_values']) / inflation_factor
        
        # Calculate retirement-specific metrics
        results.update({
            'retirement_analysis': {
                'nominal_expected_value': results['expected_value'],
                'real_expected_value': np.mean(real_values),
                'inflation_adjusted_percentiles': {
                    '25': np.percentile(real_values, 25),
                    '50': np.percentile(real_values, 50),
                    '75': np.percentile(real_values, 75),
                    '90': np.percentile(real_values, 90)
                },
                'withdrawal_rates': self._calculate_safe_withdrawal_rates(real_values)
            }
        })
        
        return results
    
    def _calculate_safe_withdrawal_rates(self, real_values: np.ndarray) -> Dict:
        """
        Calculate safe withdrawal rates based on simulation results
        
        Args:
            real_values: Inflation-adjusted final values
            
        Returns:
            Dict: Safe withdrawal rate analysis
        """
        withdrawal_rates = {}
        
        for percentile in [25, 50, 75, 90]:
            portfolio_value = np.percentile(real_values, percentile)
            
            # Calculate annual withdrawal amounts for different rates
            withdrawal_rates[f'percentile_{percentile}'] = {
                '3_percent': portfolio_value * 0.03,
                '4_percent': portfolio_value * 0.04,
                '5_percent': portfolio_value * 0.05
            }
        
        return withdrawal_rates

