import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import pandas as pd
from data_loader_lib import SFTPFileLoader

class TestSFTPFileLoader(unittest.TestCase):

    @patch('paramiko.Transport')
    @patch('paramiko.SFTPClient')
    def test_load_data(self, MockSFTPClient, MockTransport):
        # Mock the SFTP connection and file reading
        mock_transport_instance = MockTransport.return_value
        mock_sftp_client_instance = MockSFTPClient.from_transport.return_value
        mock_sftp_client_instance.listdir.return_value = ['test_file.csv']
        mock_sftp_client_instance.open.return_value = MagicMock()
        mock_sftp_client_instance.open.return_value.__enter__.return_value = MagicMock()
        mock_sftp_client_instance.open.return_value.__enter__.return_value.read.return_value = (
            b'column1,column2\n1,3\n2,4\n'
        )
        
        loader = SFTPFileLoader(
            hostname='sftp.example.com',
            port=22,
            username='user',
            password='pass',
            remote_path='/remote/path',
            name_pattern='test_file',
            date_from=datetime(2024, 1, 1),
            date_to=datetime(2024, 12, 31)
        )
        df = loader.load_data()
        self.assertEqual(len(df), 2)
        self.assertEqual(list(df.columns), ['column1', 'column2'])

if __name__ == '__main__':
    unittest.main()
