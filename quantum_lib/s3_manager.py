import boto3

class S3Manager:
    def __init__(self, config):
        self.s3_client = boto3.client('s3')
        self.bucket_name = config['S3']['BucketName']


    def create_bucket(self):
        self.s3_client.create_bucket(Bucket=self.bucket_name)


    def delete_bucket(self):
        bucket = boto3.resource('s3').Bucket(self.bucket_name)
        for obj in bucket.objects.all():
            obj.delete()
        self.s3_client.delete_bucket(Bucket=self.bucket_name)

