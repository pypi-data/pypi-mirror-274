import unittest
from unittest.mock import patch
import pandas as pd
from data_loader_lib import BigQueryLoader

class TestBigQueryLoader(unittest.TestCase):

    @patch('google.cloud.bigquery.Client')
    def test_load_data(self, MockBigQueryClient):
        # Mock the BigQuery client and query execution
        mock_client_instance = MockBigQueryClient.return_value
        mock_query_job = mock_client_instance.query.return_value
        mock_query_job.result.return_value = [
            {'column1': 1, 'column2': 3},
            {'column1': 2, 'column2': 4}
        ]

        loader = BigQueryLoader(
            project_id='my_project',
            query='SELECT * FROM my_dataset.my_table'
        )
        df = loader.load_data()
        self.assertEqual(len(df), 2)
        self.assertEqual(list(df.columns), ['column1', 'column2'])

if __name__ == '__main__':
    unittest.main()
