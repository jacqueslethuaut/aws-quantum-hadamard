# MIT License

# Copyright (c) 2023 Jacques Le Thuaut

import os
import boto3
import json
import zipfile

from botocore.exceptions import ClientError


class IAMManager:
    def __init__(self, config):
        self.iam_client = boto3.client('iam')
        self.lambda_client = boto3.client('lambda')
        self.config = config
        self.lambda_config = self.config.get('Lambda', {})
        self.lambda_function_name = self.lambda_config.get('FunctionName', 'YourLambdaFunctionName')
    
    def role_exists(self, role_name):
        try:
            self.iam_client.get_role(RoleName=role_name)
            return True
        except self.iam_client.exceptions.NoSuchEntityException:
            return False
    
    def create_roles(self):
        for role_config in self.config['IAMRoles']:
            role_name = role_config['RoleName']
            policies = role_config['Policies']
            assume_role_policy_document = json.dumps({
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Effect': 'Allow',
                        'Principal': {'Service': 'braket.amazonaws.com'},
                        'Action': 'sts:AssumeRole'
                    }
                ]
            })
            
            if not self.role_exists(role_name):
                self.iam_client.create_role(
                    RoleName=role_name,
                    AssumeRolePolicyDocument=assume_role_policy_document
                )
                print(f"Role {role_name} created.")
                
                for policy in policies:
                    self.iam_client.attach_role_policy(
                        RoleName=role_name,
                        PolicyArn=f"arn:aws:iam::aws:policy/{policy}"
                    )
            else:
                print(f"Role {role_name} already exists.")

    def create_lambda_function(self, lambda_file_path):
        handler = self.lambda_config.get('Handler', 'lambda_function.handler')
        
        # Fetch the role ARN for the last role in the IAMRoles list.
        role_name = self.config['IAMRoles'][-1]['RoleName']
        role_arn = self.iam_client.get_role(RoleName=role_name)['Role']['Arn']
        
        head, tail = os.path.split(lambda_file_path)
        name, ext = os.path.splitext(tail)
        zip_file_path = os.path.join(head, name+".zip")

        if not os.path.exists(lambda_file_path):
            raise FileNotFoundError(f"Lambda function file not found at {lambda_file_path}")

        with zipfile.ZipFile(zip_file_path, 'w') as z:
            z.write(lambda_file_path, os.path.basename(lambda_file_path))

        with open(zip_file_path, "rb") as f:
            zipped_code = f.read()

        try:
            self.lambda_client.create_function(
                FunctionName=self.lambda_function_name,
                Runtime="python3.10",
                Role=role_arn,
                Handler=handler,
                Code={'ZipFile': zipped_code},
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceConflictException':
                print(f"Function {self.lambda_function_name} already exists. Updating the function code.")
                self.lambda_client.update_function_code(
                    FunctionName=self.lambda_function_name,
                    ZipFile=zipped_code
                )
            else:
                print(f"Unexpected error: {e}")
        

    def delete_lambda_function(self):
        self.lambda_client.delete_function(FunctionName=self.lambda_function_name)
