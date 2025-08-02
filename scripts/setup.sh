#!/bin/bash

# ERP Webapp Setup Script for Linux
# This script automates the installation and setup process

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        error "This script should not be run as root"
    fi
}

# Check system requirements
check_system() {
    log "Checking system requirements..."
    
    # Check OS
    if [[ "$OSTYPE" != "linux-gnu"* ]]; then
        error "This script is designed for Linux systems"
    fi
    
    # Check available memory (minimum 2GB)
    MEMORY=$(free -m | awk 'NR==2{printf "%.0f", $2/1024}')
    if [[ $MEMORY -lt 2 ]]; then
        warn "System has less than 2GB RAM. Application may run slowly."
    fi
    
    # Check disk space (minimum 5GB)
    DISK_SPACE=$(df -BG . | awk 'NR==2{print $4}' | sed 's/G//')
    if [[ $DISK_SPACE -lt 5 ]]; then
        error "Insufficient disk space. At least 5GB required."
    fi
    
    log "System requirements check passed"
}

# Install system dependencies
install_dependencies() {
    log "Installing system dependencies..."
    
    # Update package list
    sudo apt update
    
    # Install required packages
    sudo apt install -y \
        python3.11 \
        python3.11-venv \
        python3-pip \
        nodejs \
        npm \
        postgresql \
        postgresql-contrib \
        git \
        curl \
        build-essential \
        libpq-dev \
        redis-server
    
    # Install pnpm
    sudo npm install -g pnpm
    
    log "System dependencies installed successfully"
}

# Setup PostgreSQL database
setup_database() {
    log "Setting up PostgreSQL database..."
    
    # Start PostgreSQL service
    sudo systemctl start postgresql
    sudo systemctl enable postgresql
    
    # Create database and user
    sudo -u postgres psql << EOF
CREATE DATABASE erp_webapp;
CREATE USER erp_user WITH PASSWORD 'erp_password';
GRANT ALL PRIVILEGES ON DATABASE erp_webapp TO erp_user;
ALTER USER erp_user CREATEDB;
\q
EOF
    
    # Import schema
    if [[ -f "database/schema.sql" ]]; then
        PGPASSWORD=erp_password psql -h localhost -U erp_user -d erp_webapp -f database/schema.sql
        log "Database schema imported successfully"
    else
        warn "Database schema file not found. You may need to create tables manually."
    fi
    
    log "PostgreSQL database setup completed"
}

# Setup Redis
setup_redis() {
    log "Setting up Redis..."
    
    # Start Redis service
    sudo systemctl start redis-server
    sudo systemctl enable redis-server
    
    # Test Redis connection
    if redis-cli ping | grep -q "PONG"; then
        log "Redis setup completed successfully"
    else
        warn "Redis setup may have issues"
    fi
}

# Setup backend
setup_backend() {
    log "Setting up backend..."
    
    cd backend
    
    # Create virtual environment
    python3.11 -m venv venv
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install Python dependencies
    pip install -r requirements.txt
    
    # Create environment file
    if [[ ! -f ".env" ]]; then
        cat > .env << EOF
DATABASE_URL=postgresql://erp_user:erp_password@localhost:5432/erp_webapp
JWT_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
FLASK_ENV=development
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
REDIS_URL=redis://localhost:6379/0
LOG_LEVEL=INFO
EOF
        log "Backend environment file created"
    fi
    
    # Test database connection
    python3 -c "
import os
import sys
sys.path.append('.')
from config.database import db
from app import create_app

app = create_app()
with app.app_context():
    try:
        db.create_all()
        print('Database connection successful')
    except Exception as e:
        print(f'Database connection failed: {e}')
        sys.exit(1)
"
    
    cd ..
    log "Backend setup completed"
}

# Setup frontend
setup_frontend() {
    log "Setting up frontend..."
    
    cd frontend
    
    # Install dependencies
    pnpm install
    
    # Create environment file
    if [[ ! -f ".env.local" ]]; then
        cat > .env.local << EOF
VITE_API_URL=http://localhost:5000/api
EOF
        log "Frontend environment file created"
    fi
    
    # Test build
    pnpm run build
    
    cd ..
    log "Frontend setup completed"
}

# Create systemd services
create_services() {
    log "Creating systemd services..."
    
    # Backend service
    sudo tee /etc/systemd/system/erp-backend.service > /dev/null << EOF
[Unit]
Description=ERP Webapp Backend
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)/backend
Environment=PATH=$(pwd)/backend/venv/bin
ExecStart=$(pwd)/backend/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    
    # Frontend service (using serve)
    sudo tee /etc/systemd/system/erp-frontend.service > /dev/null << EOF
