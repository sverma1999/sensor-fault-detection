import os

import boto3

from sensor.constant.env_variables import (
    AWS_ACCESS_KEY_ID_ENV_KEY,
    AWS_SECRET_ACCESS_KEY_ENV_KEY,
    REGION_NAME,
)


class S3Client:
    s3_client = None
    s3_resource = None

    def __init__(self, region_name=REGION_NAME):
        if S3Client.s3_resource == None or S3Client.s3_client == None:
            __access_key_id = os.getenv(
                AWS_ACCESS_KEY_ID_ENV_KEY,
            )

            __secret_access_key = os.getenv(
                AWS_SECRET_ACCESS_KEY_ENV_KEY,
            )

            if __access_key_id == None:
                raise Exception(
                    f"Environment variable: {AWS_ACCESS_KEY_ID_ENV_KEY} is not not set."
                )

            if __secret_access_key is None:
                raise Exception(
                    f"Environment variable: {AWS_SECRET_ACCESS_KEY_ENV_KEY} is not set."
                )

            # boto3.resource() returns a high-level service resource object that represents an Amazon S3 bucket
            S3Client.s3_resource = boto3.resource(
                "s3",
                aws_access_key_id=__access_key_id,
                aws_secret_access_key=__secret_access_key,
                region_name=region_name,
            )

            # boto3.client() returns a low-level client object, which is a direct proxy to the service
            S3Client.s3_client = boto3.client(
                "s3",
                aws_access_key_id=__access_key_id,
                aws_secret_access_key=__secret_access_key,
                region_name=region_name,
            )
        # Storing the client and resource in the class variables
        self.s3_client = S3Client.s3_client
        self.s3_resource = S3Client.s3_resource
