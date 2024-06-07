import pandas as pd
from azure.storage.blob import BlobClient
import io

SAS_URL = "https://dualcitizenstrgacct.blob.core.windows.net/langerchen/langerchen-order-data.csv?sv=2021-10-04&st=2024-06-04T12%3A17%3A38Z&se=2024-06-05T12%3A17%3A38Z&sr=b&sp=r&sig=eYqPornelBWX87kpmfQK746ZI0mk3W9XQ0ga%2FI6yXBU%3D"

def dataframe_from_azure_blob_csv(sas_url: str) -> pd.DataFrame:
    
    # Initialize a BlobClient with the SAS URL
    blob_client = BlobClient.from_blob_url(blob_url=sas_url)

    # Download the blob to a local memory stream
    stream = io.BytesIO()
    blob_client.download_blob().readinto(stream)

    # Seek to the beginning of the stream
    stream.seek(0)

    # Load the stream into a pandas DataFrame
    df = pd.read_csv(stream)

    return df


df = dataframe_from_azure_blob_csv(SAS_URL)
print(df.head())