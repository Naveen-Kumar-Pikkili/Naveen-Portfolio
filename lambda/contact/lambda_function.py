import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
cloudwatch = boto3.client('cloudwatch')
table = dynamodb.Table('ContactFormSubmission')  # Replace with your actual table name

def lambda_handler(event, context):
    try:
        # Parse JSON body from API Gateway
        body = json.loads(event.get('body', '{}'))

        # Validate required fields
        required_fields = ['name', 'email', 'mobile', 'message']
        for field in required_fields:
            if not body.get(field):
                return response(400, f"Missing required field: {field}")

        # Prepare item for DynamoDB
        item = {
            'id': str(uuid.uuid4()),
            'name': body['name'],
            'email': body['email'],
            'mobile': body['mobile'],
            'message': body['message'],
            'timestamp': datetime.utcnow().isoformat()
        }

        # Store in DynamoDB
        table.put_item(Item=item)

        # Push custom metric to CloudWatch
        cloudwatch.put_metric_data(
            Namespace='PortfolioApp',
            MetricData=[{
                'MetricName': 'FormSubmissions',
                'Value': 1,
                'Unit': 'Count'
            }]
        )

        return response(200, 'Submission received!')

    except Exception as e:
        print('Error:', str(e))
        return response(500, f"Internal server error: {str(e)}")


def response(status_code, message):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*'
        },
        'body': json.dumps({'message': message})
    }
