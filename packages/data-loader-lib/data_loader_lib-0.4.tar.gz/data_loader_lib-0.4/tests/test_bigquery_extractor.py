import unittest
from unittest.mock import patch
import pandas as pd
from data_loader.extractors.bigquery_extractor import BigQueryExtractor

class TestBigQueryExtractor(unittest.TestCase):

    @patch('google.cloud.bigquery.Client')
    def test_extract_data(self, MockBigQueryClient):
        # Mock the BigQuery client and query execution
        mock_client_instance = MockBigQueryClient.return_value
        mock_query_job = mock_client_instance.query.return_value
        mock_query_job.to_dataframe.return_value = pd.DataFrame({
            'column1': [1, 2],
            'column2': [3, 4]
        })

        extractor = BigQueryExtractor(
            project_id='my_project',
            query='SELECT * FROM my_dataset.my_table'
        )
        data = extractor.extract_data()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0].keys(), {'column1', 'column2'})

if __name__ == '__main__':
    unittest.main()
