import boto3


def post_record(title):
    current_region = boto3.session.Session().region_name
    db = boto3.resource('dynamodb', region_name=current_region)

    table = db.Table('titles')
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