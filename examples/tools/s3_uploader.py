
from base import ToolBase, ToolArgument, ToolOutput
import os
import boto3

class S3Uploader(ToolBase):
    name = "s3_uploader"
    description = "Upload .docx to S3"
    arguments = [
        ToolArgument("filename", "string", True, "Path to docx"),
        ToolArgument("bucket", "string", True, "S3 bucket"),
        ToolArgument("key", "string", True, "S3 key")
    ]

    def run(self, arguments):
        s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_DEFAULT_REGION", "ap-southeast-1")
        )
        s3.upload_file(arguments["filename"], arguments["bucket"], arguments["key"])
        return ToolOutput(content=f"✅ Uploaded to s3://{arguments['bucket']}/{arguments['key']}")
