# MIT License

# Copyright (c) 2023 Jacques Le Thuaut

import json
import boto3

def handler(event, context):
    # Extract task ID or ARN from the event object
    task_arn = event.get('task_arn', None)
    if task_arn is None:
        return {
            'statusCode': 400,
            'body': json.dumps('No task ARN provided.')
        }

    # Initialize the AWS Braket client
    braket_client = boto3.client('braket')

    # Fetch the quantum task result
    try:
        task_result = braket_client.get_quantum_task(task_arn)
        output = task_result.get('output', {})
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Failed to fetch task result: {str(e)}')
        }

    # Additional post-processing can be done here
    # For example, you might want to save the output to an S3 bucket

    return {
        'statusCode': 200,
        'body': json.dumps(f'Successfully fetched task result: {output}')
    }
