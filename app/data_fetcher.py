import io
import pandas as pd
import logging
from azure.storage.blob import BlobClient
from azure.core.exceptions import HttpResponseError, ResourceNotFoundError, AzureError

azure_logger = logging.getLogger('azure')
azure_logger.setLevel(logging.WARNING)

def dataframe_from_azure_blob_csv(data_url: str) -> pd.DataFrame:
    """
    Fetches a CSV file from Azure Blob Storage and returns it as a pandas DataFrame.
    This function requires a SAS URL to be passed as a parameter.

    Parameters:
        data_url (str): The SAS URL to the blob storage containing the CSV file.

    Returns:
        pd.DataFrame: The loaded data as a pandas DataFrame, or None if any error occurs.
    """
    if not data_url:
        logging.error("Data URL must be provided.")
        return None

    try:
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

