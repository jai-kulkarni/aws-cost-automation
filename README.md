# AWS Cost Automation for Organization Accounts

This project aims to automate AWS cost analysis for organization accounts, providing insights into spending patterns and top services utilized. By leveraging AWS Lambda functions and necessary permissions, this solution offers a clear picture of expenditure across all member accounts within an organization.


## Pre-requisites

1. **AWS Management Account**: Access to an AWS management account with permissions to manage all member accounts within the organization.
2. **Lambda Function Access**: Access to AWS Lambda service with the runtime environment set to Python.
3. **Lambda Function Role Permissions**: Adequate permissions assigned to the Lambda function role, including permissions for AWS Cost Explorer and SES (Simple Email Service).


## Purpose

The purpose of this project is to provide organizational management with detailed insights into spending across various AWS accounts. By implementing a solution that updates costs two days prior, it ensures that the data remains relevant and accurate despite any potential delays in the AWS Cost Explorer API updates.


## Enhancements

1. **Scheduled Analysis**: Implement scheduling options (daily, weekly, monthly, or custom) using Amazon EventBridge to automate cost analysis at regular intervals.
2. **Cost Data Storage**: Enable storing spending data categorized by account in an Amazon S3 bucket for further analysis and historical tracking.