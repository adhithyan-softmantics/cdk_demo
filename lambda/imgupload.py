import boto3
import os
from botocore.exceptions import ClientError

s3 = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    try:
        # Get the raw binary data from the request body
        image_content = event.get('body', None)
        if not image_content:
            return {
                "statusCode": 400,
                "body": "No image content found in the request body"
            }

        # Ensure the content type is set correctly
        content_type = event.get('headers', {}).get('content-type', 'image/jpeg')

        # Generate a unique filename
        file_name = "uploaded_image.jpg"

        # Upload the file to the S3 bucket
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=image_content,
            ContentType=content_type
        )

        return {
            "statusCode": 200,
            "body": f"Image successfully uploaded to {BUCKET_NAME} as {file_name}"
        }

    except ClientError as e:
        return {
            "statusCode": 500,
            "body": f"Error uploading image: {str(e)}"
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Unexpected error: {str(e)}"
        }
