import os
import boto3
import uuid

def create_bucket_name(bucket_prefix):
    # The generated bucket name must be between 3 and 63 chars long
    return ''.join([bucket_prefix, str(uuid.uuid4())])


def create_s3_bucket(bucket_prefix, s3_connection):
    """ Create an s3 bucket in your current region


    """
    session = boto3.session.Session()
    current_region = session.region_name
    if current_region == 'us-east-1':
        location_constraint = 'us-west-2'
    else:
        location_constraint = region
    bucket_name = create_bucket_name(bucket_prefix)
    bucket_response = s3_connection.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': location_constraint})
    print(bucket_name, current_region)
    return bucket_name, bucket_response


def upload_file(file, **kwargs):
    """
    uploads a file to s3
    """
    if os.path.getmtime(file) < os.path.getmtime(kwargs['time_stamp_file']):
        return None

    # Replace windows slashes with unix slashes
    local_key = file.replace(kwargs['master_directory'], "")
    key = local_key.replace("\\", "/")
    print(key)
    # Remove first /
    if key.startswith("/"):
        key = key[1:]
    print('uploading {} with relative path {} in s3...'.format(file, key))
    res = kwargs['bucket'].Object(key).upload_file(file)
    print('s3 returned :', res)
    return res


def upload_dir(path, **kwargs):
    """
    Uploads directory recursively to s3
    """
    for file in os.listdir(path):

        filepath = os.path.join(path, file)
        if os.path.isdir(filepath) is True:
            upload_dir(filepath, **kwargs)
        else:
            upload_file(filepath, **kwargs)
