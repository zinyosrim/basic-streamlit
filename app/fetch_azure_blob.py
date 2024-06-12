import io
import logging
from azure.storage.blob import BlobClient

# Configure logging for the module
azure_logger = logging.getLogger('azure')
azure_logger.setLevel(logging.WARNING)

def fetch_azure_blob(data_url: str) -> io.BytesIO:
    """
    Fetches data from an Azure Blob Storage URL and returns it as a BytesIO stream.

    Parameters:
        data_url (str): The URL to the Azure blob item.

    Returns:
        io.BytesIO: A BytesIO stream containing the data from the Azure blob if successful.
    
    Raises:
        Exception: Propagates any exceptions that occur during the blob fetch process.
    """
    try:
        azure_logger.debug(f"Attempting to fetch data from Azure Blob at URL: {data_url}")
        blob_client = BlobClient.from_blob_url(blob_url=data_url)
        stream = io.BytesIO()
        bytes_fetched = blob_client.download_blob().readinto(stream)
        
        if bytes_fetched is None or bytes_fetched == 0:
            azure_logger.warning(f"No data fetched from URL: {data_url}")
            raise ValueError("No data was fetched from the blob storage, the blob may be empty.")
        
        stream.seek(0)
        azure_logger.info(f"Data successfully fetched from URL: {data_url}")
        return stream
    except Exception as e:
        azure_logger.error(f"Failed to fetch data from Azure Blob Storage due to: {e}", exc_info=True)
        raise  # Re-raise the caught exception after logging
