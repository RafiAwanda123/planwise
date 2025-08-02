# ERP Webapp Setup Script for Windows PowerShell
# This script automates the installation and setup process on Windows

param(
    [switch]$SkipDependencies,
    [switch]$SkipDatabase,
    [switch]$Help
)

# Colors for output
$Colors = @{
    Red = "Red"
    Green = "Green"
    Yellow = "Yellow"
    Blue = "Blue"
    White = "White"
}

# Logging functions
function Write-Log {
    param([string]$Message, [string]$Color = "Green")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] $Message" -ForegroundColor $Color
}

function Write-Warning {
    param([string]$Message)
    Write-Log "WARNING: $Message" -Color "Yellow"
}

function Write-Error {
    param([string]$Message)
    Write-Log "ERROR: $Message" -Color "Red"
    exit 1
}

# Help function
function Show-Help {
    Write-Host @"
ERP Webapp Setup Script for Windows

USAGE:
    .\setup.ps1 [OPTIONS]

OPTIONS:
    -SkipDependencies    Skip installation of system dependencies
    -SkipDatabase        Skip database setup
    -Help               Show this help message

EXAMPLES:
    .\setup.ps1                    # Full setup
    .\setup.ps1 -SkipDependencies  # Skip dependency installation
    .\setup.ps1 -Help              # Show help

REQUIREMENTS:
    - Windows 10/11 or Windows Server 2019+
    - PowerShell 5.1 or later
    - Administrator privileges for dependency installation
    - At least 4GB RAM and 10GB free disk space

"@
}

# Check if running as administrator
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Check system requirements
function Test-SystemRequirements {
    Write-Log "Checking system requirements..."
    
    # Check PowerShell version
    if ($PSVersionTable.PSVersion.Major -lt 5) {
        Write-Error "PowerShell 5.1 or later is required"
    }
    
    # Check available memory (minimum 4GB)
    $memory = (Get-CimInstance -ClassName Win32_ComputerSystem).TotalPhysicalMemory / 1GB
    if ($memory -lt 4) {
        Write-Warning "System has less than 4GB RAM. Application may run slowly."
    }
    
    # Check disk space (minimum 10GB)
    $disk = Get-CimInstance -ClassName Win32_LogicalDisk -Filter "DeviceID='C:'"
    $freeSpaceGB = $disk.FreeSpace / 1GB
    if ($freeSpaceGB -lt 10) {
        Write-Error "Insufficient disk space. At least 10GB required on C: drive."
    }
    
    Write-Log "System requirements check passed"
}

# Install Chocolatey
function Install-Chocolatey {
    if (!(Get-Command choco -ErrorAction SilentlyContinue)) {
        Write-Log "Installing Chocolatey..."
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        
        # Refresh environment variables
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        
        Write-Log "Chocolatey installed successfully"
    } else {
        Write-Log "Chocolatey is already installed"
    }
}

# Install system dependencies
function Install-Dependencies {
    if ($SkipDependencies) {
        Write-Log "Skipping dependency installation"
        return
    }
    
    Write-Log "Installing system dependencies..."
    
    # Check if running as administrator
    if (!(Test-Administrator)) {
        Write-Error "Administrator privileges required for dependency installation. Please run as Administrator or use -SkipDependencies flag."
    }
    
    Install-Chocolatey
    
    # Install required software
    $packages = @(
        "python311",
        "nodejs",
        "postgresql15",
        "git",
        "redis-64"
    )
    
    foreach ($package in $packages) {
        Write-Log "Installing $package..."
        choco install $package -y
    }
    
    # Install pnpm
    npm install -g pnpm
    
    # Refresh environment variables
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    
    Write-Log "System dependencies installed successfully"
}

# Setup PostgreSQL database
function Setup-Database {
    if ($SkipDatabase) {
        Write-Log "Skipping database setup"
        return
    }
    
    Write-Log "Setting up PostgreSQL database..."
    
    # Start PostgreSQL service
    Start-Service postgresql-x64-15 -ErrorAction SilentlyContinue
    Set-Service postgresql-x64-15 -StartupType Automatic
    
    # Wait for service to start
    Start-Sleep -Seconds 5
    
    # Create database and user
    $sqlCommands = @"
CREATE DATABASE erp_webapp;
CREATE USER erp_user WITH PASSWORD 'erp_password';
GRANT ALL PRIVILEGES ON DATABASE erp_webapp TO erp_user;
ALTER USER erp_user CREATEDB;
"@
    
    # Execute SQL commands
    try {
        $sqlCommands | & "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U postgres -d postgres
        Write-Log "Database and user created successfully"
    } catch {
        Write-Warning "Database setup may have failed. Please check PostgreSQL installation."
    }
    
    # Import schema if exists
    if (Test-Path "database\schema.sql") {
        try {
            & "C:\Program Files\PostgreSQL\15\bin\psql.exe" -U erp_user -d erp_webapp -f "database\schema.sql"
            Write-Log "Database schema imported successfully"
        } catch {
            Write-Warning "Schema import failed. You may need to import manually."
        }
    }
    
    Write-Log "PostgreSQL database setup completed"
}

