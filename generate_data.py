import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta
from tqdm import tqdm
import os
from utils.custom_logger import get_logger  # Importing custom logger

# Initialize logger
logger = get_logger("Data_Generator")

# Set up Faker and random seeds for reproducibility
fake = Faker()
random.seed(42)
np.random.seed(42)

# Define constants
NUM_RECORDS = 25000
TRANSACTION_TYPES = ["purchase", "refund", "transfer", "withdrawal", "deposit"]
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 3, 18)

def generate_transaction_data(num_records):
    """
    Generate synthetic transaction data.

    Args:
        num_records (int): Number of transaction records to generate.

    Returns:
        pd.DataFrame: A DataFrame containing the generated transaction data.
    """
    try:
        logger.info("🚀 Starting data generation for {} records...".format(num_records))
        data = []

        for _ in tqdm(range(num_records), desc="Generating Transactions"):
            transaction_id = fake.uuid4()
            customer_id = fake.random_int(min=1000, max=9999)
            timestamp = fake.date_time_between(start_date=START_DATE, end_date=END_DATE)
            amount = round(random.uniform(5, 5000), 2)  # Amount range: 5-5000
            transaction_type = random.choice(TRANSACTION_TYPES)

            data.append({
                "transaction_id": transaction_id,
                "customer_id": customer_id,
                "timestamp": timestamp,
                "amount": amount,
                "transaction_type": transaction_type
            })

        logger.info("✅ Data generation completed successfully.")
        return pd.DataFrame(data)

    except Exception as e:
        logger.error("❌ Error during data generation: {}".format(e))
        return pd.DataFrame()

# Ensure the output directory exists
os.makedirs("data/sample", exist_ok=True)

# Generate transaction data
df = generate_transaction_data(NUM_RECORDS)

# Save data to Parquet format
try:
    df.to_parquet("data/sample/transactions.parquet", engine="pyarrow", index=False)
    logger.info("✅ Data successfully saved to 'data/sample/transactions.parquet'")
except Exception as e:
    logger.error("❌ Error saving Parquet file: {}".format(e))
