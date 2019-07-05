import atoma, requests, os, subprocess
from urllib import request, parse
import zipfile
import shutil

prov = '36'
output_gpkg = 'buildings.gpkg'

catinspire_parcels_url = 'http://www.catastro.minhap.es/INSPIRE/CadastralParcels/{prov}/ES.SDGC.CP.atom_{prov}.xml'
catinspire_address_url = 'http://www.catastro.minhap.es/INSPIRE/addresses/{prov}/ES.SDGC.ad.atom_{prov}.xml'
catinspire_building_url = 'http://www.catastro.minhap.es/INSPIRE/buildings/{prov}/ES.SDGC.bu.atom_{prov}.xml'

def format_codmun(provincia, municipio):
    return str(provincia).zfill(2) + str(municipio).zfill(3)

def parseurl(url):

    url = parse.urlsplit(url)
    url = list(url)
    url[2] = parse.quote(url[2])
    parsed_url = parse.urlunsplit(url)
    return parsed_url

def download_municipio(url, epsg):
    try:
        try:
            os.makedirs('downloads')
        except:
            pass
        filename, headers = request.urlretrieve(url)
        with zipfile.ZipFile(os.path.join(filename) , "r") as z:
            z.extractall(path=os.path.join(os.curdir, 'downloads'))
        for gml in os.listdir('downloads'):
            if os.path.splitext(gml)[1] == '.gml':
                layername = gml.split('.')[5]
                ogr_cmd = """ogr2ogr -update -append -f GPKG -s_srs EPSG:{} -t_srs EPSG:4326 -lco IDENTIFIER={} {} {}""".format(epsg, layername, output_gpkg, os.path.join('downloads', gml))
                # print ("\n Executing: ", ogr_cmd)
                subprocess.run(ogr_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print("Error: {}".format(str(e)))
    finally:
        shutil.rmtree('downloads')

def read_prov_atom(atom_url, title, codmun=None):

    response = requests.get(atom_url)

    feed = atoma.parse_atom_bytes(response.content)

    urls = []
    for entry in feed.entries:
        url = parseurl(entry.links[0].href)
        epsg = entry.categories[0].term.split('/')[-1]
        codmun_atom = os.path.basename(url).split('.')[4]

        if codmun is None or codmun == codmun_atom:
            urls.append((url, epsg))

    current = 0
    total = len(feed.entries)

    for url in urls:
        current += 1
        print('[{}/{}] Downloading {}'.format(current, total, url[0]))
        download_municipio(url[0], url[1])

def read_complete_atom(provincia=None, municipio=None):

    url = 'http://www.catastro.minhap.es/INSPIRE/buildings/ES.SDGC.BU.atom.xml'
    response = requests.get(url)
    feed = atoma.parse_atom_bytes(response.content)

    for entry in feed.entries:
        if provincia != None:
            if os.path.basename(entry.links[0].href).split('.')[3] == 'atom_{}'.format(str(provincia).zfill(2)):
                url = parseurl(entry.links[0].href)
                title = entry.title.value
                print(title)
                codmun = format_codmun(provincia, municipio) if municipio is not None else None
                read_prov_atom(url, title, codmun)
        else:
            url = parseurl(entry.links[0].href)
            title = entry.title.value
            print(title)
            read_prov_atom(url, title)

read_complete_atom(36)
