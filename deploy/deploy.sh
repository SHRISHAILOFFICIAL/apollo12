#!/bin/bash
# DCET Platform - Optimized Deployment Script
# Run this script to deploy/update the application

set -e  # Exit on error

echo "========================================="
echo "DCET Platform - Deployment"
echo "========================================="

# Configuration
PROJECT_DIR="/var/www/dcet-platform"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"
VENV_DIR="$PROJECT_DIR/venv"

# Parse arguments
SKIP_FRONTEND=false
SKIP_BACKEND=false
SKIP_NPM=false
FORCE_REBUILD=false

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --backend-only) SKIP_FRONTEND=true ;;
        --frontend-only) SKIP_BACKEND=true ;;
        --skip-npm) SKIP_NPM=true ;;
        --force) FORCE_REBUILD=true ;;
        -h|--help) 
            echo "Usage: ./deploy.sh [options]"
            echo ""
            echo "Options:"
            echo "  --backend-only   Only deploy backend (skip frontend build)"
            echo "  --frontend-only  Only deploy frontend (skip backend)"
            echo "  --skip-npm       Skip npm install (use existing node_modules)"
            echo "  --force          Force full rebuild of everything"
            echo "  -h, --help       Show this help message"
            exit 0
            ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
    shift
done

# Navigate to project directory
cd $PROJECT_DIR

# Pull latest code from GitHub
echo "Pulling latest code..."
git pull origin main

# Store the git diff to check what changed
BACKEND_CHANGED=$(git diff --name-only HEAD~1 HEAD -- backend/ 2>/dev/null | wc -l)
FRONTEND_CHANGED=$(git diff --name-only HEAD~1 HEAD -- frontend/ 2>/dev/null | wc -l)
REQUIREMENTS_CHANGED=$(git diff --name-only HEAD~1 HEAD -- backend/requirements*.txt 2>/dev/null | wc -l)
PACKAGE_JSON_CHANGED=$(git diff --name-only HEAD~1 HEAD -- frontend/package*.json 2>/dev/null | wc -l)

echo ""
echo "Changes detected:"
echo "  Backend files: $BACKEND_CHANGED"
echo "  Frontend files: $FRONTEND_CHANGED"
echo "  Requirements changed: $REQUIREMENTS_CHANGED"
echo "  Package.json changed: $PACKAGE_JSON_CHANGED"
echo ""

# Backend deployment
if [ "$SKIP_BACKEND" = false ]; then
    echo "========================================="
    echo "Deploying backend..."
    echo "========================================="
    cd $BACKEND_DIR

    # Create virtual environment if it doesn't exist
    if [ ! -d "$VENV_DIR" ]; then
        echo "Creating virtual environment..."
        python3 -m venv $VENV_DIR
    fi

    # Activate virtual environment
    source $VENV_DIR/bin/activate

    # Install/update Python dependencies only if requirements changed or forced
    if [ "$REQUIREMENTS_CHANGED" -gt 0 ] || [ "$FORCE_REBUILD" = true ] || [ ! -f "$VENV_DIR/.requirements_installed" ]; then
        echo "Installing Python dependencies..."
        pip install --upgrade -r requirements-prod.txt
        touch "$VENV_DIR/.requirements_installed"
    else
        echo "Skipping pip install (requirements unchanged)"
    fi

    # Run database migrations
    echo "Running database migrations..."
    python manage.py migrate --noinput

    # Collect static files
    echo "Collecting static files..."
    python manage.py collectstatic --noinput

    # Create necessary directories
    mkdir -p staticfiles media

    # Set proper permissions
    sudo chown -R www-data:www-data staticfiles media
else
    echo "Skipping backend deployment (--frontend-only)"
fi

# Frontend deployment
if [ "$SKIP_FRONTEND" = false ]; then
    echo ""
    echo "========================================="
    echo "Deploying frontend..."
    echo "========================================="
    cd $FRONTEND_DIR

    # Install Node dependencies only if package.json changed or forced
    if [ "$SKIP_NPM" = false ]; then
        if [ "$PACKAGE_JSON_CHANGED" -gt 0 ] || [ "$FORCE_REBUILD" = true ] || [ ! -d "node_modules" ]; then
            echo "Installing Node dependencies..."
            npm install
        else
            echo "Skipping npm install (package.json unchanged)"
        fi
    else
        echo "Skipping npm install (--skip-npm flag)"
    fi

    # Build frontend only if frontend files changed or forced
    if [ "$FRONTEND_CHANGED" -gt 0 ] || [ "$FORCE_REBUILD" = true ] || [ ! -d ".next" ]; then
        echo "Building frontend..."
        npm run build:prod

        # The standalone build creates everything in .next/standalone
        echo "Setting up standalone server..."

        # Copy public folder to standalone
        if [ -d "public" ]; then
            cp -r public .next/standalone/
        fi

        # Copy the entire .next folder to standalone/.next
        cp -r .next/static .next/standalone/.next/
        cp -r .next/server .next/standalone/.next/

        # Set proper permissions for standalone directory
        sudo chown -R www-data:www-data .next
    else
        echo "Skipping frontend build (no frontend changes)"
    fi
else
    echo "Skipping frontend deployment (--backend-only)"
fi

# Nginx configuration
echo ""
echo "========================================="
echo "Configuring Nginx..."
echo "========================================="
cd $PROJECT_DIR

# Copy Nginx configuration
sudo cp $PROJECT_DIR/nginx.conf /etc/nginx/sites-available/dcet-platform

# Create symlink if it doesn't exist
if [ ! -L /etc/nginx/sites-enabled/dcet-platform ]; then
    sudo ln -s /etc/nginx/sites-available/dcet-platform /etc/nginx/sites-enabled/
fi

# Remove default nginx site if it exists
if [ -L /etc/nginx/sites-enabled/default ]; then
    sudo rm /etc/nginx/sites-enabled/default
fi

# Test Nginx configuration
echo "Testing Nginx configuration..."
sudo nginx -t

# Copy systemd service files
echo "Updating systemd services..."
sudo cp $PROJECT_DIR/deploy/dcet-backend.service /etc/systemd/system/
sudo cp $PROJECT_DIR/deploy/dcet-frontend.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Restart services based on what was deployed
echo ""
echo "Restarting services..."
if [ "$SKIP_BACKEND" = false ]; then
    sudo systemctl restart dcet-backend
fi
if [ "$SKIP_FRONTEND" = false ]; then
    sudo systemctl restart dcet-frontend
fi
sudo systemctl restart nginx

# Enable services to start on boot
sudo systemctl enable dcet-backend
sudo systemctl enable dcet-frontend
sudo systemctl enable nginx

# Check service status
echo ""
echo "========================================="
echo "Deployment complete!"
echo "========================================="
echo ""
echo "Service status:"
sudo systemctl status dcet-backend --no-pager -l
echo ""
sudo systemctl status dcet-frontend --no-pager -l
echo ""
sudo systemctl status nginx --no-pager -l
echo ""

# Get current IP
CURRENT_IP=$(hostname -I | awk '{print $1}')
echo "Application accessible at: http://$CURRENT_IP"
echo ""
