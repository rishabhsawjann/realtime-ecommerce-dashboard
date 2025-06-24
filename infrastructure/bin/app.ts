#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { DataIngestionStack } from '../lib/data-ingestion-stack';
import { AnalyticsStack } from '../lib/analytics-stack';
import { DashboardStack } from '../lib/dashboard-stack';

const app = new cdk.App();

// Get environment variables
const account = process.env.CDK_DEFAULT_ACCOUNT;
const region = process.env.CDK_DEFAULT_REGION || 'us-east-1';

if (!account) {
  throw new Error('CDK_DEFAULT_ACCOUNT environment variable is required');
}

// Create the data ingestion stack (S3, Kinesis, API Gateway for ingestion)
const dataIngestionStack = new DataIngestionStack(app, 'EcommerceDataIngestionStack', {
  env: { account, region },
  description: 'Data ingestion infrastructure for e-commerce sales dashboard',
});

// Create the analytics stack (Athena, Lambda for analytics)
const analyticsStack = new AnalyticsStack(app, 'EcommerceAnalyticsStack', {
  env: { account, region },
  description: 'Analytics infrastructure for e-commerce sales dashboard',
  dataBucket: dataIngestionStack.dataBucket,
});

// Create the dashboard stack (API Gateway for analytics, CloudFront for frontend)
const dashboardStack = new DashboardStack(app, 'EcommerceDashboardStack', {
  env: { account, region },
  description: 'Dashboard infrastructure for e-commerce sales dashboard',
  analyticsLambda: analyticsStack.analyticsLambda,
});

// Add dependencies
analyticsStack.addDependency(dataIngestionStack);
dashboardStack.addDependency(analyticsStack);

// Add tags to all stacks
const tags = {
  Project: 'EcommerceSalesDashboard',
  Environment: 'Production',
  Owner: 'Development Team',
  CostCenter: 'Analytics',
};

[dataIngestionStack, analyticsStack, dashboardStack].forEach(stack => {
  Object.entries(tags).forEach(([key, value]) => {
    cdk.Tags.of(stack).add(key, value);
  });
});

app.synth(); 