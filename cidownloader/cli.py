import argparse
from cadastral_inspire_downloader import atom_urls, download

def main():
    parser = argparse.ArgumentParser(prog='cidownloader', description=    
    """
    Catastro Inspire Downloader.
    Utilidad que permite descargar cartografía del servicio inspire de la Dirección General de Catastro.
    Genera un fichero GeoPackage.
    """)
    
    parser.add_argument('--provincia', '-p', default=None, type=int, choices=[2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,21,22,
                                                                23,24,25,26,27,28,29,30,32,33,34,35,36,37,38,39,
                                                                40,41,42,43,44,45,46,47,49,50,51,52], help='Código Gerencia Catastro de la provincia que se desea descargar')
    parser.add_argument('-m','--municipio' , default=None, type=int, help='Código Municipio Catastro del municipio que se desea descargar')
    parser.add_argument('--srs', default=None, type=int, help='Código EPSG final para la proyección de las coordenadas')
    parser.add_argument('-t','--tipo', default='all', choices=['all', 'parcels', 'buildings', 'addresses'], help='Tipo Cartografía a descargar')
    parser.add_argument('-f','--filename', default='buildings', help='Nombre Geopackage de salida')
    parser.add_argument('--separar_salida', '-s', action='store_true', help='Separar salida a un GeoPackage por Provincia')

    args = parser.parse_args()

    if args.tipo == 'all':
        for key, url in atom_urls.items():
            print('Comenzando descarga de {}:'.format(key))
            download(data_to_download=url, provincia=args.provincia, municipio=args.municipio, srs=args.srs, filename=args.filename,
                     separar_salida=args.separar_salida)
    else:
        url = atom_urls[args.tipo]
        print('Comenzando descarga de {}:'.format(args.tipo))
        download(data_to_download=url, provincia=args.provincia, municipio=args.municipio, srs=args.srs, filename=args.filename,
                 separar_salida=args.separar_salida)

if __name__ == '__main__':
    main()
