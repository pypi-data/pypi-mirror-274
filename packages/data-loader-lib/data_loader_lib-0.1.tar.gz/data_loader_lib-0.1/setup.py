# setup.py
from setuptools import setup, find_packages

setup(
    name="data_loader_lib",
    version="0.1",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "pandas",
        "paramiko",
        "sqlalchemy",
        "google-cloud-bigquery",
        "injector"
    ],
    author="Tu Nombre",
    author_email="reyesramirezricardoemanuel@gmail.com",
    description="Librería para cargar datos desde diferentes fuentes en un DataFrame",
    url="http://onbotgo.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
