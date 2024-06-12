import unittest
from unittest.mock import patch, MagicMock
import io
from app.fetch_azure_blob import fetch_azure_blob

class TestFetchAzureBlob(unittest.TestCase):

    def test_fetch_azure_blob_success(self):
        """
        Test that fetching from Azure blob storage successfully returns a BytesIO stream.
        This test ensures that the function returns a correctly filled BytesIO object when BlobClient works as expected.
        """
        test_url = "https://fakeazureblobstorage.blob.core.windows.net/mycontainer/myblob.csv..."
        expected_data = b"test data"
        mock_stream = io.BytesIO()
        mock_stream.write(expected_data)
        mock_stream.seek(0)

        # Mocking the BlobClient and configuring it to mimic successful data fetching
        with patch('app.fetch_azure_blob.BlobClient') as mock_blob_client:
            mock_blob = MagicMock()
            mock_blob.download_blob().readinto.side_effect = lambda x: x.write(expected_data)
            mock_blob_client.from_blob_url.return_value = mock_blob
            
            result = fetch_azure_blob(test_url)
            result.seek(0)  # Reset the stream position for reading
            self.assertEqual(result.read(), expected_data)

    def test_fetch_azure_blob_failure(self):
        """
        Test that exceptions are handled properly when network errors occur.
        This test checks that the correct exception is raised and the error message is as expected.
        """
        test_url = "https://fakeazureblobstorage.blob.core.windows.net/mycontainer/myblob.csv..."

        # Mocking the BlobClient to raise an exception simulating a network error
        with patch('app.fetch_azure_blob.BlobClient.from_blob_url', side_effect=Exception("Network error")):
            with self.assertRaises(Exception) as context:
                fetch_azure_blob(test_url)
            # Check that the exception message matches the expected message
            self.assertEqual(str(context.exception), "Network error")

if __name__ == '__main__':
    unittest.main()
