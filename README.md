# Web detective
A Lambda-based project to process documents from the web.

# Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites
* Install the [Serverless Framework](https://serverless.com/framework/docs/providers/aws/guide/installation#installing-the-serverless-framework) - The framework used
* Set up [AWS Account credentials](https://serverless.com/framework/docs/providers/aws/guide/credentials#create-an-iam-user-and-access-key) to run serverless commands that interface with your AWS account
* Create a [Python 3.7](https://docs.aws.amazon.com/lambda/latest/dg/python-programming-model.html) environment
* Install the dependencies in the ``` requirements.txt ``` file
* Install the project ```package-lock.json ``` packages
* Replace the aws AccountID in ```serverless.yml``` with yours.


## Running the tests

To deploy the project for testing, run

```sls deploy```

## Versioning

I used [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/Jaxx0/web-detective/tags). 

[First Version](https://github.com/Jaxx0/web-detective/releases/tag/V1.0)

Receives a URL as an argument and makes a request to that URL. The Lambda function extracts the title from the HTML document in the response and returns it to the caller


[Second Version](https://github.com/Jaxx0/web-detective/releases/tag/V2.0)

Receives a URL as an argument and makes a request to that URL. The Lambda function stores the response body to an [S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingBucket.html) and also stores the extracted title as a record in a [DynamoDB table](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html) It then return the extracted title and the S3 URL of the stored response object.


[Third Version](https://github.com/Jaxx0/web-detective/releases/tag/V3.0)

This version accepts a URL as an argument, creates an identifier for the request, store the URL to a DynamoDB record keyed to that identifier, along with the state of “PENDING”, invokes the processing function [asynchronously](https://docs.aws.amazon.com/lambda/latest/dg/lambda-invocation.html) with the identifier, and returns the identifier to the client.
The proccessing function invoked receives the response, extracts the title and updates the DynamoDB record to include the S3 URL, extracted title, and update the state to “PROCESSED”.


[Fourth Version](https://github.com/Jaxx0/web-detective/releases/tag/V4.0

)
This version uses [DynamoDB streams](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html) instead of an explicit function invocation in the third version.


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details



