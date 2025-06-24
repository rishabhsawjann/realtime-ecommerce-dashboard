import os
import json
import boto3
import base64

FIREHOSE_STREAM_NAME = os.environ.get('FIREHOSE_STREAM_NAME')
firehose = boto3.client('firehose')

def handler(event, context):
    try:
        # API Gateway proxy integration: event['body'] is a JSON string
        if 'body' in event:
            body = event['body']
            if isinstance(body, str):
                data = json.loads(body)
            else:
                data = body
        else:
            data = event
        # Add timestamp if not present
        if 'timestamp' not in data:
            from datetime import datetime
            data['timestamp'] = datetime.utcnow().isoformat()
        # Put record to Firehose
        response = firehose.put_record(
            DeliveryStreamName=FIREHOSE_STREAM_NAME,
            Record={
                'Data': (json.dumps(data) + '\n').encode('utf-8')
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Data ingested successfully', 'recordId': response.get('RecordId')})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        } 