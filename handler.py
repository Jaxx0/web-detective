import json
from files.document_processor import crawler


def document_crawler(event, context):

    """ This function receives a URL as an argument from the API gateway
    (query?=url input by user ) and passes it to the crawler function"""

    if event['httpMethod'] == 'GET' and event['queryStringParameters']['query']:
        url = event['queryStringParameters']['query']
        body = crawler(url)
        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }
        return response
    return dict(statusCode=200, body=json.dumps(event))
