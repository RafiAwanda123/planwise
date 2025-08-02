-- ERP Webapp Database Schema
-- PostgreSQL Database Schema for Enterprise Risk Management

-- Create database (run this separately)
-- CREATE DATABASE erp_db;

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Risk profiles table
CREATE TABLE risk_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    risk_tolerance VARCHAR(20) CHECK (risk_tolerance IN ('conservative', 'moderate', 'aggressive')),
    investment_experience VARCHAR(20) CHECK (investment_experience IN ('beginner', 'intermediate', 'advanced')),
    time_horizon INTEGER, -- in years
    age INTEGER,
    employment_status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Financial data table
CREATE TABLE financial_data (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    monthly_income DECIMAL(15,2) NOT NULL,
    monthly_expenses DECIMAL(15,2) NOT NULL,
    total_assets DECIMAL(15,2) DEFAULT 0,
    total_debt DECIMAL(15,2) DEFAULT 0,
    emergency_fund DECIMAL(15,2) DEFAULT 0,
    insurance_coverage DECIMAL(15,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Asset allocation table
CREATE TABLE asset_allocations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    asset_type VARCHAR(50) NOT NULL, -- stocks, bonds, cash, real_estate, etc.
    current_amount DECIMAL(15,2) DEFAULT 0,
    target_percentage DECIMAL(5,2) DEFAULT 0,
    recommended_percentage DECIMAL(5,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Financial goals table
CREATE TABLE financial_goals (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    goal_name VARCHAR(255) NOT NULL,
    target_amount DECIMAL(15,2) NOT NULL,
    current_amount DECIMAL(15,2) DEFAULT 0,
    target_date DATE,
    priority VARCHAR(20) CHECK (priority IN ('low', 'medium', 'high')),
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'completed', 'paused')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Risk assessments table
CREATE TABLE risk_assessments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    liquidity_risk_score DECIMAL(3,1) DEFAULT 0,
    credit_risk_score DECIMAL(3,1) DEFAULT 0,
    market_risk_score DECIMAL(3,1) DEFAULT 0,
    inflation_risk_score DECIMAL(3,1) DEFAULT 0,
    protection_risk_score DECIMAL(3,1) DEFAULT 0,
    total_risk_score DECIMAL(3,1) DEFAULT 0,
    risk_level VARCHAR(20) CHECK (risk_level IN ('low', 'moderate', 'high')),
    assessment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Monte Carlo simulations table
CREATE TABLE monte_carlo_simulations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    simulation_name VARCHAR(255),
    initial_portfolio_value DECIMAL(15,2),
    expected_return DECIMAL(5,4),
    volatility DECIMAL(5,4),
    time_horizon INTEGER, -- in years
    iterations INTEGER DEFAULT 10000,
    success_probability DECIMAL(5,2),
    var_95 DECIMAL(15,2), -- Value at Risk 95%
    var_99 DECIMAL(15,2), -- Value at Risk 99%
    expected_value DECIMAL(15,2),
    simulation_results TEXT, -- JSON data
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Reports table
CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    report_type VARCHAR(50) NOT NULL, -- dashboard, pdf, detailed
    report_data TEXT, -- JSON data
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_path VARCHAR(500)
);

-- Create indexes for better performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_risk_profiles_user_id ON risk_profiles(user_id);
CREATE INDEX idx_financial_data_user_id ON financial_data(user_id);
CREATE INDEX idx_asset_allocations_user_id ON asset_allocations(user_id);
CREATE INDEX idx_financial_goals_user_id ON financial_goals(user_id);
CREATE INDEX idx_risk_assessments_user_id ON risk_assessments(user_id);
CREATE INDEX idx_monte_carlo_simulations_user_id ON monte_carlo_simulations(user_id);
CREATE INDEX idx_reports_user_id ON reports(user_id);

-- Create trigger for updating updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply triggers to tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_risk_profiles_updated_at BEFORE UPDATE ON risk_profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_financial_data_updated_at BEFORE UPDATE ON financial_data FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_asset_allocations_updated_at BEFORE UPDATE ON asset_allocations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_financial_goals_updated_at BEFORE UPDATE ON financial_goals FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

