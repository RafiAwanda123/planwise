# Plan Wise - Enterprise Risk Management System

A comprehensive web application for personal financial risk management, built with modern technologies and following ISO 31000:2018 framework principles.

## 🚀 Features

### Core Functionality
- **User Authentication**: Secure JWT-based authentication system
- **Financial Data Management**: Comprehensive input and tracking of income, expenses, assets, and debts
- **Risk Assessment Engine**: Advanced risk scoring system (0-10 scale) covering:
  - Liquidity Risk
  - Credit Risk
  - Market Risk
  - Inflation Risk
  - Protection Risk
- **Monte Carlo Simulation**: Portfolio projections with statistical modeling
- **Asset Allocation Recommendations**: Personalized investment suggestions
- **Goal Tracking**: Set and monitor financial objectives
- **Comprehensive Reports**: PDF generation and dashboard analytics

### Technical Features
- **Modern Frontend**: React with Tailwind CSS and shadcn/ui components
- **Robust Backend**: Flask with PostgreSQL database
- **Statistical Models**: Python-based risk engine and actuarial calculations
- **Containerized Deployment**: Docker and Docker Compose support
- **API Documentation**: RESTful API with comprehensive endpoints
- **Security**: CORS, JWT tokens, input validation, and error handling

## 🏗️ Architecture

```
erp-webapp/
├── backend/                 # Flask API server
│   ├── controllers/         # Request handlers
│   ├── models/             # Database models
│   ├── services/           # Business logic
│   ├── utils/              # Utility functions
│   ├── middlewares/        # Custom middleware
│   ├── routes/             # API routes
│   └── config/             # Configuration files
├── frontend/               # React web application
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── contexts/       # React contexts
│   │   ├── lib/           # Utility libraries
│   │   └── assets/        # Static assets
│   └── public/            # Public files
├── database/              # Database schemas and migrations
├── docs/                  # Documentation
└── scripts/               # Utility scripts
```

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask (Python 3.11)
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy
- **Authentication**: JWT (PyJWT)
- **Statistical Computing**: NumPy, SciPy, Pandas
- **Report Generation**: ReportLab, Matplotlib
- **API Documentation**: Flask-RESTX

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui
- **Charts**: Recharts
- **Routing**: React Router
- **State Management**: React Context

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx (for frontend)
- **Caching**: Redis (optional)
- **Process Management**: Gunicorn

## 📋 Prerequisites

### For Docker Installation (Recommended)
- Docker Engine 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum
- 10GB free disk space

### For Manual Installation
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Git

## 🚀 Quick Start with Docker

### 1. Clone the Repository
```bash
git clone <repository-url>
cd erp-webapp
```

### 2. Environment Setup
```bash
# Copy environment file
cp .env.example .env.production

# Edit environment variables (important for security)
nano .env.production
```

### 3. Build and Run
```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### 4. Access the Application
- **Frontend**: http://localhost
- **Backend API**: http://localhost:5000
- **API Documentation**: http://localhost:5000/api/docs
- **Database**: localhost:5432

### 5. Initial Setup
```bash
# Create database tables (if needed)
docker-compose exec backend python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

## 💻 Manual Installation

### Linux (Ubuntu/Debian)

#### 1. System Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3.11 python3.11-venv python3-pip nodejs npm postgresql postgresql-contrib git curl

# Install pnpm
npm install -g pnpm
```

#### 2. Database Setup
```bash
# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql << EOF
CREATE DATABASE erp_webapp;
CREATE USER erp_user WITH PASSWORD 'erp_password';
GRANT ALL PRIVILEGES ON DATABASE erp_webapp TO erp_user;
\q
EOF

# Import schema
psql -U erp_user -d erp_webapp -f database/schema.sql
```

#### 3. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://erp_user:erp_password@localhost:5432/erp_webapp"
export JWT_SECRET_KEY="your-secret-key"

# Run the application
python app.py
```

#### 4. Frontend Setup
```bash
# Open new terminal and navigate to frontend
cd frontend

# Install dependencies
pnpm install

# Set environment variables
echo "VITE_API_URL=http://localhost:5000/api" > .env.local

# Start development server
pnpm run dev
```

### Windows

#### 1. Prerequisites Installation
```powershell
# Install Chocolatey (if not installed)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install required software
choco install python311 nodejs postgresql git -y

# Install pnpm
npm install -g pnpm
```

#### 2. Database Setup
```powershell
# Start PostgreSQL service
net start postgresql-x64-15

# Create database (using pgAdmin or command line)
# Connect to PostgreSQL and run:
# CREATE DATABASE erp_webapp;
# CREATE USER erp_user WITH PASSWORD 'erp_password';
# GRANT ALL PRIVILEGES ON DATABASE erp_webapp TO erp_user;
```

