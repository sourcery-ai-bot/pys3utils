"""
Module to download git repo and upload it to Amazon s3
Configure the bucket, and git url using the settings file
Ths also requires AWS credentials to be set up in a file (or using AWS CLI):
Unix: ~/.aws/credentials
Windows: C:\\Users\\Username\\.aws\\credentials
In this file put the following:
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
[default]
region=us-east-1
"""

import os
import boto3
import stat
import sys
import time
from utils import upload_dir


def remove_readonly(func, path, excinfo):
    """
    Changes permissions on files that can't be deleted
    by shutil.rmtree
    """
    os.chmod(path, stat.S_IWRITE)
    func(path)


def main():
    if not sys.argv[1]:
        logger.critical('You must provide a directory to push!')
        exit(1)

    directory = os.path.abspath(sys.argv[1])
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(sys.argv[2])
    syncfile = os.path.join(directory,'.s3_sync_timestamp')
    try:
        print("uploading directory {}".format(directory))
        print('-----------------------------------------')
        with open(syncfile, 'w+') as f:
            ts = time.time()
            f.write('last updated/pushed to s3:'+ str(ts))

        upload_dir(directory, bucket=bucket, master_directory=directory, time_stamp_file=syncfile)

    except Exception as ex:
        print(ex)

    return

if __name__ == "__main__":
    main()

# OLD for cloning and pushing
#
# # Create temp directory
# print("Creating temporary directory %s" % settings.TEMP_DIRECTORY)
# if not os.path.exists(settings.TEMP_DIRECTORY):
#     os.makedirs(settings.TEMP_DIRECTORY)
# # Clone repository to temp directory
# print("Cloning repository from %s" % settings.GIT_URL)
# Repo.clone_from(settings.GIT_URL, settings.TEMP_DIRECTORY)
#
# # Uploads contents of temp directory to s3
# print("Uploading to S3")
# upload_dir(settings.TEMP_DIRECTORY)
#     finally:
#         # Deletes temporary directory
#         print("Deleting temporary directory and contents")
#         shutil.rmtree(settings.TEMP_DIRECTORY, onerror=remove_readonly)