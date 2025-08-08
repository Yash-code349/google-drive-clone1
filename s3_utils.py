import boto3
import os

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = "ap-south-1"
S3_BUCKET = "google-drive-clone-devs3-2025"

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

def upload_to_s3(file):
    try:
        s3_client.upload_fileobj(
            file,
            S3_BUCKET,
            file.filename,
        )
        url = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{file.filename}"
        return url
    except Exception as e:
        print("Upload to S3 failed:", e)
        return None

def delete_from_s3(filename):
    try:
        s3_client.delete_object(Bucket=S3_BUCKET, Key=filename)
        return True
    except Exception as e:
        print("Delete from S3 failed:", e)
        return False

