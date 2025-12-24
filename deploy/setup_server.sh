#!/bin/bash
# DCET Platform - Initial Server Setup Script
# Run this script on a fresh Ubuntu server to install all dependencies

set -e  # Exit on error

echo "========================================="
echo "DCET Platform - Server Setup"
echo "========================================="

# Update system packages
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python and development tools
echo "Installing Python and development tools..."
sudo apt install -y python3 python3-pip python3-venv python3-dev build-essential

# Install MySQL
echo "Installing MySQL..."
sudo apt install -y mysql-server mysql-client libmysqlclient-dev
sudo systemctl start mysql
sudo systemctl enable mysql

# Install Redis
echo "Installing Redis..."
sudo apt install -y redis-server
sudo systemctl start redis
sudo systemctl enable redis

# Install Nginx
echo "Installing Nginx..."
sudo apt install -y nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Install Node.js (for frontend build)
echo "Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Create application directory
echo "Creating application directory..."
sudo mkdir -p /var/www/dcet-platform
sudo chown -R $USER:$USER /var/www/dcet-platform

# Create Python virtual environment
echo "Creating Python virtual environment..."
cd /var/www/dcet-platform
python3 -m venv venv

# Configure firewall
echo "Configuring firewall..."
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS (for future)
sudo ufw --force enable

echo "========================================="
echo "Server setup complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Clone your repository to /var/www/dcet-platform/"
echo "2. Copy backend/.env.example to backend/.env and configure"
echo "3. Run the deployment script: ./deploy/deploy.sh"
echo ""
