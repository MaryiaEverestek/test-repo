import os
import logging
import boto3
from botocore.exceptions import ClientError

from config import aws_access_key_id, aws_secret_access_key #, region_name
from config import bucket_name, expiration



class AWSLoadS3:
    @staticmethod
    def get_credentials():
        """
        Returns the credentials for the service
        """
        credentials = {
        'aws_access_key_id': aws_access_key_id,
        'aws_secret_access_key': aws_secret_access_key,
        # 'region_name': region_name,
        }
        return credentials


    @staticmethod
    def get_client(name):
        """
        Returns the client for the service
        """
        credentials = AWSLoadS3.get_credentials()
        client = boto3.client(name, **credentials)
        return client


    @staticmethod
    def upload_file(file, bucket_name=bucket_name, object_name=None):
        """
        Uploads a file to S3 bucket
        """
        client = AWSLoadS3.get_client('s3')
        
        if object_name is None:
            object_name = os.path.basename(file.filename)
        try:
            client.upload_fileobj(file.file, Bucket=bucket_name, Key=object_name,
                                  ExtraArgs={
                                            'ContentDisposition': 'inline',
                                            'ContentType': 'application/pdf'})
        except ClientError as e:
            logging.error(e)
            return False
        
        url = AWSLoadS3.get_file_url(bucket_name=bucket_name, object_name=object_name, ExpiresIn=expiration)

        if url is None:
            return False
        
        return url


    @staticmethod
    def get_file_url(bucket_name=bucket_name, object_name=None, ExpiresIn=expiration):
        """
        Returns the URL of the file uploaded to S3 by the file_name
        """
        client = AWSLoadS3.get_client('s3')
        try:
            url = client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': object_name},
                ExpiresIn=ExpiresIn)
        except ClientError as e:
            logging.error(e)
            return None
        
        return url