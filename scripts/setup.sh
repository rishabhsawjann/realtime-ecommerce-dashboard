#!/bin/bash

echo "🚀 Setting up Real-Time E-commerce Sales Dashboard"

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI is not installed. Please install it first:"
    echo "   https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install it first:"
    echo "   https://nodejs.org/"
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install it first:"
    echo "   https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Install CDK globally
echo "📦 Installing AWS CDK globally..."
npm install -g aws-cdk

# Install infrastructure dependencies
echo "📦 Installing infrastructure dependencies..."
cd infrastructure
npm install
cd ..

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
pip install -r requirements.txt
cd ..

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure AWS credentials: aws configure"
echo "2. Deploy infrastructure: cd infrastructure && npm run deploy"
echo "3. Start data producer: cd backend/data-producer && python producer.py"
echo "4. Start frontend: cd frontend && npm start"
echo ""
echo "For more information, see README.md" 