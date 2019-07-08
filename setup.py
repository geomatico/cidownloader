from setuptools import setup

setup(
    name='CatastroInspireDownloader',
    version='0.1',
    py_modules=['cadastral_inspire_downloader'],
    install_requires=[
        'Click==7.0',
        'atoma',
        'GDAL>=2.3.3',
        'requests==2.22.0',
    ],

    author="Francisco P. Sampayo",
    author_email="fpsampayo@gmail.com",
    description="Herramienta para descargar datos Inspire del Catastro de España a través de Atom.",
    entry_points='''
        [console_scripts]
        cidownloader=cadastral_inspire_downloader:cli
    ''',
)