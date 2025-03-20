provider "aws" {
  region = "eu-north-1"
}

# =========================
# 🥉 Bronze Bucket
# =========================
resource "aws_s3_bucket" "bronze_bucket" {
  bucket = "bronze-layer-bucket-12345"
}

resource "aws_s3_bucket_policy" "bronze_policy" {
  bucket = aws_s3_bucket.bronze_bucket.id
  policy = <<POLICY
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": "*",
        "Action": ["s3:GetObject", "s3:PutObject"],
        "Resource": "arn:aws:s3:::bronze-layer-bucket-12345/*"
      }
    ]
  }
  POLICY
}

# =========================
# 🥈 Silver Bucket
# =========================
resource "aws_s3_bucket" "silver_bucket" {
  bucket = "silver-layer-bucket-12345"
}

resource "aws_s3_bucket_policy" "silver_policy" {
  bucket = aws_s3_bucket.silver_bucket.id
  policy = <<POLICY
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": "*",
        "Action": ["s3:GetObject", "s3:PutObject"],
        "Resource": "arn:aws:s3:::silver-layer-bucket-12345/*"
      }
    ]
  }
  POLICY
}

# =========================
# 🥇 Gold Bucket
# =========================
resource "aws_s3_bucket" "gold_bucket" {
  bucket = "gold-layer-bucket-12345"
}

resource "aws_s3_bucket_policy" "gold_policy" {
  bucket = aws_s3_bucket.gold_bucket.id
  policy = <<POLICY
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": "*",
        "Action": ["s3:GetObject", "s3:PutObject"],
        "Resource": "arn:aws:s3:::gold-layer-bucket-12345/*"
      }
    ]
  }
  POLICY
}

# =========================
# 🔑 IAM
# =========================
resource "aws_iam_role" "lambda_role" {
  name = "lambda_s3_trigger_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = { Service = "lambda.amazonaws.com" },
        Action = "sts:AssumeRole"
      }
    ]
  })
}


resource "aws_iam_policy" "lambda_s3_policy" {
  name        = "lambda_s3_policy"
  description = "Policy to allow Lambda function to access S3 buckets"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:CopyObject",
          "s3:ListBucket"
        ],
        Resource = [
          "arn:aws:s3:::bronze-layer-bucket-12345/*",
          "arn:aws:s3:::silver-layer-bucket-12345/*",
          "arn:aws:s3:::gold-layer-bucket-12345/*"
        ]
      }
    ]
  })
}

# IAM
resource "aws_iam_role_policy_attachment" "lambda_s3_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_s3_policy.arn
}

# =========================
# 🏗️ Lambda
# =========================
resource "aws_lambda_function" "s3_trigger_lambda" {
  function_name = "S3FileProcessor"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.9"
  timeout       = 30

  filename         = "lambda_function.zip"
  source_code_hash = filebase64sha256("lambda_function.zip")
}

# =========================
# 🔔 S3 Event Trigger 
# =========================
resource "aws_s3_bucket_notification" "bronze_trigger" {
  bucket = aws_s3_bucket.bronze_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.s3_trigger_lambda.arn
    events              = ["s3:ObjectCreated:*"]
  }
}
