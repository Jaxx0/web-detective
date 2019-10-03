import uuid

import boto3
import json


def save_to_s3(bucket_name, file_name, data):
    """ Saves data to a file in the bucket
    bucket_name - - The name of the bucket you're saving to
    file_name   - -  The name of the file
    data         - - data to be saved """

    s3 = boto3.resource('s3')
    obj = s3.Object(bucket_name, file_name)
    resp = obj.put(Body=json.dumps(data))
    return resp


def get_s3_object_url(bucket_name, file_name,):
    """ Retrieves the s3 object URL of the stored data
    bucket_name - - The name of the bucket you're saving to
    file_name   - -  The name of the file """

    session = boto3.session.Session()
    current_region = session.region_name
    url = "https://{}.s3.{}.amazonaws.com/{}".format(str(bucket_name),
                                                     current_region, str(file_name))
    return url


def create_file_name():
    """ This function generates a unique universal id to use as filename"""
    # This generates a name that is between 3 to 63 chars long
    return str(uuid.uuid4())