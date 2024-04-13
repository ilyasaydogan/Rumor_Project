import boto3
import os
from datetime import datetime,timedelta

def upload_to_s3(file_path, folder_name):

    aws_access_key_id = ""
    aws_secret_access_key = ""
    bucket_name = 'rumors3'

    file_name = os.path.basename(file_path)
    
    object_key = folder_name + file_name
    
    s3 = boto3.client('s3', 
                      aws_access_key_id=aws_access_key_id, 
                      aws_secret_access_key=aws_secret_access_key)
    
    s3.upload_file(file_path, bucket_name, object_key)

