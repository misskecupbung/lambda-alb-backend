"""Lambda function to serve HTML content from S3 via ALB."""

import os
import boto3
import botocore

# Configuration from environment variables
S3_BUCKET = os.environ.get('S3_BUCKET')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
HTML_KEY = 'index.html'

# Initialize S3 client
s3_client = boto3.client('s3', region_name=AWS_REGION)


def lambda_handler(event, context):
    """Main Lambda handler for ALB integration.
    
    Args:
        event: ALB request event
        context: Lambda context object
    
    Returns:
        dict: ALB-compatible response with HTML content
    """
    html_content, status_code = get_html_from_s3()
    
    return {
        'statusCode': status_code,
        'statusDescription': f'{status_code} OK' if status_code == 200 else f'{status_code} Error',
        'isBase64Encoded': False,
        'headers': {
            'Content-Type': 'text/html'
        },
        'body': html_content
    }


def get_html_from_s3():
    """Fetch HTML content from S3 bucket.
    
    Returns:
        tuple: (html_content, status_code)
    """
    if not S3_BUCKET:
        return generate_error_html('S3_BUCKET environment variable is not set'), 500
    
    try:
        response = s3_client.get_object(Bucket=S3_BUCKET, Key=HTML_KEY)
        html_content = response['Body'].read().decode('utf-8')
        return html_content, 200
    except botocore.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        if error_code == 'NoSuchKey':
            return generate_error_html(f'File not found: {HTML_KEY}'), 404
        elif error_code == 'NoSuchBucket':
            return generate_error_html(f'Bucket not found: {S3_BUCKET}'), 404
        elif error_code == 'AccessDenied':
            return generate_error_html('Access denied to S3 bucket'), 403
        return generate_error_html(f'S3 Error: {error_message}'), 500
    except Exception as e:
        return generate_error_html(f'Unexpected error: {str(e)}'), 500


def generate_error_html(message):
    """Generate a simple HTML error page.
    
    Args:
        message: Error message to display
    
    Returns:
        str: HTML error page
    """
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Error</title>
</head>
<body>
    <h1>Error</h1>
    <p>{message}</p>
</body>
</html>"""
