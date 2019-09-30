import uuid

import boto3
import json

""" Saves data to a file in the bucket"""


def save_to_s3(bucket_name, file_name, data):
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket_name, file_name)
    resp = obj.put(Body=json.dumps(data))
    return resp


""" Retrieves the s3 object URL of the stored data """


def get_s3_object_url(bucket_name, file_name,):
    session = boto3.session.Session()
    current_region = session.region_name
    url = "https://{}.s3.{}.amazonaws.com/{}".format(str(bucket_name),
                                                     current_region, str(file_name))
    return url


""" This fucntion generates a unique universal id to use as filename"""


def create_file_name():
    # This generates a name that is between 3 to 63 chars long
    return str(uuid.uuid4())