#### 3. Backend Setup
```powershell
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
$env:DATABASE_URL="postgresql://erp_user:erp_password@localhost:5432/erp_webapp"
$env:JWT_SECRET_KEY="your-secret-key"

# Run the application
python app.py
```

#### 4. Frontend Setup
```powershell
# Open new PowerShell window and navigate to frontend
cd frontend

# Install dependencies
pnpm install

# Set environment variables
echo "VITE_API_URL=http://localhost:5000/api" > .env.local

# Start development server
pnpm run dev
```

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/erp_webapp

# Security
JWT_SECRET_KEY=your-super-secret-jwt-key
SECRET_KEY=your-flask-secret-key

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Optional
REDIS_URL=redis://localhost:6379/0
LOG_LEVEL=INFO
```

#### Frontend (.env.local)
```bash
VITE_API_URL=http://localhost:5000/api
```

### Database Configuration

The application uses PostgreSQL with the following default settings:
- **Database**: erp_webapp
- **User**: erp_user
- **Password**: erp_password
- **Host**: localhost
- **Port**: 5432

## 📊 API Documentation

### Authentication Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/profile` - Get user profile

### Financial Data Endpoints
- `GET /api/financial/data` - Get financial data
- `POST /api/financial/data` - Update financial data
- `GET /api/financial/summary` - Get financial summary
- `GET /api/financial/goals` - Get financial goals
- `POST /api/financial/goals` - Create financial goal

### Risk Assessment Endpoints
- `POST /api/risk/assess` - Run risk assessment
- `GET /api/risk/assessment` - Get latest assessment
- `GET /api/risk/history` - Get assessment history
- `POST /api/risk/simulations` - Run Monte Carlo simulation
- `GET /api/risk/simulations` - Get simulation results

### Report Endpoints
- `POST /api/reports/dashboard` - Generate dashboard report
- `POST /api/reports/pdf` - Generate PDF report
- `GET /api/reports/analytics` - Get analytics data

## 🧪 Testing

### Backend Tests
```bash
cd backend
source venv/bin/activate
python -m pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
pnpm test
```

### Integration Tests
```bash
# Start all services
docker-compose up -d

# Run integration tests
python scripts/integration_tests.py
```

## 🚀 Deployment

### Production Deployment with Docker

#### 1. Prepare Environment
```bash
# Copy production environment
cp .env.production .env

# Update security settings
nano .env
```

#### 2. Deploy
```bash
# Build and deploy
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

# Check status
docker-compose ps
```

#### 3. SSL Setup (Optional)
```bash
# Add SSL certificates
# Update nginx configuration
# Restart services
```

### Manual Production Deployment

#### 1. Backend (using Gunicorn)
```bash
cd backend
source venv/bin/activate
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

#### 2. Frontend (build and serve)
```bash
cd frontend
pnpm run build
# Serve dist/ folder with nginx or apache
```

## 🔒 Security Considerations

### Production Security Checklist
- [ ] Change all default passwords
- [ ] Use strong JWT secret keys
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Set up rate limiting
- [ ] Enable database encryption
- [ ] Regular security updates
- [ ] Monitor logs for suspicious activity

### Environment Security
```bash
# Generate secure keys
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Set proper file permissions
chmod 600 .env
chmod 600 .env.production
```

## 📈 Monitoring and Maintenance

### Health Checks
- **Backend**: `GET /health`
- **Database**: Built-in PostgreSQL health checks
- **Frontend**: Nginx status

### Logging
```bash
# View application logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Database logs
docker-compose logs -f database
```

### Backup
```bash
# Database backup
docker-compose exec database pg_dump -U erp_user erp_webapp > backup.sql

# Restore database
docker-compose exec -T database psql -U erp_user erp_webapp < backup.sql
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make changes and test
4. Submit a pull request

### Code Style
- **Python**: Follow PEP 8
- **JavaScript**: Use Prettier and ESLint
- **Commit Messages**: Use conventional commits

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

#### Database Connection Error
```bash
# Check PostgreSQL status
docker-compose ps database

# Restart database
docker-compose restart database
```

#### Frontend Build Issues
```bash
# Clear node modules and reinstall
cd frontend
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

#### Backend Import Errors
```bash
# Activate virtual environment
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Getting Help
- Check the [Issues](https://github.com/your-repo/issues) page
- Review the [Documentation](docs/)
- Contact support: support@yourcompany.com

## 🔄 Updates and Maintenance

### Regular Updates
```bash
# Update dependencies
cd backend && pip install -r requirements.txt --upgrade
cd frontend && pnpm update

# Update Docker images
docker-compose pull
docker-compose up -d --build
```

### Version History
- **v1.0.0** - Initial release with core features
- **v1.1.0** - Added Monte Carlo simulation
- **v1.2.0** - Enhanced reporting features

---

**Built with ❤️ for better financial risk management**

