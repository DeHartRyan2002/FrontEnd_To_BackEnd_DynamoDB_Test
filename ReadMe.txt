Directions:

1. Create S3 Bucket:
	In AWS find S3 service and select "Create Bucket"
	Choose "General Purpose" and name the Bucket
	To host static website uncheck "Block all public access" and acknowledge the statement
	Select Create Bucket

2. Upload index.html file

3. Enable "Static Website Hosting"
	Navigate to properties within the S3 bucket
	scroll to the bottom of the page and select "Edit" within Static Website Hosting
	Enable static website hosting
	fill in the index document name which should be index.html if using the file in the github
	Select "Save changes"
	Take note of the S3's ARN

4. Create Bucket policy
	Navigate to Permissions within the S3 bucket
	Select Edit within Bucket policy
	Paste the bucket policy code provided
	replace "yourARN" with the previouslt mentioned ARN
	Select "Save Changes"

5. Test if website is working
	In parameters scroll to the bottom of the page and click the "Bucket website endpoint" link

6. Create a Lambda function to transfer data to DynamoDB
	Navigate to the Lambda service
	Select "Create function"
	Select "Author from scratch"
	enter the function name (ex. UserResponse)
	Select the most up-to-date python version within "Runtime" (3.13 as of writing this)
	Select "Create function"
	Delete the default code within the text editor under the "code" tab and insert the code seen within the "userResponseLambdaCode" function file
	Replace "yourWebsiteURL" within the headers with the website's URL hosted in S3
	Deploy the Lambda function

7. Setup a RestAPI via APIGateway
	Navigate to the APIGateway Service
	Select "Create API"
	Select "Build" under REST API
	Select "New API"
	Enter an API name (ex. UserResponseAPI)
	Select "Edge-optimized" under API endpoint type
	Keep IPv4 selected
	Select "Create API"

8. Create a Resource, a POST Method,and a OPTIONS Method
	Within your API navigate to the "Resources" tab
	Select "Create Resource"
	Enter your Resource Name (ex. UserResponse)
	Select "Create Resource"
	Select "Create method" within your resource
	Select "Post" as a method type
	Select Lambda Function under integration type
	Choose your lambda function under "Lambda function"
	Select "Create method"
	Select your resource and "Create method" again
	This time the method type is "OPTIONS"
	Select Mock as the integration type
	Select "Create method"

9. Create Mapping Template
	Select "POST" Under resouces
	Select "Integration request"
	Select "Edit"
	Expand "Mapping Templates"
	Select "Add mapping templates"
	Write "application/json" in content type
	Copy paste the test within the "mappingTemplate" file
	Select "Save"

10. Enable CORS
	Navigate to your resource
	Select Enable CORS within "Resouce details"
	Select "default 4XX" and "default 5XX"
	Select "OPTIONS" and "POST"
	Leave the text within "Access-Control-Allow-Headers"
	Enter your website URL under "Access-Control-Allow-Origin"
	Select "Save"

11. Deploy the API
	Select "Deploy API"
	Understage select "New Stage"
	Name the Stage "Prod"
	Select Deploy
	Take Note of API URL and replace "YourAPIURL" within the index.html file

12. Setup DynamoDB Table
	Navigate to the DynamoDB service
	Select "Create table"
	Enter your Table name (Ex. UserResponses)
	Enter "id" as the Partition key
	Select Create table
	make sure to edit the lambda function with your DynamoDB table name

13. Attatch DynamoDBFullAccess Policy to Lambda
	Navigate to the Lambda service
	Select your function
	Select the "Configuration" tab
	Select "Permissions"
	Click the link under "Role name"
	Select "Add permissions" and "Attatch policies" in the drop down
	Search for "AmazonDynamoDBFullAccess" and select it
	Select Add permissions

14. Test for Correct functionality
	Open the website URL and Enter a First and Last name
	Select Submit
	If an error code of 200 appears then it is successful
	Navigate to DynamoDB and select "Explore table items"
	The entry should be stored
	
	



