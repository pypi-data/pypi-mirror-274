# 📦 Data Loader Library

[![PyPI version](https://badge.fury.io/py/data_loader_lib.svg)](https://badge.fury.io/py/data_loader_lib)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Data Loader Library es una librería de Python para cargar datos desde diversas fuentes a un DataFrame de pandas.

## 🚀 Instalación

Usa el gestor de paquetes [pip](https://pip.pypa.io/en/stable/) para instalar `data_loader_lib`.

```bash
pip install data_loader_lib
```

## 📄 Descripción

Data Loader Library proporciona una forma sencilla de cargar datos desde diferentes fuentes como archivos locales, servidores SFTP y BigQuery en un DataFrame de pandas. Esto facilita el procesamiento y análisis de datos en Python.

## 🛠️ Uso

### LocalFileLoader

```python
from data_loader_lib import LocalFileLoader
from datetime import datetime

local_loader = LocalFileLoader(
    directory='data',
    name_pattern='file_',
    date_from=datetime(2024, 1, 1),
    date_to=datetime(2024, 12, 31)
)
df = local_loader.load_data()
print(df)
```

### SFTPFileLoader

```python
from data_loader_lib import SFTPFileLoader
from datetime import datetime

sftp_loader = SFTPFileLoader(
    hostname='sftp.example.com',
    port=22,
    username='user',
    password='pass',
    remote_path='/remote/path',
    name_pattern='file_',
    date_from=datetime(2024, 1, 1),
    date_to=datetime(2024, 12, 31)
)
df = sftp_loader.load_data()
print(df)
```

### BigQueryLoader

```python
from data_loader_lib import BigQueryLoader

bq_loader = BigQueryLoader(
    project_id='my_project',
    query='SELECT * FROM my_dataset.my_table'
)
df = bq_loader.load_data()
print(df)
```

## 🔧 Configuración

### .env

Crea un archivo `.env` en el directorio raíz de tu proyecto para almacenar las credenciales y configuraciones:

```env
SFTP_HOSTNAME=sftp.example.com
SFTP_PORT=22
SFTP_USERNAME=user
SFTP_PASSWORD=pass
BQ_PROJECT_ID=my_project
```

## 🧪 Testing

Para ejecutar las pruebas unitarias, usa `pytest`:

```bash
pytest
```

## 📜 Licencia

Este proyecto está licenciado bajo la licencia MIT. Consulta el archivo [LICENSE](https://choosealicense.com/licenses/mit/) para obtener más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes, abre un problema primero para discutir lo que te gustaría cambiar.

Asegúrate de actualizar las pruebas según sea necesario.

## ✨ Créditos

- Autor: Ricardo Reyes
- Correo: reyesramirezcardoemanuel@gmail.com
- GitHub: [devsmart3](https://github.com/devsmart3)