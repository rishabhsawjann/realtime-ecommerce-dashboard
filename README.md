# Real-Time E-commerce Sales Dashboard

A comprehensive real-time analytics system that monitors and visualizes sales from a fictional online store. Built with AWS serverless architecture and modern web technologies.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Producer │───▶│  API Gateway    │───▶│ Kinesis Firehose│
│   (Python)      │    │   (Ingestion)   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Dashboard│◀───│  API Gateway    │◀───│   Lambda        │
│                 │    │   (Analytics)   │    │   (Athena Query)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │   Amazon S3     │
                                              │   (Data Lake)   │
                                              └─────────────────┘
                                                       │
                                                       ▼
                                              ┌─────────────────┐
                                              │   Amazon Athena │
                                              │   (SQL Queries) │
                                              └─────────────────┘
```

## 🚀 Features

- **Real-time Data Ingestion**: Continuous stream of fake sales data
- **Serverless Architecture**: Fully managed AWS services
- **Live Analytics**: SQL queries on streaming data
- **Interactive Dashboard**: Real-time charts and metrics
- **Automated Deployment**: CI/CD pipeline with GitHub Actions
- **Infrastructure as Code**: AWS CDK for infrastructure management

## 📁 Project Structure

```
├── infrastructure/          # AWS CDK infrastructure code
│   ├── lib/
│   │   ├── data-ingestion-stack.ts
│   │   ├── analytics-stack.ts
│   │   └── dashboard-stack.ts
│   ├── bin/
│   │   └── app.ts
│   └── package.json
├── backend/                 # Lambda functions and data producer
│   ├── lambda/
│   │   ├── analytics-handler.py
│   │   └── requirements.txt
│   ├── data-producer/
│   │   ├── producer.py
│   │   └── requirements.txt
│   └── requirements.txt
├── frontend/               # React dashboard application
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── App.tsx
│   ├── package.json
│   └── public/
├── .github/                # GitHub Actions workflows
│   └── workflows/
│       ├── deploy-infrastructure.yml
│       └── deploy-frontend.yml
├── scripts/                # Utility scripts
│   ├── setup.sh
│   └── deploy.sh
└── README.md
```

## 🛠️ Tech Stack

### Cloud Infrastructure
- **AWS API Gateway** - RESTful APIs for data ingestion and analytics
- **AWS Kinesis Data Firehose** - Real-time data streaming
- **Amazon S3** - Data lake storage
- **Amazon Athena** - Serverless SQL analytics
- **AWS Lambda** - Serverless compute for analytics queries
- **AWS CDK** - Infrastructure as Code

### Backend
- **Python** - Lambda functions and data producer
- **boto3** - AWS SDK for Python

### Frontend
- **React** - User interface framework
- **TypeScript** - Type-safe JavaScript
- **Recharts** - Charting library
- **Axios** - HTTP client

### DevOps
- **GitHub Actions** - CI/CD pipeline
- **AWS CDK** - Infrastructure deployment

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- AWS CLI configured
- AWS CDK installed globally

### Installation

1. **Clone and setup the project:**
```bash
git clone <repository-url>
cd e-commerce-sales-dashboard
```

2. **Install dependencies:**
```bash
# Install CDK dependencies
cd infrastructure
npm install

# Install backend dependencies
cd ../backend
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
npm install
```

3. **Deploy infrastructure:**
```bash
cd ../infrastructure
npm run deploy
```

4. **Start the data producer:**
```bash
cd ../backend/data-producer
python producer.py
```

5. **Start the dashboard:**
```bash
cd ../frontend
npm start
```

## 📊 Dashboard Features

- **Real-time Sales Metrics**: Live updates every 10 seconds
- **Top Selling Products**: Dynamic product rankings
- **Geographic Sales Distribution**: Sales by location
- **Revenue Trends**: Time-series revenue visualization
- **Product Categories**: Sales breakdown by category

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the frontend directory:
```env
REACT_APP_API_ENDPOINT=https://your-api-gateway-url.amazonaws.com
REACT_APP_REGION=us-east-1
```

### AWS Configuration

Ensure your AWS credentials are configured:
```bash
aws configure
```

## 🚀 Deployment

### Manual Deployment
```bash
# Deploy infrastructure
cd infrastructure
npm run deploy

# Deploy frontend (after infrastructure is ready)
cd ../frontend
npm run build
npm run deploy
```

### Automated Deployment
The project includes GitHub Actions workflows that automatically deploy on push to main branch.

## 📈 Monitoring and Analytics

- **CloudWatch Logs**: Lambda function logs
- **CloudWatch Metrics**: API Gateway and Lambda metrics
- **S3 Access Logs**: Data lake access monitoring
- **Athena Query History**: Analytics query performance

## 🔒 Security

- **IAM Roles**: Least privilege access for Lambda functions
- **API Gateway**: Request throttling and authentication
- **S3 Bucket Policies**: Secure data lake access
- **CORS Configuration**: Frontend API access control

## 📝 License

MIT License - see LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For questions or issues, please open a GitHub issue or contact the development team. 