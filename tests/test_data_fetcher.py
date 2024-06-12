import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from io import BytesIO
from app.data_fetcher import dataframe_from_azure_blob_csv

class TestBlobStorageDataframe(unittest.TestCase):
    def setUp(self):
        # Sample data to be used as a response from Blob Storage
        self.sample_csv_data = "name,age\nAlice,24\nBob,30"
        self.sample_data_stream = BytesIO(self.sample_csv_data.encode())
        self.test_url = "https://fakeurl.com/fake_sas_token"

    @patch('app.data_fetcher.BlobClient')
    def test_dataframe_from_azure_blob_csv_success(self, mock_blob_client):
        # Setup the mock to return a stream containing the CSV data
        mock_blob = MagicMock()
        # Ensure that readinto correctly handles the byte stream
        mock_blob.download_blob().readinto.side_effect = lambda x: x.write(self.sample_data_stream.getvalue())
        mock_blob_client.from_blob_url.return_value = mock_blob

        # Pass the test URL directly to the function
        df = dataframe_from_azure_blob_csv(self.test_url)
        
        # Check if DataFrame is correctly loaded
        expected_df = pd.read_csv(BytesIO(self.sample_csv_data.encode()))
        pd.testing.assert_frame_equal(df, expected_df)

    @patch('app.data_fetcher.BlobClient')
    def test_dataframe_from_azure_blob_csv_failure(self, mock_blob_client):
        mock_blob = MagicMock()
        mock_blob.download_blob().readinto.side_effect = Exception("Network error")
        mock_blob_client.from_blob_url.return_value = mock_blob

        result = dataframe_from_azure_blob_csv(self.test_url)
        self.assertIsNone(result, "Expected None when a network error occurs")


if __name__ == '__main__':
    unittest.main()