[Unit]
Description=ERP Webapp Frontend
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)/frontend
ExecStart=/usr/bin/npx serve -s dist -l 3000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    
    # Reload systemd
    sudo systemctl daemon-reload
    
    log "Systemd services created"
}

# Setup nginx (optional)
setup_nginx() {
    read -p "Do you want to setup Nginx reverse proxy? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log "Setting up Nginx..."
        
        # Install nginx
        sudo apt install -y nginx
        
        # Create nginx configuration
        sudo tee /etc/nginx/sites-available/erp-webapp > /dev/null << EOF
server {
    listen 80;
    server_name localhost;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:5000/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF
        
        # Enable site
        sudo ln -sf /etc/nginx/sites-available/erp-webapp /etc/nginx/sites-enabled/
        sudo rm -f /etc/nginx/sites-enabled/default
        
        # Test nginx configuration
        sudo nginx -t
        
        # Start nginx
        sudo systemctl start nginx
        sudo systemctl enable nginx
        
        log "Nginx setup completed"
    fi
}

# Start services
start_services() {
    log "Starting services..."
    
    # Start and enable services
    sudo systemctl start erp-backend
    sudo systemctl enable erp-backend
    
    sudo systemctl start erp-frontend
    sudo systemctl enable erp-frontend
    
    # Wait a moment for services to start
    sleep 5
    
    # Check service status
    if systemctl is-active --quiet erp-backend; then
        log "Backend service is running"
    else
        error "Backend service failed to start"
    fi
    
    if systemctl is-active --quiet erp-frontend; then
        log "Frontend service is running"
    else
        error "Frontend service failed to start"
    fi
    
    log "All services started successfully"
}

# Test installation
test_installation() {
    log "Testing installation..."
    
    # Test backend health
    if curl -f http://localhost:5000/health > /dev/null 2>&1; then
        log "Backend health check passed"
    else
        error "Backend health check failed"
    fi
    
    # Test frontend
    if curl -f http://localhost:3000 > /dev/null 2>&1; then
        log "Frontend accessibility check passed"
    else
        error "Frontend accessibility check failed"
    fi
    
    log "Installation test completed successfully"
}

# Print final instructions
print_instructions() {
    echo
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  ERP Webapp Setup Completed!${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo
    echo -e "${GREEN}Application URLs:${NC}"
    echo "  Frontend: http://localhost:3000"
    echo "  Backend API: http://localhost:5000"
    echo "  API Documentation: http://localhost:5000/api/docs"
    echo
    echo -e "${GREEN}Database Information:${NC}"
    echo "  Host: localhost"
    echo "  Port: 5432"
    echo "  Database: erp_webapp"
    echo "  Username: erp_user"
    echo "  Password: erp_password"
    echo
    echo -e "${GREEN}Service Management:${NC}"
    echo "  Start backend: sudo systemctl start erp-backend"
    echo "  Stop backend: sudo systemctl stop erp-backend"
    echo "  Start frontend: sudo systemctl start erp-frontend"
    echo "  Stop frontend: sudo systemctl stop erp-frontend"
    echo "  View logs: sudo journalctl -u erp-backend -f"
    echo
    echo -e "${GREEN}Development Commands:${NC}"
    echo "  Backend dev: cd backend && source venv/bin/activate && python app.py"
    echo "  Frontend dev: cd frontend && pnpm run dev"
    echo
    echo -e "${YELLOW}Next Steps:${NC}"
    echo "1. Visit http://localhost:3000 to access the application"
    echo "2. Create your first user account"
    echo "3. Input your financial data"
    echo "4. Run risk assessment"
    echo "5. Generate reports"
    echo
    echo -e "${YELLOW}For production deployment:${NC}"
    echo "1. Update environment variables in backend/.env"
    echo "2. Configure SSL certificates"
    echo "3. Set up proper firewall rules"
    echo "4. Configure backup procedures"
    echo
}

# Main execution
main() {
    echo -e "${BLUE}ERP Webapp Setup Script${NC}"
    echo -e "${BLUE}========================${NC}"
    echo
    
    check_root
    check_system
    install_dependencies
    setup_database
    setup_redis
    setup_backend
    setup_frontend
    create_services
    setup_nginx
    start_services
    test_installation
    print_instructions
    
    log "Setup completed successfully!"
}

# Run main function
main "$@"

