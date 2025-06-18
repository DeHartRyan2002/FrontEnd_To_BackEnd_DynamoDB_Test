import json
import boto3
from time import gmtime, strftime

# Initialize the DynamoDB resource and table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UserResponses')
now = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

# AWS Bedrock endpoint details
bedrock_client = boto3.client('bedrock')
BEDROCK_MODEL_ID = 'your-bedrock-model-id'  # Replace with your Bedrock model ID

def call_bedrock_model(input_text):
    response = bedrock_client.invoke_model(
        ModelId=BEDROCK_MODEL_ID,
        Body=json.dumps({"text": input_text}),
        ContentType="application/json"
    )
    return json.loads(response['Body'].read())

def lambda_handler(event, context):
    try:
        # Debugging: Print the entire event object
        print("Event received:", json.dumps(event, indent=2))
        
        # Check if the 'body' field exists in the event
        if 'body' not in event:
            raise ValueError("Missing 'body' in event")

        # Accessing the body of the request
        body = json.loads(event['body'])
        print("Body:", body)  # Debugging line to print the body

        # Extracting the first name and last name
        first_name = body.get('firstName')
        last_name = body.get('lastName')

        print("First name:", first_name)  # Debugging line to print first name
        print("Last name:", last_name)    # Debugging line to print last name

        # If first name or last name is missing, raise an error
        if not first_name or not last_name:
            raise ValueError("Missing 'firstName' or 'lastName' in request")

        # Construct the input for the AI model
        input_text = f"{first_name} {last_name}"

        # Call Bedrock endpoint
        bedrock_response = call_bedrock_model(input_text)
        ai_interpretation = bedrock_response.get('generated_text', '')

        # Insert item into DynamoDB table
        db_response = table.put_item(
            Item={
                'ID': input_text,
                'LatestGreetingTime': now,
                'Interpretation': ai_interpretation
            }
        )
        
        # Debugging: Print the response from DynamoDB
        print("DynamoDB response:", json.dumps(db_response, indent=2))
        
        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "http://testserveryeehaw.s3-website.us-east-2.amazonaws.com",
                "Access-Control-Allow-Credentials": True,
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            'body': json.dumps(f'Hello from Lambda, {first_name} {last_name}. Interpretation: {ai_interpretation}')
        }
    except Exception as e:
        print("Error:", str(e))  # Debugging line to print the error
        return {
            'statusCode': 500,
            'headers': {
                "Access-Control-Allow-Origin": "http://testserveryeehaw.s3-website.us-east-2.amazonaws.com",
                "Access-Control-Allow-Credentials": True,
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            'body': json.dumps(f'Error: {str(e)}')
        }
