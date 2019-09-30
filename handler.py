import json
import os

import boto3

from files.document_processor import crawler
from files.bucket_stores import create_file_name, save_to_s3, get_s3_object_url
from files.database_stores import post_record, create_partition_key, save_to_db, get_URL_from_db, update_record, query

"""This function receives a URL as an argument from the API gateway and passes it to the crawler function It then 
stores the response to an s3 bucket an a DynamoDB and returns the extracted title and the S3 URL of the stored 
response object """


def document_crawler(event, context):
    try:
        if event['httpMethod'] == 'GET' and event['queryStringParameters']['query']:
            url = event['queryStringParameters']['query']
            body = crawler(url)
            response = {
                "statusCode": 200,
                "body": json.dumps(body)
            }
            # Stores extracted title to DB
            db_store = post_record(body['title'], table=str(os.environ['TABLE_NAME']))

            # Stores body to bucket
            file_name = create_file_name()  # The name the file is stored under
            bucket_store = save_to_s3(bucket_name=os.environ['BUCKET_NAME'], file_name=file_name, data=response['body'])

            # Returns the extracted title and the S3 URL of the stored response object

            if db_store['ResponseMetadata']['HTTPStatusCode'] == 200 and bucket_store['ResponseMetadata'][
                'HTTPStatusCode'] == 200:
                url = get_s3_object_url(bucket_name=os.environ['BUCKET_NAME'], file_name=file_name)
                body = dict(title=json.dumps(body['title']), url=url)
                return dict(statusCode=200, body=json.dumps(body))

        return dict(statusCode=200, body=json.dumps(event))

    except Exception as e:
        return dict(statusCode=200, body=str(e))


""" This Lambda function receives a URL as an argument, creates an identifier for the request, stores the URL in a 
DynamoDB record keyed to that identifier, along with the state of “PENDING”, invokes the processing function
 ​asynchronously​ with the identifier, and returns the identifier to the client. """


def post_url_and_identity(event, context):
    try:
        if event['httpMethod'] == 'GET' and event['queryStringParameters']['query']:
            url = event['queryStringParameters']['query']

            identifier = create_partition_key()  # created identifier
            db_store = save_to_db(identifier, url, table=os.environ['URL_TABLE_NAME'])  # saves url keyed to the identifier

            # Stores url to bucket with an identifier filename
            bucket_store = save_to_s3(bucket_name=os.environ['BUCKET_NAME'], file_name=identifier, data=url)

            if db_store['ResponseMetadata']['HTTPStatusCode'] == 200 and bucket_store['ResponseMetadata']['HTTPStatusCode'] == 200:
                return dict(statusCode=200, body=json.dumps(identifier))
            return dict(statusCode=200, body=json.dumps(event))

    except Exception as e:
        return dict(statusCode=200, body=str(e))


""" This function gets called whenever the database table gets populated with a data record
    It retrieves the identifier to retrieve the URL, makes a request to the URL to obtain a response and 
    processes the response to extract the title and obtain the s3 URL of the response object and then
                            updates the status to "PROCESSED" """


def dynamo_trigger_stream(event, context):
    try:
        current_region = boto3.session.Session().region_name
        db = boto3.resource('dynamodb', region_name=current_region)
        table = db.Table(os.environ['URL_TABLE_NAME'])
        response = table.scan()
        for resp in response['Items']:
            if resp['state'] == "PENDING":
                id = resp['id']
                url = resp['url']
                response = crawler(url)
                title = response['title']
                s3_url = get_s3_object_url(os.environ['BUCKET_NAME'], file_name=id)
                response = update_record(id, s3_url, title, table=os.environ['URL_TABLE_NAME'])
                return dict(statusCode=200, body=json.dumps(response))

    except Exception as e:
        return dict(statusCode=200, body=str(e))