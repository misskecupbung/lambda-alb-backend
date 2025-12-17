# Lambda ALB Backend

A simple AWS Lambda function that serves an HTML page from S3, designed to work behind an Application Load Balancer (ALB).

## Architecture

```
ALB → Lambda → S3 (index.html)
```

## Prerequisites

- AWS Account with appropriate permissions
- S3 bucket with `index.html` uploaded
- Lambda function with S3 read permissions
- Application Load Balancer configured with Lambda target group

## Setup

### 1. Configure Environment Variables

Set the following environment variables in your Lambda function:

| Variable | Description | Example |
|----------|-------------|--------|
| `S3_BUCKET` | Name of your S3 bucket | `my-website-bucket` |
| `AWS_REGION` | AWS region where your bucket is located | `ap-southeast-1` |

### 2. Upload HTML File

Upload `index.html` to your S3 bucket:

```bash
aws s3 cp index.html s3://your-bucket-name/index.html
```

### 3. Lambda IAM Policy

Ensure your Lambda execution role has the following permissions:

```json
{
  "Effect": "Allow",
  "Action": ["s3:GetObject"],
  "Resource": "arn:aws:s3:::your-bucket-name/*"
}
```

## Files

- `lambda_function.py` - Main Lambda handler
- `index.html` - Sample HTML page served by the Lambda

## License

MIT