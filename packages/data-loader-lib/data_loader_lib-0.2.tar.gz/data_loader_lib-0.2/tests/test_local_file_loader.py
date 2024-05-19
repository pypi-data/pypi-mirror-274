import unittest
from datetime import datetime
import pandas as pd
from data_loader_lib import LocalFileLoader

# Verificar que data_loader_lib está en sys.path
import sys
print(f"Current sys.path in test_local_file_loader: {sys.path}")

class TestLocalFileLoader(unittest.TestCase):

    def setUp(self):
        # Crear un directorio de prueba y algunos archivos de prueba
        self.test_dir = 'test_data'
        os.makedirs(self.test_dir, exist_ok=True)
        self.file_paths = [
            os.path.join(self.test_dir, 'test_file_1.csv'),
            os.path.join(self.test_dir, 'test_file_2.csv')
        ]
        for file_path in self.file_paths:
            df = pd.DataFrame({'column1': [1, 2], 'column2': [3, 4]})
            df.to_csv(file_path, index=False)

    def tearDown(self):
        # Eliminar los archivos y el directorio de prueba
        for file_path in self.file_paths:
            os.remove(file_path)
        os.rmdir(self.test_dir)

    def test_load_data(self):
        loader = LocalFileLoader(
            directory=self.test_dir,
            name_pattern='test_file_',
            date_from=datetime(2024, 1, 1),
            date_to=datetime(2024, 12, 31)
        )
        df = loader.load_data()
        self.assertEqual(len(df), 4)
        self.assertEqual(list(df.columns), ['column1', 'column2'])

if __name__ == '__main__':
    unittest.main()
