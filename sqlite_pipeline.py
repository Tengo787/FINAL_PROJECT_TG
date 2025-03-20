import sqlite3
import pandas as pd
import os
from utils.custom_logger import get_logger

# Initialize logger
logger = get_logger("SQLite_ETL")

# Database file
DB_FILE = "data/transactions.db"

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

def create_tables():
    """
    Create SQLite3 tables for bronze, silver, and gold layers.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Create Bronze Layer (Raw Data)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bronze_transactions (
                transaction_id TEXT PRIMARY KEY,
                customer_id INTEGER,
                timestamp TEXT,
                amount REAL,
                transaction_type TEXT
            )
        """)

        # Create Silver Layer (Cleaned Data)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS silver_transactions (
                transaction_id TEXT PRIMARY KEY,
                customer_id INTEGER,
                timestamp TEXT,
                amount REAL CHECK(amount > 0),  -- No negative or zero values
                transaction_type TEXT
            )
        """)

        # Create Gold Layer (Aggregated Data)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gold_transactions (
                customer_id INTEGER PRIMARY KEY,
                total_transactions INTEGER,
                total_amount REAL,
                avg_amount REAL
            )
        """)

        conn.commit()
        conn.close()
        logger.info("✅ Tables created successfully.")

    except Exception as e:
        logger.error(f"❌ Error creating tables: {e}")

def load_bronze_layer():
    """
    Load data from Parquet into the Bronze layer.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        df = pd.read_parquet("data/sample/transactions.parquet")

        df.to_sql("bronze_transactions", conn, if_exists="replace", index=False)
        conn.close()
        logger.info("✅ Data loaded into Bronze layer successfully.")

    except Exception as e:
        logger.error(f"❌ Error loading data into Bronze layer: {e}")

def transform_silver_layer():
    """
    Transform data and load it into the Silver layer.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Data Cleaning & Validation (removing invalid amounts)
        cursor.execute("""
            INSERT INTO silver_transactions
            SELECT * FROM bronze_transactions
            WHERE amount > 0
        """)

        conn.commit()
        conn.close()
        logger.info("✅ Data transformed and loaded into Silver layer successfully.")

    except Exception as e:
        logger.error(f"❌ Error transforming data into Silver layer: {e}")

def aggregate_gold_layer():
    """
    Aggregate data and load it into the Gold layer.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Aggregation logic: total transactions, total amount, and average amount per customer
        cursor.execute("""
            INSERT INTO gold_transactions
            SELECT 
                customer_id,
                COUNT(transaction_id) AS total_transactions,
                SUM(amount) AS total_amount,
                AVG(amount) AS avg_amount
            FROM silver_transactions
            GROUP BY customer_id
        """)

        conn.commit()
        conn.close()
        logger.info("✅ Data aggregated and loaded into Gold layer successfully.")

    except Exception as e:
        logger.error(f"❌ Error aggregating data into Gold layer: {e}")

def run_etl():
    """
    Run the full ETL process: Bronze -> Silver -> Gold.
    """
    create_tables()
    load_bronze_layer()
    transform_silver_layer()
    aggregate_gold_layer()
    logger.info("🚀 ETL Pipeline completed successfully.")

if __name__ == "__main__":
    run_etl()
