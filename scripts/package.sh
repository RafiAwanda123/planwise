#!/bin/bash

# ERP Webapp Packaging Script
# This script creates a distributable package of the application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
PACKAGE_NAME="erp-webapp"
VERSION="1.0.0"
BUILD_DIR="build"
PACKAGE_DIR="$BUILD_DIR/$PACKAGE_NAME-$VERSION"
ARCHIVE_NAME="$PACKAGE_NAME-$VERSION.zip"

# Logging functions
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

# Clean previous builds
clean_build() {
    log "Cleaning previous builds..."
    rm -rf "$BUILD_DIR"
    mkdir -p "$PACKAGE_DIR"
}

# Copy source files
copy_source() {
    log "Copying source files..."
    
    # Backend files
    log "Copying backend files..."
    mkdir -p "$PACKAGE_DIR/backend"
    cp -r backend/* "$PACKAGE_DIR/backend/"
    
    # Remove virtual environment and cache
    rm -rf "$PACKAGE_DIR/backend/venv"
    rm -rf "$PACKAGE_DIR/backend/__pycache__"
    find "$PACKAGE_DIR/backend" -name "*.pyc" -delete
    find "$PACKAGE_DIR/backend" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    
    # Frontend files
    log "Copying frontend files..."
    mkdir -p "$PACKAGE_DIR/frontend"
    cp -r frontend/* "$PACKAGE_DIR/frontend/"
    
    # Remove node_modules and build artifacts
    rm -rf "$PACKAGE_DIR/frontend/node_modules"
    rm -rf "$PACKAGE_DIR/frontend/dist"
    rm -rf "$PACKAGE_DIR/frontend/.next"
    
    # Database files
    log "Copying database files..."
    mkdir -p "$PACKAGE_DIR/database"
    cp -r database/* "$PACKAGE_DIR/database/"
    
    # Documentation
    log "Copying documentation..."
    mkdir -p "$PACKAGE_DIR/docs"
    cp -r docs/* "$PACKAGE_DIR/docs/" 2>/dev/null || true
    
    # Scripts
    log "Copying scripts..."
    mkdir -p "$PACKAGE_DIR/scripts"
    cp -r scripts/* "$PACKAGE_DIR/scripts/"
    
    # Root files
    log "Copying root configuration files..."
    cp README.md "$PACKAGE_DIR/"
    cp docker-compose.yml "$PACKAGE_DIR/"
    cp .env.example "$PACKAGE_DIR/"
    cp .env.production "$PACKAGE_DIR/"
    
    # Copy license if exists
    [ -f LICENSE ] && cp LICENSE "$PACKAGE_DIR/"
    [ -f CHANGELOG.md ] && cp CHANGELOG.md "$PACKAGE_DIR/"
}

# Create installation guide
create_install_guide() {
    log "Creating installation guide..."
    
    cat > "$PACKAGE_DIR/INSTALL.md" << 'EOF'
# ERP Webapp Installation Guide

## Quick Start

### Option 1: Docker (Recommended)
```bash
# Extract the package
unzip erp-webapp-1.0.0.zip
cd erp-webapp-1.0.0

# Copy environment file
cp .env.production .env

# Start with Docker Compose
docker-compose up -d --build

# Access the application
# Frontend: http://localhost
# Backend: http://localhost:5000
```

### Option 2: Manual Installation

#### Linux
```bash
# Extract and navigate
unzip erp-webapp-1.0.0.zip
cd erp-webapp-1.0.0

# Run setup script
chmod +x scripts/setup.sh
./scripts/setup.sh

# Access the application
# Frontend: http://localhost:3000
# Backend: http://localhost:5000
```

#### Windows
```powershell
# Extract and navigate
Expand-Archive erp-webapp-1.0.0.zip
cd erp-webapp-1.0.0

# Run setup script (as Administrator)
PowerShell -ExecutionPolicy Bypass -File scripts\setup.ps1

# Access the application
# Frontend: http://localhost:3000
# Backend: http://localhost:5000
```

## System Requirements

### Minimum Requirements
- **OS**: Linux (Ubuntu 20.04+), Windows 10+, macOS 10.15+
- **RAM**: 4GB
- **Storage**: 10GB free space
- **Network**: Internet connection for initial setup

### For Docker Installation
- Docker Engine 20.10+
- Docker Compose 2.0+

### For Manual Installation
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 6+

## Configuration

### Environment Variables
Edit `.env` file to configure:
- Database connection
- JWT secrets
- CORS settings
- API endpoints

### Database Setup
The application will automatically create the required database tables on first run.

### Security
- Change default passwords
- Update JWT secret keys
- Configure CORS for your domain
- Enable HTTPS in production

## Troubleshooting

### Common Issues
1. **Port conflicts**: Change ports in docker-compose.yml or environment files
2. **Database connection**: Ensure PostgreSQL is running and accessible
3. **Permission errors**: Run setup scripts with appropriate permissions

### Getting Help
- Check the README.md for detailed documentation
- Review API documentation in docs/API_DOCUMENTATION.md
- Check logs: `docker-compose logs` or service logs

## Support
For support and questions, please refer to the documentation or contact support.
EOF
}

# Create version info
create_version_info() {
    log "Creating version information..."
    
    cat > "$PACKAGE_DIR/VERSION.txt" << EOF
ERP Webapp Version Information
==============================

Version: $VERSION
Build Date: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
Git Commit: $(git rev-parse HEAD 2>/dev/null || echo "N/A")
Build Environment: $(uname -a)

Components:
- Backend: Flask (Python 3.11)
- Frontend: React 18 + Vite
- Database: PostgreSQL 15
- Cache: Redis 6
- Containerization: Docker & Docker Compose

Features:
- User Authentication (JWT)
- Financial Data Management
- Risk Assessment Engine
- Monte Carlo Simulations
- Asset Allocation Recommendations
- Goal Tracking
- Comprehensive Reporting
- Dashboard Analytics

Security:
- CORS Protection
- Input Validation
- SQL Injection Prevention
- XSS Protection
- Rate Limiting
- Secure Headers

Documentation:
- README.md - Main documentation
- INSTALL.md - Installation guide
- docs/API_DOCUMENTATION.md - API reference
- scripts/ - Setup and utility scripts

Support:
- Email: support@yourcompany.com
- Documentation: https://docs.yourcompany.com
- Issues: https://github.com/your-repo/issues
EOF
}

# Create checksums
create_checksums() {
    log "Creating checksums..."
    
    cd "$PACKAGE_DIR"
    
    # Create checksums for important files
    find . -type f \( -name "*.py" -o -name "*.js" -o -name "*.jsx" -o -name "*.sql" -o -name "*.md" -o -name "*.yml" -o -name "*.json" \) -exec sha256sum {} \; > CHECKSUMS.txt
    
    cd - > /dev/null
}

# Validate package
validate_package() {
    log "Validating package..."
    
    # Check required files exist
    REQUIRED_FILES=(
        "$PACKAGE_DIR/README.md"
        "$PACKAGE_DIR/INSTALL.md"
        "$PACKAGE_DIR/VERSION.txt"
        "$PACKAGE_DIR/docker-compose.yml"
        "$PACKAGE_DIR/backend/app.py"
        "$PACKAGE_DIR/backend/requirements.txt"
        "$PACKAGE_DIR/frontend/package.json"
        "$PACKAGE_DIR/frontend/src/App.jsx"
        "$PACKAGE_DIR/database/schema.sql"
        "$PACKAGE_DIR/scripts/setup.sh"
        "$PACKAGE_DIR/scripts/setup.ps1"
    )
    
    for file in "${REQUIRED_FILES[@]}"; do
        if [ ! -f "$file" ]; then
            error "Required file missing: $file"
        fi
    done
    
    # Check file sizes (basic sanity check)
    PACKAGE_SIZE=$(du -sh "$PACKAGE_DIR" | cut -f1)
    log "Package size: $PACKAGE_SIZE"
    
    # Count files
    FILE_COUNT=$(find "$PACKAGE_DIR" -type f | wc -l)
    log "Total files: $FILE_COUNT"
    
    log "Package validation completed"
}

# Create archive
create_archive() {
    log "Creating archive..."
    
    cd "$BUILD_DIR"
    
    # Create zip archive
    zip -r "$ARCHIVE_NAME" "$PACKAGE_NAME-$VERSION" -x "*.DS_Store" "*.git*" "node_modules/*" "__pycache__/*" "*.pyc"
    
    # Create tarball as alternative
    tar -czf "$PACKAGE_NAME-$VERSION.tar.gz" "$PACKAGE_NAME-$VERSION" --exclude="*.DS_Store" --exclude="*.git*" --exclude="node_modules" --exclude="__pycache__" --exclude="*.pyc"
    
    cd - > /dev/null
    
    # Calculate archive sizes and checksums
    ZIP_SIZE=$(du -sh "$BUILD_DIR/$ARCHIVE_NAME" | cut -f1)
    TAR_SIZE=$(du -sh "$BUILD_DIR/$PACKAGE_NAME-$VERSION.tar.gz" | cut -f1)
    
    ZIP_CHECKSUM=$(sha256sum "$BUILD_DIR/$ARCHIVE_NAME" | cut -d' ' -f1)
    TAR_CHECKSUM=$(sha256sum "$BUILD_DIR/$PACKAGE_NAME-$VERSION.tar.gz" | cut -d' ' -f1)
    
    log "Archive created successfully"
    log "ZIP size: $ZIP_SIZE (SHA256: $ZIP_CHECKSUM)"
    log "TAR.GZ size: $TAR_SIZE (SHA256: $TAR_CHECKSUM)"
}

# Create release notes
create_release_notes() {
    log "Creating release notes..."
    
    cat > "$BUILD_DIR/RELEASE_NOTES.md" << EOF
# ERP Webapp v$VERSION Release Notes

## Release Information
- **Version**: $VERSION
- **Release Date**: $(date +"%Y-%m-%d")
- **Build**: $(git rev-parse --short HEAD 2>/dev/null || echo "N/A")

## Package Contents
- **ZIP Archive**: $ARCHIVE_NAME
- **TAR.GZ Archive**: $PACKAGE_NAME-$VERSION.tar.gz
- **Installation Guide**: INSTALL.md
- **Documentation**: README.md, docs/

## What's New in v$VERSION

### Core Features
- ✅ Complete Enterprise Risk Management system
- ✅ User authentication and authorization
- ✅ Financial data management
- ✅ Advanced risk assessment engine (5-factor model)
- ✅ Monte Carlo simulation for portfolio projections
- ✅ Asset allocation recommendations
- ✅ Goal tracking and progress monitoring
- ✅ Comprehensive reporting (PDF + Dashboard)
- ✅ Real-time analytics and visualizations

### Technical Features
- ✅ Modern React frontend with responsive design
- ✅ Flask backend with RESTful API
- ✅ PostgreSQL database with optimized schema
- ✅ Redis caching for improved performance
- ✅ Docker containerization for easy deployment
- ✅ Comprehensive API documentation
- ✅ Automated setup scripts for Linux and Windows

### Security Features
- ✅ JWT-based authentication
- ✅ CORS protection
- ✅ Input validation and sanitization
- ✅ SQL injection prevention
- ✅ XSS protection
- ✅ Rate limiting
- ✅ Secure HTTP headers

### Risk Management Framework
- ✅ ISO 31000:2018 compliant risk assessment
- ✅ Multi-factor risk scoring (0-10 scale)
- ✅ Liquidity risk analysis
- ✅ Credit risk evaluation
- ✅ Market risk assessment
- ✅ Inflation risk modeling
- ✅ Protection risk analysis

### Statistical Models
- ✅ Monte Carlo simulation engine
- ✅ Value at Risk (VaR) calculations
- ✅ Expected Shortfall analysis
- ✅ Portfolio optimization algorithms
- ✅ Actuarial modeling for retirement planning
- ✅ Goal-based investment projections

## Installation Options

### Quick Start (Docker)
1. Extract the package
2. Run: \`docker-compose up -d --build\`
3. Access: http://localhost

### Manual Installation
1. Extract the package
2. Run setup script: \`./scripts/setup.sh\` (Linux) or \`scripts\\setup.ps1\` (Windows)
3. Access: http://localhost:3000

## System Requirements
- **Minimum**: 4GB RAM, 10GB storage
- **Recommended**: 8GB RAM, 20GB storage
- **OS**: Linux, Windows 10+, macOS 10.15+

## Deployment Options
- **Development**: Local installation with setup scripts
- **Production**: Docker Compose with reverse proxy
- **Cloud**: Container orchestration (Kubernetes, Docker Swarm)
- **Enterprise**: Custom deployment with load balancing

## API Endpoints
- **Authentication**: /api/auth/*
- **Financial Data**: /api/financial/*
- **Risk Assessment**: /api/risk/*
- **Reports**: /api/reports/*
- **Documentation**: /api/docs

## Support and Documentation
- **Installation Guide**: INSTALL.md
- **User Manual**: README.md
- **API Reference**: docs/API_DOCUMENTATION.md
- **Troubleshooting**: README.md#troubleshooting

## Known Issues
- None reported for this release

## Upgrade Notes
- This is the initial release (v$VERSION)
- No upgrade path required

## Contributors
- Development Team
- Quality Assurance Team
- Documentation Team

## License
This software is licensed under the MIT License. See LICENSE file for details.

---

**Download**: $ARCHIVE_NAME ($ZIP_SIZE)
**Checksum**: $ZIP_CHECKSUM

For support, please contact: support@yourcompany.com
EOF
}

# Print package summary
print_summary() {
    echo
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  Package Summary${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo
    echo -e "${GREEN}Package Name: $PACKAGE_NAME-$VERSION${NC}"
    echo -e "${GREEN}Archive: $BUILD_DIR/$ARCHIVE_NAME${NC}"
    echo -e "${GREEN}Alternative: $BUILD_DIR/$PACKAGE_NAME-$VERSION.tar.gz${NC}"
    echo
    echo -e "${GREEN}Package Contents:${NC}"
    echo "  - Backend (Flask + Python)"
    echo "  - Frontend (React + Vite)"
    echo "  - Database schema (PostgreSQL)"
    echo "  - Docker configuration"
    echo "  - Setup scripts (Linux + Windows)"
    echo "  - Documentation"
    echo "  - Installation guide"
    echo
    echo -e "${GREEN}Ready for distribution!${NC}"
    echo
    echo -e "${YELLOW}Next steps:${NC}"
    echo "1. Test the package on a clean system"
    echo "2. Upload to distribution platform"
    echo "3. Update documentation links"
    echo "4. Announce the release"
    echo
}

# Main execution
main() {
    echo -e "${BLUE}ERP Webapp Packaging Script${NC}"
    echo -e "${BLUE}=============================${NC}"
    echo
    
    clean_build
    copy_source
    create_install_guide
    create_version_info
    create_checksums
    validate_package
    create_archive
    create_release_notes
    print_summary
    
    log "Packaging completed successfully!"
}

# Run main function
main "$@"

