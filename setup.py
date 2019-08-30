from pip._vendor.urllib3 import packages
from setuptools import setup, find_packages

setup(
    name='CatastroInspireDownloader',
    version='0.1.1',
    install_requires=[
        'Click==7.0',
        'atoma',
        'requests==2.22.0',
    ],
    author="Francisco P. Sampayo",
    author_email="francisco.perez@geomati.co",
    description="Herramienta para descargar datos Inspire del Catastro de España a través de Atom.",
    packages=find_packages(include=['cidownloader']),
    entry_points='''
        [console_scripts]
        cidownloader=cidownloader.cli:cli
    ''',
    license='GPLv3',
)
