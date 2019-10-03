import uuid
import boto3
from boto3.dynamodb.conditions import Key

"""variables are used """
current_region = boto3.session.Session().region_name
db = boto3.resource('dynamodb', region_name=current_region)


def post_record(title, table):
    """ This function receives the extracted title and table as an argument and stores it in the Table of DynamoDB"""

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


def create_partition_key():
    """  function generates a uuid to be used as the partition key in URLs Table of the NoSQL DynamoDB """

    # This generates a unique partition key between 3 to 63 chars long
    return str(uuid.uuid4())


def save_to_db(identifier, url, table):
    """This function stores the identifier and the URL to the table of the DynamoDB"""

    table = db.Table(str(table))
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


def get_URL_from_db(identifier, table):
    """This function retrieves a URL from the DynamoDB record that is associated with a given identifier"""

    table = db.Table(table)
    try:
        response = table.get_item(
            Key={
                'id': str(identifier),
            }
        )
    except Exception as e:
        return str(e)
    else:
        return response['Item']


def update_record(identifier, s3_url, title, table):
    """This function updates the DynamoDB record to include the s3 URL object,
            extracted title and updates the state to PROCESSED """

    table = db.Table(table)
    try:
        response = table.update_item(
            Key={
                'id': str(identifier)
            },
            UpdateExpression="SET s3_url = :s3, title = :t, #process_status=:ps",
            ExpressionAttributeNames ={"#process_status": "state"},
            ExpressionAttributeValues={
                ':s3': s3_url,
                ':t': title,
                ':ps': 'PROCESSED'
            },
            ReturnValues="UPDATED_NEW"
        )
    except Exception as e:
        return str(e)
    else:
        return response


def query(identifier, table):
    """ This function performs a query on the Table for data given an identifier"""

    table = db.Table(table)
    try:
        response = table.query(
            KeyConditionExpression=Key('identifier').eq(identifier))
    except Exception as e:
        return str(e)
    else:
        return response['Item']