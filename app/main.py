import os
import pandas as pd
import logging
from app.data_fetcher import dataframe_from_azure_blob_csv
from azure.storage.blob import BlobClient
from azure.core.exceptions import AzureError, HttpResponseError, ResourceNotFoundError

# General logger configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    Main function to execute the script logic.
    It retrieves a DataFrame from Azure Blob Storage and prints the head if data is available.
    """
    data_url = os.getenv('CLOUD_DATA_URL')
    if not data_url:
        logging.error("CLOUD_DATA_URL environment variable is not set.")
    else:
        df = dataframe_from_azure_blob_csv(data_url)
        if df.empty:
            logging.info("Data loaded but the DataFrame is empty.")
        else:
            print(df.head())  # Print the first few rows of the DataFrame



if __name__ == '__main__':
    main()
