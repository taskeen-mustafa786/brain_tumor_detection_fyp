#!/bin/bash

# Brain Tumor Detection - Deployment Script
# This script helps deploy both frontend and backend

echo "🚀 Brain Tumor Detection Deployment Script"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required tools are installed
check_dependencies() {
    print_status "Checking dependencies..."

    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js first."
        exit 1
    fi

    if ! command -v npm &> /dev/null; then
        print_error "npm is not installed. Please install npm first."
        exit 1
    fi

    if ! command -v git &> /dev/null; then
        print_error "Git is not installed. Please install Git first."
        exit 1
    fi

    print_success "All dependencies are installed."
}

# Deploy frontend to GitHub Pages
deploy_frontend() {
    print_status "Deploying frontend to GitHub Pages..."

    # Check if package.json exists
    if [ ! -f "package.json" ]; then
        print_error "package.json not found. Run 'npm init -y' first."
        return 1
    fi

    # Install dependencies
    npm install

    # Deploy to GitHub Pages
    npm run deploy

    if [ $? -eq 0 ]; then
        print_success "Frontend deployed successfully!"
        print_success "Frontend URL: https://taskeen-mustafa786.github.io/brain_tumor_detection_fyp"
    else
        print_error "Frontend deployment failed."
        return 1
    fi
}

# Prepare backend for deployment
prepare_backend() {
    print_status "Preparing backend for deployment..."

    # Check if .env file exists
    if [ ! -f ".env" ]; then
        print_warning ".env file not found. Please create one with your configuration."
        print_warning "Copy .env.example to .env and fill in your values."
    fi

    # Check if Procfile exists
    if [ ! -f "Procfile" ]; then
        print_error "Procfile not found."
        return 1
    fi

    print_success "Backend preparation complete."
}

# Deploy backend to Heroku
deploy_backend_heroku() {
    print_status "Deploying backend to Heroku..."

    # Check if Heroku CLI is installed
    if ! command -v heroku &> /dev/null; then
        print_error "Heroku CLI is not installed."
        print_status "Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli"
        return 1
    fi

    # Check if user is logged in
    heroku whoami &> /dev/null
    if [ $? -ne 0 ]; then
        print_warning "Please login to Heroku first:"
        heroku login
    fi

    # Create Heroku app
    read -p "Enter Heroku app name (or press Enter for auto-generated): " app_name
    if [ -z "$app_name" ]; then
        heroku create
    else
        heroku create "$app_name"
    fi

    # Set environment variables
    print_status "Setting environment variables..."
    heroku config:set APP_ENV=production
    heroku config:set DEBUG=false
    heroku config:set PORT=8000

    # Ask for Firebase config
    print_warning "Please set your Firebase configuration variables:"
    echo "Run the following commands with your actual values:"
    echo "heroku config:set FIREBASE_API_KEY=your_api_key"
    echo "heroku config:set FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com"
    echo "heroku config:set FIREBASE_PROJECT_ID=your_project_id"
    echo "heroku config:set JWT_SECRET=your_secure_jwt_secret"

    # Deploy
    print_status "Deploying to Heroku..."
    git push heroku main

    if [ $? -eq 0 ]; then
        print_success "Backend deployed successfully!"
        heroku apps:info --json | grep -o '"web_url": "[^"]*"' | cut -d'"' -f4
    else
        print_error "Backend deployment failed."
        return 1
    fi
}

# Main menu
show_menu() {
    echo ""
    echo "Select deployment option:"
    echo "1) Deploy Frontend Only (GitHub Pages)"
    echo "2) Deploy Backend Only (Heroku)"
    echo "3) Prepare for Deployment (Both)"
    echo "4) Full Deployment (Frontend + Backend)"
    echo "5) Exit"
    echo ""
    read -p "Enter your choice (1-5): " choice
}

# Main script
main() {
    check_dependencies

    while true; do
        show_menu

        case $choice in
            1)
                deploy_frontend
                ;;
            2)
                prepare_backend
                deploy_backend_heroku
                ;;
            3)
                prepare_backend
                print_success "Ready for manual deployment."
                ;;
            4)
                deploy_frontend
                prepare_backend
                deploy_backend_heroku
                ;;
            5)
                print_status "Goodbye!"
                exit 0
                ;;
            *)
                print_error "Invalid option. Please choose 1-5."
                ;;
        esac

        echo ""
        read -p "Press Enter to continue..."
    done
}

# Run main function
main