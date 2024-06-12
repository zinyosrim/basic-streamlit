import unittest
from unittest.mock import patch, MagicMock
import io
import pandas as pd
from app.fetch_data import fetch_data 

class TestFetchData(unittest.TestCase):

    def setUp(self):
        self.data_url = "https://example.com/data.csv"
        self.good_data = "name,age\nAlice,24\nBob,30"
        self.mock_stream = io.BytesIO(self.good_data.encode())

    @patch('app.fetch_data.logging')
    def test_fetch_data_success(self, mock_logging):
        """
        Test successful data fetch and DataFrame creation.
        """
        def mock_fetcher(url):
            return io.BytesIO(self.good_data.encode())

        df = fetch_data(self.data_url, mock_fetcher)

        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)  # Expecting two rows
        mock_logging.info.assert_called_with("Attempting to fetch data from data URL")
        mock_logging.debug.assert_called_with("Data stream successfully retrieved, loading into DataFrame.")

    @patch('app.fetch_data.logging')
    def test_fetch_data_no_stream(self, mock_logging):
        """
        Test the scenario where no valid data stream is returned.
        """
        def mock_fetcher(url):
            return None  # Simulating no data stream returned

        df = fetch_data(self.data_url, mock_fetcher)

        self.assertIsNone(df)
        mock_logging.warning.assert_called_with(f"No data stream returned from fetcher function for URL: {self.data_url}")


    @patch('app.fetch_data.logging')
    def test_fetch_data_unexpected_error(self, mock_logging):
        """
        Test handling of an unexpected error.
        """
        def mock_fetcher(url):
            raise Exception("Network error")

        with self.assertRaises(Exception) as context:
            fetch_data(self.data_url, mock_fetcher)
        
        self.assertEqual(str(context.exception), "Network error")
        mock_logging.exception.assert_called_with(f"Unexpected error fetching data from URL: {self.data_url}")

if __name__ == '__main__':
    unittest.main()
