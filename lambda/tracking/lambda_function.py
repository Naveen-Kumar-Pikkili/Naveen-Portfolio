import json
import boto3
from datetime import datetime
import random
import string

dynamo = boto3.resource('dynamodb')
cloudwatch = boto3.client('cloudwatch')

TABLE_NAME = 'VisitorTracking'

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))

        # Get IP Address from request context or headers
        ip = 'unknown'
        if 'requestContext' in event:
            # REST API
            if 'identity' in event['requestContext']:
                ip = event['requestContext']['identity'].get('sourceIp', 'unknown')
            # HTTP API
            elif 'http' in event['requestContext']:
                ip = event['requestContext']['http'].get('sourceIp', 'unknown')
        if ip == 'unknown':
            headers = event.get('headers', {})
            xff = headers.get('X-Forwarded-For') or headers.get('x-forwarded-for')
            if xff:
                ip = xff.split(',')[0]

        table = dynamo.Table(TABLE_NAME)

        # Create unique ID like JS version
        rand_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        unique_id = f"{int(datetime.utcnow().timestamp() * 1000)}-{rand_str}"

        item = {
            'id': unique_id,
            'page': body.get('page', 'unknown'),
            'userAgent': body.get('userAgent', 'unknown'),
            'ipAddress': ip,
            'timestamp': datetime.utcnow().isoformat()
        }

        # Save to DynamoDB
        table.put_item(Item=item)

        # Send custom CloudWatch metric
        cloudwatch.put_metric_data(
            Namespace='Portfolio/Visitors',
            MetricData=[
                {
                    'MetricName': 'PageVisit',
                    'Dimensions': [{'Name': 'Page', 'Value': item['page']}],
                    'Unit': 'Count',
                    'Value': 1
                }
            ]
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Visit logged successfully'}),
            'headers': {
                'Access-Control-Allow-Origin': '*'
            }
        }

    except Exception as e:
        print(f"Error logging visit: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal Server Error'}),
            'headers': {
                'Access-Control-Allow-Origin': '*'
            }
        }
