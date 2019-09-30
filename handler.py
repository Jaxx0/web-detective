import json
import os

from files.document_processor import crawler
from files.database_stores import post_record, create_partition_key, save_to_db, get_URL_from_db
from files.bucket_stores import create_file_name, save_to_s3, get_s3_object_url

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
            # url = "https://www.wikipedia.com"

            identifier = create_partition_key()  # created identifier
            db_store = save_to_db(identifier, url, table=os.environ['URL_TABLE_NAME'])  # saves url keyed to the identifier

            # Stores url to bucket with an identifier filename
            file_name = create_file_name()  # The name the file is stored under
            bucket_store = save_to_s3(bucket_name=os.environ['BUCKET_NAME'], file_name=identifier, data=url)

            if db_store['ResponseMetadata']['HTTPStatusCode'] == 200 and bucket_store['ResponseMetadata']['HTTPStatusCode'] == 200:
                # To Do - Invoke processing function asynchronously
                return dict(statusCode=200, body=json.dumps(identifier))
            return dict(statusCode=200, body=json.dumps(event))

    except Exception as e:
        return dict(statusCode=200, body=str(e))


""" This CLIENT function receives the identifier, reads the URL from the DynamoDB record keyed to that identifier, 
    makes a request to that URL. It then processes the response to extract the title as before, 
    and updates the DynamoDB record to include the S3 URL, extracted title, and updates the state to “PROCESSED”. """


def get_url_given_identifier(event, context):
    try:
        if event['httpMethod'] == 'GET' and event['queryStringParameters']['query']:
            identifier = event['queryStringParameters']['query']  # input identifier from the API gateway

            obj = get_URL_from_db(identifier, table=os.environ['URL_TABLE_NAME'])  # retrieved URL from the database
            response = crawler(obj['url'])  # response from the request processor

            title = response['title']
            s3_url = get_s3_object_url(os.environ['BUCKET_NAME'], file_name=identifier)
            response = update_record(identifier, s3_url, title)
            return dict(statusCode=200, body=json.dumps(response))
            return dict(statusCode=200, body=json.dumps(obj))

    except Exception as e:
        return dict(statusCode=200, body=str(e))