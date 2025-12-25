#!/bin/bash
# DCET Platform - Deployment Script
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

# Navigate to project directory
cd $PROJECT_DIR

# Pull latest code from GitHub
echo "Pulling latest code..."
git pull origin main

# Backend deployment
echo "Deploying backend..."
cd $BACKEND_DIR

# Activate virtual environment
source $VENV_DIR/bin/activate

# Install/update Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements-prod.txt

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

# Frontend deployment
echo "Deploying frontend..."
cd $FRONTEND_DIR

# Install Node dependencies (only missing ones)
echo "Installing Node dependencies..."
npm install

# Build frontend in standalone mode
echo "Building frontend..."
npm run build:prod

# The standalone build creates everything in .next/standalone
# We need to copy static assets and the .next folder structure
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

# Copy Nginx configuration
echo "Updating Nginx configuration..."
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

# Restart services
echo "Restarting services..."
sudo systemctl restart dcet-backend
sudo systemctl restart dcet-frontend
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
echo "Application should be accessible at: http://192.168.54.75"
echo ""
