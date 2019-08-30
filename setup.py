from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='CatastroInspireDownloader',
    version='0.2.0',
    install_requires=[
        'Click==7.0',
        'atoma',
        'requests==2.22.0',
    ],
    author="Francisco P. Sampayo",
    author_email="francisco.perez@geomati.co",
    description="Herramienta para descargar datos Inspire del Catastro de España a través de Atom.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(include=['cidownloader']),
    entry_points='''
        [console_scripts]
        cidownloader=cidownloader.cli:cli
    ''',
    license='GPLv3',
    url="https://github.com/geomatico/cidownloader",
)
