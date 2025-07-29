import boto3
import botocore

def lambda_handler(event, context):
    # Explicitly specify endpoint URL and region
    client = boto3.client(
        's3',
        endpoint_url='https://st-deviz-s3-vpce.s3.us-east-1.amazonaws.com',
        region_name='us-east-1'
    )

    html = get_object(client)

    response = {
        'statusCode': 200,
        'statusDescription': '200 OK',
        'isBase64Encoded': False,
        'headers': {
            'Content-Type': 'text/html'
        },
        'body': html
    }

    return response

def get_object(client):
    try:
        response = client.get_object(
            Bucket='<s3_bucket>',
            Key='index.html'
        )
        body = response['Body'].read().decode('utf-8')
        return body
    except botocore.exceptions.ClientError as e:
        return f"Error fetching object: {e.response['Error']['Message']}"
    except Exception as e:
        return f"Unhandled error: {str(e)}"
