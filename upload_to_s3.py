import boto3
import logging
import os

# Initialize logger
from utils.custom_logger import get_logger
logger = get_logger("S3_Uploader")

# AWS Configuration
AWS_REGION = "eu-north-1"
BRONZE_BUCKET = "bronze-layer-bucket-12345"
SILVER_BUCKET = "silver-layer-bucket-12345"
GOLD_BUCKET = "gold-layer-bucket-12345"
S3_OBJECT_NAME = "transactions.parquet"

# Initialize S3 client
s3 = boto3.client('s3', region_name=AWS_REGION)

def upload_file():
    """Upload a file from local system to Bronze S3 bucket"""
    try:
        file_path = "data/sample/transactions.parquet"
        logger.info(f"Uploading {file_path} to S3 bucket {BRONZE_BUCKET}...")
        s3.upload_file(file_path, BRONZE_BUCKET, S3_OBJECT_NAME)
        logger.info(f"✅ File uploaded successfully to {BRONZE_BUCKET}/{S3_OBJECT_NAME}")
    except Exception as e:
        logger.error(f"❌ Error uploading file: {e}")

if __name__ == "__main__":
    # Step 1: Upload to Bronze (if not already uploaded)
    upload_file()
