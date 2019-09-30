import json
from files.document_processor import crawler
from files.database_stores import post_record

""" This function receives a URL as an argument from the API gateway and passes it to the crawler function"""


def document_crawler(event, context):
    if event['httpMethod'] == 'GET' and event['queryStringParameters']['query']:
        url = event['queryStringParameters']['query']
        body = crawler(url)
        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }
        # To Do - Store body to bucket and extracted title to titles table in DynamoDb
        data = post_record(body['title']) # Stores extracted title to DB

    return dict(statusCode=200, body=json.dumps(event))
