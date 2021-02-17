DynamoDB model

MVP
ID (uuid)
ServiceName
URL
most recent response (latest status code)


Final
ID
Service Name
data: {
    URL
    Type (webpage / API / others ?)
    Request Type (GET / POST / etc)
    Expected response
    MostRecentResponse
    TimeBetweenChecks ?
    CreatedDate
    CreatedBy ?
    ModifiedDate
    ModifiedBy ?
}



MVP
A SAM application that is able to test status codes for specified URL's and to send a notification to Teams if there is an error

Breakdown
DynamoDB to store list of services and expected results
Lambda function to get list and run test
webhook to send errors to Teams
Scheduled task to run the Lambda function at 30 second interval

If there is time in first sprint
    API's to control the dynamoDB


Incoming webhook url: https://hooks.slack.com/services/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


a scheduled lambda function that:
    GET's urls from table
    for each url
        check status code
        UPDATE table with most recent response
        if status code not 200
            send notification via webhook 




## First version
### app.py
get list of websites to check

foreach (url, previous_response) in websites:
	get status_code(url)
	if status_code != previous_response:
		update websites
		webhook(url, code)


### DynamoDB
{
    "ID": uuid(),
    "website": {
        "url": "https://www.northamptonshire.gov.uk",
        "previous_response": 200
    }
}