# Setup Redis
function Setup-Redis {
    Write-Log "Setting up Redis..."
    
    # Start Redis service
    try {
        Start-Service Redis -ErrorAction SilentlyContinue
        Set-Service Redis -StartupType Automatic
        Write-Log "Redis service started successfully"
    } catch {
        Write-Warning "Redis service setup may have issues"
    }
}

# Setup backend
function Setup-Backend {
    Write-Log "Setting up backend..."
    
    Set-Location backend
    
    # Create virtual environment
    python -m venv venv
    
    # Activate virtual environment
    & "venv\Scripts\Activate.ps1"
    
    # Upgrade pip
    python -m pip install --upgrade pip
    
    # Install Python dependencies
    pip install -r requirements.txt
    
    # Create environment file
    if (!(Test-Path ".env")) {
        $envContent = @"
DATABASE_URL=postgresql://erp_user:erp_password@localhost:5432/erp_webapp
JWT_SECRET_KEY=$((New-Guid).ToString().Replace('-', ''))
SECRET_KEY=$((New-Guid).ToString().Replace('-', ''))
FLASK_ENV=development
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
REDIS_URL=redis://localhost:6379/0
LOG_LEVEL=INFO
"@
        $envContent | Out-File -FilePath ".env" -Encoding UTF8
        Write-Log "Backend environment file created"
    }
    
    # Test database connection
    try {
        python -c @"
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
"@
        Write-Log "Database connection test passed"
    } catch {
        Write-Warning "Database connection test failed"
    }
    
    Set-Location ..
    Write-Log "Backend setup completed"
}

# Setup frontend
function Setup-Frontend {
    Write-Log "Setting up frontend..."
    
    Set-Location frontend
    
    # Install dependencies
    pnpm install
    
    # Create environment file
    if (!(Test-Path ".env.local")) {
        "VITE_API_URL=http://localhost:5000/api" | Out-File -FilePath ".env.local" -Encoding UTF8
        Write-Log "Frontend environment file created"
    }
    
    # Test build
    try {
        pnpm run build
        Write-Log "Frontend build test passed"
    } catch {
        Write-Warning "Frontend build test failed"
    }
    
    Set-Location ..
    Write-Log "Frontend setup completed"
}

# Create Windows services
function Create-Services {
    Write-Log "Creating Windows services..."
    
    # Check if NSSM is available for service creation
    if (!(Get-Command nssm -ErrorAction SilentlyContinue)) {
        Write-Log "Installing NSSM for service management..."
        choco install nssm -y
    }
    
    # Create backend service
    $backendPath = (Resolve-Path "backend\venv\Scripts\python.exe").Path
    $backendScript = (Resolve-Path "backend\app.py").Path
    
    try {
        nssm install "ERP-Backend" $backendPath $backendScript
        nssm set "ERP-Backend" AppDirectory (Resolve-Path "backend").Path
        nssm set "ERP-Backend" DisplayName "ERP Webapp Backend"
        nssm set "ERP-Backend" Description "ERP Webapp Backend Service"
        nssm set "ERP-Backend" Start SERVICE_AUTO_START
        Write-Log "Backend service created"
    } catch {
        Write-Warning "Backend service creation failed"
    }
    
    # Create frontend service (using serve)
    try {
        $servePath = (Get-Command npx).Source
        nssm install "ERP-Frontend" $servePath "serve -s dist -l 3000"
        nssm set "ERP-Frontend" AppDirectory (Resolve-Path "frontend").Path
        nssm set "ERP-Frontend" DisplayName "ERP Webapp Frontend"
        nssm set "ERP-Frontend" Description "ERP Webapp Frontend Service"
        nssm set "ERP-Frontend" Start SERVICE_AUTO_START
        Write-Log "Frontend service created"
    } catch {
        Write-Warning "Frontend service creation failed"
    }
    
    Write-Log "Windows services created"
}

