import os
import pandas as pd
import logging
from fetch_data import fetch_data
from fetch_azure_blob import fetch_azure_blob


# General logger configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    Main function to execute the script logic.
    It retrieves a DataFrame from Azure Blob Storage and prints the head if data is available.
    """
    data_url = os.getenv('CLOUD_DATA_URL')
    
    # Early exit if the environment variable is not set
    if not data_url:
        logging.error("CLOUD_DATA_URL environment variable is not set.")
        return  # Exit the function early

    df = fetch_data(data_url, fetch_azure_blob)

    # Check if the DataFrame is empty and handle this case early
    if df is None or df.empty:
        logging.info("Data loaded but the DataFrame is empty or None.")
        return  # Exit the function early

    # If everything is fine, print the first few rows of the DataFrame
    print(df.head())

if __name__ == '__main__':
    main()
