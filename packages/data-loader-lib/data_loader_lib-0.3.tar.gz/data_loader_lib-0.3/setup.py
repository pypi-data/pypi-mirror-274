import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.3'
PACKAGE_NAME = 'data_loader_lib'
AUTHOR = 'Ricardo Reyes'
AUTHOR_EMAIL = 'reyesramirezcardoemanuel@gmail.com'
URL = 'https://github.com/tu-usuario-github/data_loader_lib'

LICENSE = 'MIT'
DESCRIPTION = 'Librería para cargar datos desde diferentes fuentes en un DataFrame'
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8')
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
    'pandas',
    'paramiko',
    'sqlalchemy',
    'google-cloud-bigquery',
    'injector',
    'python-dotenv',
    'matplotlib'
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(where='data_loader'),
    package_dir={'': 'data_loader'},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
