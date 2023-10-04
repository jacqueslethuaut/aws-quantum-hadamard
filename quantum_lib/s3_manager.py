# MIT License

# Copyright (c) 2023 Jacques Le Thuaut


import boto3
import json

class S3Manager:
    def __init__(self, config):
        self.s3_client = boto3.client('s3')
        self.bucket_name = config['S3']['BucketName']
        self.prefix = config['S3']['Prefix']


    def bucket_exists(self):
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            return True
        except:
            return False
        
    def create_bucket_if_not_exists(self):
        if not self.bucket_exists():
            self.s3_client.create_bucket(
                Bucket=self.bucket_name,
                CreateBucketConfiguration={'LocationConstraint': 'eu-west-2'}  
            )
    
    def save_to_s3(self, data, key):
        full_key = f"{self.prefix}/{key}"
        self.s3_client.put_object(Body=json.dumps(data), Bucket=self.bucket_name, Key=full_key)


    def delete_bucket(self):
        bucket = boto3.resource('s3').Bucket(self.bucket_name)
        for obj in bucket.objects.all():
            obj.delete()
        self.s3_client.delete_bucket(Bucket=self.bucket_name)

