import uuid

import boto3

""" This function receives the extracted title and table as an argument and stores it in the Table of DynamoDB"""


def post_record(title, table):
    current_region = boto3.session.Session().region_name
    db = boto3.resource('dynamodb', region_name=current_region)

    table = db.Table(table)
    try:
        response = table.put_item(
            Item={
                'title': title
            }
        )
    except Exception as e:
        return str(e)
    else:
        return response


"""  function generates a uuid to be used as the partition key in URLs Table of the NoSQL DynamoDB """


def create_partition_key():
    # This generates a unique partition key between 3 to 63 chars long
    return str(uuid.uuid4())


"""This function stores the identifier and the URL to the table of the DynamoDB"""


def save_to_db(identifier, url, table):
    current_region = boto3.session.Session().region_name
    db = boto3.resource('dynamodb', region_name=current_region)
    table = db.Table(table)
    try:
        response = table.put_item(
            Item={
                'id': str(identifier),
                'url': url,
                'state': 'PENDING'
            }
        )
    except Exception as e:
        return str(e)
    else:
        return response