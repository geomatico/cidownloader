import click

from cidownloader.cadastral_inspire_downloader import atom_urls, download

"""
CLI para el uso del cidownloader
"""


@click.command()
@click.option('--provincia', '-p', default=None, type=click.INT, help='Código Gerencia Catastro. Si no se indica '
                                                                      'descarga todas las provincias.')
@click.option('--municipio', '-m', default=None, type=click.INT, help='Código Municipio Catastro. Si no se indica '
                                                                      'descarga todos los municipios.')
@click.option('--srs', default=None, type=click.INT, help='Código EPSG final. Si no se indica, '
                                                          'se mantendrá el de origen.')
@click.option('--tipo', default='all', type=click.Choice(['all', 'parcels', 'buildings', 'addresses']),
              help='Tipo Cartografía a descargar.')
@click.option('--filename', default="buildings", help='Nombre Geopackage')
@click.option('--separar_salida', '-s', flag_value=True, is_flag=True, help='Separar salida a un '
                                                                            'GeoPackage por Provincia')
@click.version_option()
def cli(provincia, municipio, tipo, srs, filename, separar_salida):
    """Catastro Inspire Downloader.

    Utilidad que permite descargar cartografía del
    servicio inspire de la Dirección General de Catastro.

    Genera un fichero GeoPackage.

    """

    if tipo == 'all':
        for key, url in atom_urls.items():
            print('Comenzando descarga de {}:'.format(key))
            download(data_to_download=url, provincia=provincia, municipio=municipio, srs=srs, filename=filename,
                     separar_salida=separar_salida)
    else:
        url = atom_urls[tipo]
        print('Comenzando descarga de {}:'.format(tipo))
        download(data_to_download=url, provincia=provincia, municipio=municipio, srs=srs, filename=filename,
                 separar_salida=separar_salida)
