import atoma
import requests
import os
import subprocess
from urllib import request, parse
import zipfile
import shutil

atom_urls = {
    'parcels': 'https://www.catastro.hacienda.gob.es/INSPIRE/CadastralParcels/ES.SDGC.CP.atom.xml',
    'buildings': 'https://www.catastro.hacienda.gob.es/INSPIRE/buildings/ES.SDGC.BU.atom.xml',
    'addresses': 'https://www.catastro.hacienda.gob.es/INSPIRE/Addresses/ES.SDGC.AD.atom.xml'
}


class ProcessMunicipalityException(Exception):
    pass



def format_codmun(provincia, municipio):
    """Obtiene el código de municipio a partir de la provincia y el municipio"""
    return str(provincia).zfill(2) + str(municipio).zfill(3)


def parse_url(url):
    """Codifica la URL. parse.quote('abc def') -> 'abc%20def'"""

    url = parse.urlsplit(url)
    url = list(url)
    url[2] = parse.quote(url[2])
    parsed_url = parse.urlunsplit(url)
    return parsed_url


def download_and_process_municipality(url, epsg, output_gpkg, to_epsg=None):
    """
    Descarga un gml de catastro a partir de una url y un epgs.
    Lo convierte a geopackage.
    Permite declarar un epsg de destino.
    """
    if not to_epsg:
        to_epsg = epsg

    try:
        try:
            os.makedirs('downloads')
        except:
            pass
        filename, headers = request.urlretrieve(url)
        with zipfile.ZipFile(os.path.join(filename), "r") as z:
            z.extractall(path=os.path.join(os.curdir, 'downloads'))
        for gml in os.listdir('downloads'):
            if os.path.splitext(gml)[1] == '.gml':
                layer_name = gml.split('.')[5]
                ogr_cmd = """ogr2ogr -update -append -f GPKG -s_srs EPSG:{} -t_srs EPSG:{} -lco IDENTIFIER={} {} {}""" \
                    .format(epsg, to_epsg, layer_name, output_gpkg + '.gpkg', os.path.join('downloads', gml))
                # print ("\n Executing: ", ogr_cmd)
                subprocess.run(ogr_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print("Error: {}".format(str(e)))
    finally:
        shutil.rmtree('downloads')


def get_municipality_atoms_url(atom_url, codmun=None):
    """
    Lee el atom específico para cada parroquia. 
    
    Devuelve el url del Atom de cada municipio con su epsg.

    Se puede pasar un parámetro codmun para devolver sólo este municipio.
    """

    response = requests.get(atom_url)

    feed = atoma.parse_atom_bytes(response.content)

    urls = []
    for entry in feed.entries:
        url = parse_url(entry.links[0].href)
        epsg = entry.categories[0].term.split('/')[-1]
        codmun_atom = os.path.basename(url).split('.')[4]

        if codmun is None or codmun == codmun_atom:
            urls.append((url, epsg))

    return urls


def get_provinces_atoms_url(url, province_code=None):
    """
    Lee el atom general de Catastro Inspire que contiene los diferentes
    Atoms para cada provincia.

    Devuelve una lista con url a los atoms y el título.
    """
    response = requests.get(url)
    feed = atoma.parse_atom_bytes(response.content)

    atoms_provincias = []

    for entry in feed.entries:
        if province_code is not None:
            if os.path.basename(entry.links[0].href).split('.')[3] == 'atom_{}'.format(str(province_code).zfill(2)):
                url = parse_url(entry.links[0].href)
                title = entry.title.value
                atoms_provincias.append((url, title))
        else:
            url = parse_url(entry.links[0].href)
            title = entry.title.value
            atoms_provincias.append((url, title))

    return atoms_provincias


def download(data_to_download, provincia=None, municipio=None, srs=None, filename="buildings", separar_salida=False):
    atoms_provincias = get_provinces_atoms_url(data_to_download, provincia)
    codmun = format_codmun(provincia, municipio) if municipio is not None else None

    geopackage_name = filename
    current_prov = 0
    total_prov = len(atoms_provincias)
    for atom in atoms_provincias:
        current_prov += 1
        prov_title = atom[1]
        prov_url = atom[0]
        print(prov_title)
        urls = get_municipality_atoms_url(prov_url, codmun=codmun)

        current_mun = 0
        total_mun = len(urls)
        for url in urls:
            current_mun += 1
            print('[{}/{}][{}/{}] Downloading {}'.format(current_prov, total_prov, current_mun, total_mun, url[0]))
            if separar_salida:
                geopackage_name = '_'.join([filename, prov_title.replace(' ', '_')])
            download_and_process_municipality(url[0], url[1], geopackage_name, to_epsg=srs)

if __name__ == "__main__":
    download(data_to_download=atom_urls['buildings'], provincia=36, municipio=31)