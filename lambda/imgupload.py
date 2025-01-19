 
import boto3
import base64
import os
from botocore.exceptions import ClientError

s3 = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    try:
        image_path = "/var/task/test_image.jpg" 
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        # Upload the image to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key="uploaded_image.jpg",
            Body=image_data,
            ContentType="image/jpeg"
        )

        return {
            "statusCode": 200,
            "body": "Image successfully uploaded to the bucket!"
        }

    except ClientError as e:
        return {
            "statusCode": 500,
            "body": str(e)
        }
