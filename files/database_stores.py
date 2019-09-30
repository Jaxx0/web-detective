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