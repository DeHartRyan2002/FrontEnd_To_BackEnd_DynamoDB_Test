import json
import boto3
from time import gmtime, strftime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('yourDynamoDBTableName')
now = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

def lambda_handler(event, context):
    try:
        # Check if the 'body' field exists in the event
        if 'body' not in event:
            print(event)  # Debugging line to print the event received
            raise ValueError("Missing 'body' in event" + json.dumps(event))

        # Accessing the body of the request
        body = json.loads(event['body'])

        # Extracting the first name and last name
        first_name = body.get('firstName')
        last_name = body.get('lastName')

        #print(first_name,last_name)  # Debugging line to print extracted names

        # If first name or last name is missing, raise an error
        if not first_name or not last_name:
            raise ValueError("Missing 'firstName' or 'lastName' in request")

        name = f"{first_name} {last_name}"

        response = table.put_item(
            Item={
                'id': name,
                'LatestGreetingTime': now
            }
        )
        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "yourWebsiteURL",
                "Access-Control-Allow-Credentials": True,
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            'body': json.dumps(f'Hello from Lambda, {name}')
        }
    except Exception as e:
        print("Error:", str(e))  # Debugging line to print the error
        return {
            'statusCode': 500,
            'headers': {
                "Access-Control-Allow-Origin": "yourWebsiteURL",
                "Access-Control-Allow-Credentials": True,
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            'body': json.dumps(f'Error: {str(e)}')
        }