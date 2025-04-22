from app.domain.AWS.interfaces import S3ImageUploaderInterface
import aioboto3
import uuid
import logging
import imghdr
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os

load_dotenv()

BUCKET_NAME = os.getenv("BUCKET_NAME")
REGION_NAME = os.getenv("REGION_NAME")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")

session_kwargs = {
    "region_name":REGION_NAME,
    "aws_access_key_id": AWS_ACCESS_KEY,
    "aws_secret_access_key": AWS_SECRET_KEY
}

class S3ImageUploaderAdapter(S3ImageUploaderInterface):
    # def __init__(self, bucket_name: str, region_name: str, aws_access_key_id: str, aws_secret_access_key: str):
    #     self.bucket_name = bucket_name
        
    #     # Store session parameters
    #     self.session_kwargs = {}
    #     if region_name:
    #         self.session_kwargs['region_name'] = region_name
    #     if aws_access_key_id and aws_secret_access_key:
    #         self.session_kwargs['aws_access_key_id'] = aws_access_key_id
    #         self.session_kwargs['aws_secret_access_key'] = aws_secret_access_key

    async def upload_image(self, image_bytes: bytes, folder: str, content_type=None):

        file_type = imghdr.what(None, h=image_bytes)
        print(f"นี่คือ filetype ของ upload_image {file_type}")

        filename = f"{uuid.uuid4()}.{file_type}"
        
        # Create the full path (key) for the image
        if folder:
            key = f"{folder}/{filename}"
        else:
            key = filename
            
        # Determine content type if not provided
        if content_type is None:
            content_type = f"image/{file_type}"
            
        # Set extra args for the upload
        extra_args = {
            'ContentType': content_type
        }
        
        session = aioboto3.Session(**session_kwargs)
        
        try:
            async with session.client('s3') as s3_client:
                # Upload the file
                await s3_client.put_object(
                    Bucket=BUCKET_NAME,
                    Key=key,
                    Body=image_bytes,
                    **extra_args
                )
                
                # Generate URL
                url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{key}"
                logging.info(f"Successfully uploaded image to {url}")
                return url
                
        except ClientError as e:
            print(f"Error uploading image to S3: {e}")