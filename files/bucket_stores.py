import boto3
import json

""" Saves data to a file in the bucket"""


def save_to_s3(bucket_name, file_name, data):
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket_name, file_name)
    resp = obj.put(Body=json.dumps(data))
    return resp


""" Retrieves the s3 object URL of the stored data """


def get_s3_object_url():
    session = boto3.session.Session()
    current_region = session.region_name
    url = "https://{}.s3.{}.amazonaws.com/{}".format("scrapper-dev-uploads",
                                                     current_region, "scrapped-title")
    return url