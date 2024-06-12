import os
import unittest

class TestEnvironmentVariable(unittest.TestCase):
    def test_cloud_data_url(self):
        self.assertIsNotNone(os.getenv("CLOUD_DATA_URL"), "CLOUD_DATA_URL is not set.")

if __name__ == '__main__':
    unittest.main()