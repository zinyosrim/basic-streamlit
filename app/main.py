import os
import io
import pandas as pd
import logging
from azure.storage.blob import BlobClient
from azure.core.exceptions import AzureError, HttpResponseError, ResourceNotFoundError

# General logger configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Get the logger for the Azure SDK and set its level to WARNING to suppress INFO logs
azure_logger = logging.getLogger('azure')
azure_logger.setLevel(logging.WARNING)

def dataframe_from_azure_blob_csv() -> pd.DataFrame:
    """
    Fetches a CSV file from Azure Blob Storage and returns it as a pandas DataFrame.
    This function uses the SAS URL stored in the CLOUD_DATA_URL environment variable.

    Returns:
        pd.DataFrame: The loaded data as a pandas DataFrame, or None if any error occurs.
    """
    try:
        data_url = os.getenv('CLOUD_DATA_URL')
        
        if not data_url:
            logging.error("Environment variable CLOUD_DATA_URL is not set.")
            return None

        logging.info("Starting blob download...")
        blob_client = BlobClient.from_blob_url(blob_url=data_url)
        stream = io.BytesIO()
        blob_client.download_blob().readinto(stream)
        
        stream.seek(0)
        df = pd.read_csv(stream)
        logging.info("Blob download completed successfully.")
        return df

    except HttpResponseError as e:
        logging.error(f"Network error occurred: {e}")
        return None
    except ResourceNotFoundError as e:
        logging.error(f"Blob not found: {e}")
        return None
    except AzureError as e:
        logging.error(f"Azure-specific error occurred: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None

def main():
    """
    Main function to execute the script logic.
    It retrieves a DataFrame from Azure Blob Storage and prints the head if data is available.
    """
    df = dataframe_from_azure_blob_csv()

    # Check if DataFrame was not created
    if df is None:
        logging.info("Failed to load data.")
        return  # Exit the function as there's no data to process
    
    # Check if the DataFrame is empty
    if df.empty:
        logging.info("Data loaded but the DataFrame is empty.")
    else:
        print(df.head())  # Print the first few rows of the DataFrame


if __name__ == '__main__':
    main()
