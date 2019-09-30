import json
import os

from files.document_processor import crawler
from files.database_stores import post_record
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

            if db_store['ResponseMetadata']['HTTPStatusCode'] == 200 and bucket_store['ResponseMetadata']['HTTPStatusCode'] == 200:
                url = get_s3_object_url(bucket_name=os.environ['BUCKET_NAME'], file_name=file_name)
                body = dict(title=json.dumps(body['title']), url=url)
                return dict(statusCode=200, body=json.dumps(body))

        return dict(statusCode=200, body=json.dumps(event))

    except Exception as e:
        return dict(statusCode=200, body=str(e))