# Start services
function Start-Services {
    Write-Log "Starting services..."
    
    # Start backend service
    try {
        Start-Service "ERP-Backend"
        Write-Log "Backend service started"
    } catch {
        Write-Warning "Failed to start backend service"
    }
    
    # Start frontend service
    try {
        Start-Service "ERP-Frontend"
        Write-Log "Frontend service started"
    } catch {
        Write-Warning "Failed to start frontend service"
    }
    
    # Wait for services to start
    Start-Sleep -Seconds 10
    
    Write-Log "Services startup completed"
}

# Test installation
function Test-Installation {
    Write-Log "Testing installation..."
    
    # Test backend health
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:5000/health" -UseBasicParsing -TimeoutSec 10
        if ($response.StatusCode -eq 200) {
            Write-Log "Backend health check passed"
        } else {
            Write-Warning "Backend health check returned status: $($response.StatusCode)"
        }
    } catch {
        Write-Warning "Backend health check failed: $($_.Exception.Message)"
    }
    
    # Test frontend
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing -TimeoutSec 10
        if ($response.StatusCode -eq 200) {
            Write-Log "Frontend accessibility check passed"
        } else {
            Write-Warning "Frontend accessibility check returned status: $($response.StatusCode)"
        }
    } catch {
        Write-Warning "Frontend accessibility check failed: $($_.Exception.Message)"
    }
    
    Write-Log "Installation test completed"
}

# Print final instructions
function Show-FinalInstructions {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Blue
    Write-Host "  ERP Webapp Setup Completed!" -ForegroundColor Blue
    Write-Host "========================================" -ForegroundColor Blue
    Write-Host ""
    Write-Host "Application URLs:" -ForegroundColor Green
    Write-Host "  Frontend: http://localhost:3000"
    Write-Host "  Backend API: http://localhost:5000"
    Write-Host "  API Documentation: http://localhost:5000/api/docs"
    Write-Host ""
    Write-Host "Database Information:" -ForegroundColor Green
    Write-Host "  Host: localhost"
    Write-Host "  Port: 5432"
    Write-Host "  Database: erp_webapp"
    Write-Host "  Username: erp_user"
    Write-Host "  Password: erp_password"
    Write-Host ""
    Write-Host "Service Management:" -ForegroundColor Green
    Write-Host "  Start backend: Start-Service 'ERP-Backend'"
    Write-Host "  Stop backend: Stop-Service 'ERP-Backend'"
    Write-Host "  Start frontend: Start-Service 'ERP-Frontend'"
    Write-Host "  Stop frontend: Stop-Service 'ERP-Frontend'"
    Write-Host "  View services: Get-Service ERP-*"
    Write-Host ""
    Write-Host "Development Commands:" -ForegroundColor Green
    Write-Host "  Backend dev: cd backend; .\venv\Scripts\Activate.ps1; python app.py"
    Write-Host "  Frontend dev: cd frontend; pnpm run dev"
    Write-Host ""
    Write-Host "Next Steps:" -ForegroundColor Yellow
    Write-Host "1. Visit http://localhost:3000 to access the application"
    Write-Host "2. Create your first user account"
    Write-Host "3. Input your financial data"
    Write-Host "4. Run risk assessment"
    Write-Host "5. Generate reports"
    Write-Host ""
    Write-Host "For production deployment:" -ForegroundColor Yellow
    Write-Host "1. Update environment variables in backend\.env"
    Write-Host "2. Configure SSL certificates"
    Write-Host "3. Set up proper firewall rules"
    Write-Host "4. Configure backup procedures"
    Write-Host ""
}

# Main execution
function Main {
    if ($Help) {
        Show-Help
        return
    }
    
    Write-Host "ERP Webapp Setup Script for Windows" -ForegroundColor Blue
    Write-Host "====================================" -ForegroundColor Blue
    Write-Host ""
    
    try {
        Test-SystemRequirements
        Install-Dependencies
        Setup-Database
        Setup-Redis
        Setup-Backend
        Setup-Frontend
        Create-Services
        Start-Services
        Test-Installation
        Show-FinalInstructions
        
        Write-Log "Setup completed successfully!"
    } catch {
        Write-Error "Setup failed: $($_.Exception.Message)"
    }
}

# Run main function
Main

