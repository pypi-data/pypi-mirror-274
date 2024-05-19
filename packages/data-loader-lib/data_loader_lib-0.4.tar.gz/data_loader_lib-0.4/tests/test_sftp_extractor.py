import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from data_loader.extractors.sftp_extractor import SFTPExtractor

class TestSFTPExtractor(unittest.TestCase):

    @patch('paramiko.Transport')
    @patch('paramiko.SFTPClient')
    def test_extract_data_csv(self, MockSFTPClient, MockTransport):
        # Mock the SFTP connection and file reading for CSV
        mock_transport_instance = MockTransport.return_value
        mock_sftp_client_instance = MockSFTPClient.from_transport.return_value
        mock_sftp_client_instance.listdir.return_value = ['test_file_20240101.csv']
        mock_sftp_file = MagicMock()
        mock_sftp_file.__enter__.return_value.read.return_value = b'column1,column2\n1,3\n2,4\n'
        mock_sftp_client_instance.open.return_value = mock_sftp_file

        extractor = SFTPExtractor(
            hostname='sftp.example.com',
            port=22,
            username='user',
            password='pass',
            remote_path='/remote/path',
            name_pattern='test_file_',
            date_from=datetime(2024, 1, 1),
            date_to=datetime(2024, 12, 31)
        )
        data = extractor.extract_data()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0].keys(), {'column1', 'column2'})

    @patch('paramiko.Transport')
    @patch('paramiko.SFTPClient')
    def test_extract_data_xlsx(self, MockSFTPClient, MockTransport):
        # Mock the SFTP connection and file reading for XLSX
        mock_transport_instance = MockTransport.return_value
        mock_sftp_client_instance = MockSFTPClient.from_transport.return_value
        mock_sftp_client_instance.listdir.return_value = ['test_file_20240101.xlsx']
        mock_sftp_file = MagicMock()
        excel_content = b'\x50\x4b\x03\x04\x14\x00\x06\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        mock_sftp_file.__enter__.return_value.read.return_value = excel_content
        mock_sftp_client_instance.open.return_value = mock_sftp_file

        with patch('pandas.read_excel') as mock_read_excel:
            mock_read_excel.return_value = pd.DataFrame({
                'column1': [1, 2],
                'column2': [3, 4]
            })

            extractor = SFTPExtractor(
                hostname='sftp.example.com',
                port=22,
                username='user',
                password='pass',
                remote_path='/remote/path',
                name_pattern='test_file_',
                date_from=datetime(2024, 1, 1),
                date_to=datetime(2024, 12, 31)
            )
            data = extractor.extract_data()
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0].keys(), {'column1', 'column2'})

if __name__ == '__main__':
    unittest.main()
