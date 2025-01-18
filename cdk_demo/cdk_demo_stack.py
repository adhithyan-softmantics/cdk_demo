from aws_cdk import (
    App,
    Stack,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    RemovalPolicy,
)

class cdkdemostack(Stack):
    def __init__(self, scope: App, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create an S3 bucket
        bucket = s3.Bucket(
            self,
            "ImageBucket",
            bucket_name="imgbucket",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,  # Cleanup on stack deletion
            auto_delete_objects=True,  # Automatically delete bucket objects
        )

        # Create a Lambda function
        lambda_function = _lambda.Function(
            self,
            "UploadImageLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="imgupload.lambda_handler",  # Lambda handler function
            code=_lambda.Code.from_asset("lambda"),  # handler location
            environment={
                "BUCKET_NAME": bucket.bucket_name,  # Use the actual bucket name from the S3 bucket object
            },
        )

        # Grant the Lambda function permissions to write to the S3 bucket
        bucket.grant_put(lambda_function)

        # Create an API Gateway to trigger the Lambda function
        api = apigateway.LambdaRestApi(
            self,
            "ImageUploadApi",
            handler=lambda_function,
            proxy=False,
        )

        # Add a POST method for the API
        image_upload_resource = api.root.add_resource("upload")
        image_upload_resource.add_method("POST")  # POST method triggers the Lambda


