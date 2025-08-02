#!/bin/bash

# ERP Webapp Testing Script
# This script runs comprehensive tests for the application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging functions
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_TOTAL=0

# Test result tracking
test_result() {
    TESTS_TOTAL=$((TESTS_TOTAL + 1))
    if [ $1 -eq 0 ]; then
        TESTS_PASSED=$((TESTS_PASSED + 1))
        log "✓ $2"
    else
        TESTS_FAILED=$((TESTS_FAILED + 1))
        error "✗ $2"
    fi
}

# Test database connection
test_database() {
    log "Testing database connection..."
    
    # Test PostgreSQL connection
    if PGPASSWORD=erp_password psql -h localhost -U erp_user -d erp_webapp -c "SELECT 1;" > /dev/null 2>&1; then
        test_result 0 "Database connection"
    else
        test_result 1 "Database connection"
    fi
    
    # Test Redis connection
    if redis-cli ping | grep -q "PONG" 2>/dev/null; then
        test_result 0 "Redis connection"
    else
        test_result 1 "Redis connection"
    fi
}

# Test backend
test_backend() {
    log "Testing backend..."
    
    cd backend
    source venv/bin/activate
    
    # Test Python imports
    if python -c "
import sys
sys.path.append('.')
try:
    from app import create_app
    from models import db
    from services.risk_engine import RiskEngine
    from services.monte_carlo_service import MonteCarloService
    from services.report_service import ReportService
    print('All imports successful')
except ImportError as e:
    print(f'Import error: {e}')
    sys.exit(1)
" > /dev/null 2>&1; then
        test_result 0 "Backend imports"
    else
        test_result 1 "Backend imports"
    fi
    
    # Test Flask app creation
    if python -c "
import sys
sys.path.append('.')
from app import create_app
app = create_app()
print('Flask app created successfully')
" > /dev/null 2>&1; then
        test_result 0 "Flask app creation"
    else
        test_result 1 "Flask app creation"
    fi
    
    # Start backend in background for API tests
    python app.py &
    BACKEND_PID=$!
    sleep 5
    
    # Test health endpoint
    if curl -f http://localhost:5000/health > /dev/null 2>&1; then
        test_result 0 "Backend health endpoint"
    else
        test_result 1 "Backend health endpoint"
    fi
    
    # Test API info endpoint
    if curl -f http://localhost:5000/api > /dev/null 2>&1; then
        test_result 0 "API info endpoint"
    else
        test_result 1 "API info endpoint"
    fi
    
    # Test user registration
    REGISTER_RESPONSE=$(curl -s -X POST http://localhost:5000/api/auth/register \
        -H "Content-Type: application/json" \
        -d '{
            "email": "test@example.com",
            "password": "testpassword123",
            "first_name": "Test",
            "last_name": "User"
        }')
    
    if echo "$REGISTER_RESPONSE" | grep -q '"success": true'; then
        test_result 0 "User registration"
        
        # Extract token for further tests
        TOKEN=$(echo "$REGISTER_RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('success') and 'tokens' in data.get('data', {}):
    print(data['data']['tokens']['access_token'])
")
        
        # Test authenticated endpoint
        if [ -n "$TOKEN" ]; then
            if curl -f -H "Authorization: Bearer $TOKEN" http://localhost:5000/api/auth/profile > /dev/null 2>&1; then
                test_result 0 "Authenticated API access"
            else
                test_result 1 "Authenticated API access"
            fi
        fi
    else
        test_result 1 "User registration"
    fi
    
    # Stop backend
    kill $BACKEND_PID 2>/dev/null || true
    wait $BACKEND_PID 2>/dev/null || true
    
    cd ..
}

# Test frontend
test_frontend() {
    log "Testing frontend..."
    
    cd frontend
    
    # Test dependencies
    if pnpm list > /dev/null 2>&1; then
        test_result 0 "Frontend dependencies"
    else
        test_result 1 "Frontend dependencies"
    fi
    
    # Test build
    if pnpm run build > /dev/null 2>&1; then
        test_result 0 "Frontend build"
    else
        test_result 1 "Frontend build"
    fi
    
    # Test if built files exist
    if [ -d "dist" ] && [ -f "dist/index.html" ]; then
        test_result 0 "Build output files"
    else
        test_result 1 "Build output files"
    fi
    
    # Start frontend server in background
    pnpm run preview --port 3000 &
    FRONTEND_PID=$!
    sleep 5
    
    # Test frontend accessibility
    if curl -f http://localhost:3000 > /dev/null 2>&1; then
        test_result 0 "Frontend accessibility"
    else
        test_result 1 "Frontend accessibility"
    fi
    
    # Stop frontend
    kill $FRONTEND_PID 2>/dev/null || true
    wait $FRONTEND_PID 2>/dev/null || true
    
    cd ..
}

# Test Docker setup
test_docker() {
    log "Testing Docker setup..."
    
    # Check if Docker is available
    if command -v docker > /dev/null 2>&1; then
        # Test Docker Compose file syntax
        if docker-compose config > /dev/null 2>&1; then
            test_result 0 "Docker Compose configuration"
        else
            test_result 1 "Docker Compose configuration"
        fi
        
        # Test Dockerfile syntax (backend)
        if docker build -t erp-backend-test backend > /dev/null 2>&1; then
            test_result 0 "Backend Dockerfile"
            docker rmi erp-backend-test > /dev/null 2>&1 || true
        else
            test_result 1 "Backend Dockerfile"
        fi
        
        # Test Dockerfile syntax (frontend)
        if docker build -t erp-frontend-test frontend > /dev/null 2>&1; then
            test_result 0 "Frontend Dockerfile"
            docker rmi erp-frontend-test > /dev/null 2>&1 || true
        else
            test_result 1 "Frontend Dockerfile"
        fi
    else
        warn "Docker not available, skipping Docker tests"
    fi
}

# Test file structure
test_file_structure() {
    log "Testing file structure..."
    
    # Required files and directories
    REQUIRED_PATHS=(
        "backend/app.py"
        "backend/requirements.txt"
        "backend/Dockerfile"
        "backend/models"
        "backend/controllers"
        "backend/services"
        "backend/routes"
        "frontend/package.json"
        "frontend/Dockerfile"
        "frontend/src/App.jsx"
        "frontend/src/components"
        "database/schema.sql"
        "docker-compose.yml"
        "README.md"
        "docs/API_DOCUMENTATION.md"
        "scripts/setup.sh"
        "scripts/setup.ps1"
    )
    
    for path in "${REQUIRED_PATHS[@]}"; do
        if [ -e "$path" ]; then
            test_result 0 "File/directory exists: $path"
        else
            test_result 1 "File/directory exists: $path"
        fi
    done
}

# Test configuration files
test_configuration() {
    log "Testing configuration files..."
    
    # Test environment files
    if [ -f ".env.example" ]; then
        test_result 0 "Environment example file exists"
    else
        test_result 1 "Environment example file exists"
    fi
    
    # Test package.json validity
    if cd frontend && node -e "JSON.parse(require('fs').readFileSync('package.json', 'utf8'))" 2>/dev/null; then
        test_result 0 "Frontend package.json validity"
    else
        test_result 1 "Frontend package.json validity"
    fi
    cd ..
    
    # Test requirements.txt
    if [ -f "backend/requirements.txt" ] && [ -s "backend/requirements.txt" ]; then
        test_result 0 "Backend requirements.txt exists and not empty"
    else
        test_result 1 "Backend requirements.txt exists and not empty"
    fi
}

# Test security
test_security() {
    log "Testing security configurations..."
    
    # Check for hardcoded secrets in common files
    SECURITY_ISSUES=0
    
    # Check for common secret patterns
    if grep -r "password.*=" backend/ --include="*.py" | grep -v "password_hash" | grep -v "example" > /dev/null 2>&1; then
        SECURITY_ISSUES=$((SECURITY_ISSUES + 1))
        warn "Potential hardcoded passwords found in backend"
    fi
    
    if grep -r "secret.*=" backend/ --include="*.py" | grep -v "SECRET_KEY" | grep -v "example" > /dev/null 2>&1; then
        SECURITY_ISSUES=$((SECURITY_ISSUES + 1))
        warn "Potential hardcoded secrets found in backend"
    fi
    
    # Check for proper CORS configuration
    if grep -r "CORS" backend/ --include="*.py" > /dev/null 2>&1; then
        test_result 0 "CORS configuration present"
    else
        test_result 1 "CORS configuration present"
    fi
    
    if [ $SECURITY_ISSUES -eq 0 ]; then
        test_result 0 "No obvious security issues found"
    else
        test_result 1 "Security issues detected"
    fi
}

# Performance tests
test_performance() {
    log "Testing performance..."
    
    cd backend
    source venv/bin/activate
    
    # Test risk engine performance
    if python -c "
import time
import sys
sys.path.append('.')
from services.risk_engine import RiskEngine
from models.financial_data import FinancialData

# Mock financial data
class MockFinancialData:
    def __init__(self):
        self.monthly_income = 5000
        self.monthly_expenses = 3500
        self.monthly_surplus = 1500
        self.total_assets = 100000
        self.total_debt = 25000
        self.net_worth = 75000
        self.emergency_fund = 15000
        self.emergency_fund_months = 4.3
        self.insurance_coverage = 500000
        self.debt_to_income_ratio = 0.42

# Performance test
start_time = time.time()
engine = RiskEngine(MockFinancialData())
risks = engine.calculate_all_risks()
end_time = time.time()

if end_time - start_time < 1.0:  # Should complete in less than 1 second
    print('Risk engine performance test passed')
else:
    print('Risk engine performance test failed')
    sys.exit(1)
" > /dev/null 2>&1; then
        test_result 0 "Risk engine performance"
    else
        test_result 1 "Risk engine performance"
    fi
    
    cd ..
}

# Integration tests
test_integration() {
    log "Running integration tests..."
    
    # Start all services
    cd backend
    source venv/bin/activate
    python app.py &
    BACKEND_PID=$!
    cd ..
    
    cd frontend
    pnpm run preview --port 3000 &
    FRONTEND_PID=$!
    cd ..
    
    sleep 10
    
    # Test full user flow
    # 1. Register user
    REGISTER_RESPONSE=$(curl -s -X POST http://localhost:5000/api/auth/register \
        -H "Content-Type: application/json" \
        -d '{
            "email": "integration@test.com",
            "password": "testpass123",
            "first_name": "Integration",
            "last_name": "Test"
        }')
    
    if echo "$REGISTER_RESPONSE" | grep -q '"success": true'; then
        TOKEN=$(echo "$REGISTER_RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
if data.get('success') and 'tokens' in data.get('data', {}):
    print(data['data']['tokens']['access_token'])
")
        
        # 2. Update financial data
        FINANCIAL_RESPONSE=$(curl -s -X POST http://localhost:5000/api/financial/data \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $TOKEN" \
            -d '{
                "monthly_income": 5000,
                "monthly_expenses": 3500,
                "total_assets": 100000,
                "total_debt": 25000,
                "emergency_fund": 15000,
                "insurance_coverage": 500000
            }')
        
        if echo "$FINANCIAL_RESPONSE" | grep -q '"success": true'; then
            # 3. Run risk assessment
            RISK_RESPONSE=$(curl -s -X POST http://localhost:5000/api/risk/assess \
                -H "Authorization: Bearer $TOKEN")
            
            if echo "$RISK_RESPONSE" | grep -q '"success": true'; then
                test_result 0 "Full integration flow"
            else
                test_result 1 "Risk assessment in integration flow"
            fi
        else
            test_result 1 "Financial data update in integration flow"
        fi
    else
        test_result 1 "User registration in integration flow"
    fi
    
    # Cleanup
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    wait $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
}

# Print test summary
print_summary() {
    echo
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  Test Summary${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo
    echo -e "${GREEN}Tests Passed: $TESTS_PASSED${NC}"
    echo -e "${RED}Tests Failed: $TESTS_FAILED${NC}"
    echo -e "${BLUE}Total Tests: $TESTS_TOTAL${NC}"
    echo
    
    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "${GREEN}✓ All tests passed!${NC}"
        echo
        echo -e "${GREEN}The application is ready for deployment.${NC}"
        return 0
    else
        echo -e "${RED}✗ Some tests failed.${NC}"
        echo
        echo -e "${YELLOW}Please review the failed tests and fix the issues before deployment.${NC}"
        return 1
    fi
}

# Main execution
main() {
    echo -e "${BLUE}ERP Webapp Test Suite${NC}"
    echo -e "${BLUE}=====================${NC}"
    echo
    
    test_file_structure
    test_configuration
    test_database
    test_backend
    test_frontend
    test_docker
    test_security
    test_performance
    test_integration
    
    print_summary
}

# Run main function
main "$@"

