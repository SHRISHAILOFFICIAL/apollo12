#!/bin/bash
# DCET Platform - Quick Deploy Script (No Dependencies)
# Use this for quick updates when you haven't changed dependencies
# Run this script to deploy/update the application WITHOUT reinstalling dependencies

set -e  # Exit on error

echo "========================================="
echo "DCET Platform - Quick Deployment"
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

# Run database migrations (quick, only applies new migrations)
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files (quick, only copies changed files)
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Frontend deployment
echo "Deploying frontend..."
cd $FRONTEND_DIR

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

# Test Nginx configuration
echo "Testing Nginx configuration..."
sudo nginx -t

# Restart services
echo "Restarting services..."
sudo systemctl restart dcet-backend
sudo systemctl restart dcet-frontend
sudo systemctl restart nginx

# Check service status
echo ""
echo "========================================="
echo "Quick Deployment complete!"
echo "========================================="
echo ""
echo "Service status:"
sudo systemctl status dcet-backend --no-pager -l | head -5
echo ""
sudo systemctl status dcet-frontend --no-pager -l | head -5
echo ""
sudo systemctl status nginx --no-pager -l | head -5
echo ""
echo "Application should be accessible at: http://192.168.1.18"
echo ""
