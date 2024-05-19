import unittest
from datetime import datetime
import pandas as pd
import os
from data_loader.extractors.local_extractor import LocalExtractor

class TestLocalExtractor(unittest.TestCase):

    def setUp(self):
        # Crear un directorio de prueba y algunos archivos de prueba
        self.test_dir = 'test_data'
        os.makedirs(self.test_dir, exist_ok=True)
        self.file_paths = [
            os.path.join(self.test_dir, 'test_file_20240101.csv'),
            os.path.join(self.test_dir, 'test_file_20240201.xlsx')
        ]
        for file_path in self.file_paths:
            if file_path.endswith('.csv'):
                df = pd.DataFrame({'column1': [1, 2], 'column2': [3, 4]})
                df.to_csv(file_path, index=False)
            else:
                df = pd.DataFrame({'column1': [1, 2], 'column2': [3, 4]})
                df.to_excel(file_path, index=False)

    def tearDown(self):
        # Eliminar los archivos y el directorio de prueba
        for file_path in self.file_paths:
            os.remove(file_path)
        os.rmdir(self.test_dir)

    def test_extract_data(self):
        extractor = LocalExtractor(
            directory=self.test_dir,
            name_pattern='test_file_',
            date_from=datetime(2024, 1, 1),
            date_to=datetime(2024, 12, 31)
        )
        data = extractor.extract_data()
        self.assertEqual(len(data), 4)
        self.assertEqual(data[0].keys(), {'column1', 'column2'})

if __name__ == '__main__':
    unittest.main()
