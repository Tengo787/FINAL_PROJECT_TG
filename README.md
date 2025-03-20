# 🚀 FINAL_PROJECT_TG

📌 **Final Data Engineering Project**  
This project implements a **data pipeline** using **SQLite3, AWS S3, Terraform, and Python** while following the **Medallion Architecture** (Bronze/Silver/Gold).

## 🏗️ Project Structure

FINAL_PROJECT_TG │── data/ # Data folder │ ├── sample/ # Sample datasets │ │ ├── transactions.parquet │ │ ├── transactions.db │── logs/ # Logging directory │── terraform/ # Infrastructure as Code (IaC) │ ├── main.tf # Terraform config │ ├── lambda_function.py # AWS Lambda function │── utils/ # Helper scripts │ ├── custom_logger.py # Custom logging module │── venv/ # Virtual environment │── .gitignore # Git ignored files │── generate_data.py # Data generation script │── sqlite_pipeline.py # SQLite ETL pipeline │── upload_to_s3.py # AWS S3 upload script │── README.md # Project documentation