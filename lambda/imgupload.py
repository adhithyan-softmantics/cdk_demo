 
import boto3
import base64
import os
from botocore.exceptions import ClientError

s3 = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    try:
        # Read the image from the request body (base64-encoded)
        image_content = event.get('body')
        if not image_content:
            return {
                "statusCode": 400,
                "body": "No image content found in the request body"
            }

        # Decode the base64-encoded image
        image_data = base64.b64decode(image_content)
          # Use a timestamp to create a unique filename
        timestamp = int(time.time())
        file_name = f"uploaded_image_{timestamp}.jpg"

        # Upload the image to S3
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
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
