import json
import boto3
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


s3 = boto3.client("s3")


BRONZE_BUCKET = "bronze-layer-bucket-12345"
SILVER_BUCKET = "silver-layer-bucket-12345"
GOLD_BUCKET = "gold-layer-bucket-12345"

def lambda_handler(event, context):
    """Triggered when a file is uploaded to Bronze bucket."""
    try:

        file_name = event["Records"][0]["s3"]["object"]["key"]
        logger.info(f"🔄 File detected: {file_name} in {BRONZE_BUCKET}")

        # Bronze → Silver გადატანა
        copy_source = {"Bucket": BRONZE_BUCKET, "Key": file_name}
        s3.copy_object(CopySource=copy_source, Bucket=SILVER_BUCKET, Key=file_name)
        logger.info(f"✅ File copied to Silver: {file_name}")

        # Silver → Gold გადატანა
        copy_source = {"Bucket": SILVER_BUCKET, "Key": file_name}
        s3.copy_object(CopySource=copy_source, Bucket=GOLD_BUCKET, Key=file_name)
        logger.info(f"✅ File copied to Gold: {file_name}")

        return {
            "statusCode": 200,
            "body": json.dumps("✅ S3 Processing Completed Successfully!")
        }

    except Exception as e:
        logger.error(f"❌ Error processing file: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error: {str(e)}")
        }
