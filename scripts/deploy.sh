#!/bin/bash

set -e

echo "🚀 Deploying Real-Time E-commerce Sales Dashboard"

# Check if AWS credentials are configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured. Please run 'aws configure' first."
    exit 1
fi

# Deploy infrastructure
echo "🏗️  Deploying infrastructure..."
cd infrastructure
npm run deploy
cd ..

# Get the API Gateway URL from CDK outputs
echo "📡 Getting API Gateway URL..."
API_URL=$(aws cloudformation describe-stacks --stack-name EcommerceAnalyticsStack --query 'Stacks[0].Outputs[?OutputKey==`AnalyticsApiUrl`].OutputValue' --output text)

if [ -z "$API_URL" ]; then
    echo "❌ Failed to get API Gateway URL"
    exit 1
fi

echo "✅ API Gateway URL: $API_URL"

# Update frontend environment
echo "🔧 Updating frontend environment..."
cd frontend
echo "REACT_APP_API_ENDPOINT=$API_URL" > .env
echo "REACT_APP_REGION=us-east-1" >> .env

# Build and deploy frontend
echo "📦 Building frontend..."
npm run build

# Get S3 bucket name from CDK outputs
FRONTEND_BUCKET=$(aws cloudformation describe-stacks --stack-name EcommerceDashboardStack --query 'Stacks[0].Outputs[?OutputKey==`FrontendBucketName`].OutputValue' --output text)

if [ -z "$FRONTEND_BUCKET" ]; then
    echo "❌ Failed to get frontend bucket name"
    exit 1
fi

echo "📤 Deploying frontend to S3..."
aws s3 sync build/ s3://$FRONTEND_BUCKET --delete

# Get CloudFront distribution ID
DISTRIBUTION_ID=$(aws cloudformation describe-stacks --stack-name EcommerceDashboardStack --query 'Stacks[0].Outputs[?OutputKey==`CloudFrontDistributionId`].OutputValue' --output text)

if [ -n "$DISTRIBUTION_ID" ]; then
    echo "🔄 Invalidating CloudFront cache..."
    aws cloudfront create-invalidation --distribution-id $DISTRIBUTION_ID --paths "/*"
fi

cd ..

echo "✅ Deployment complete!"
echo ""
echo "🎉 Your dashboard is now live!"
echo "Frontend URL: https://$(aws cloudformation describe-stacks --stack-name EcommerceDashboardStack --query 'Stacks[0].Outputs[?OutputKey==`FrontendUrl`].OutputValue' --output text)"
echo ""
echo "To start generating data, run:"
echo "cd backend/data-producer && python producer.py" 