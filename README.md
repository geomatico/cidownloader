# Catastro Inspire Downloader

Herramienta para descargar datos del servicio ATOM [Inspire de Catastro](http://www.catastro.minhap.es/webinspire/index.html) y convertirlo en [GeoPackage](https://www.geopackage.org/).

> Necesita disponer de GDAL >= 2.3.3. y Python 3

## Usar la CLI

Para instalar:

```bash
pip install CatastroInspireDownloader
```

Para ejecutar:

```bash
$ cidownloader --help

Usage: cidownloader [OPTIONS]

  Catastro Inspire Downloader.

  Utilidad que permite descargar cartografía del  servicio inspire de la
  Dirección General de Catastro.

  Genera un fichero GeoPackage.

Options:
  -p, --provincia INTEGER         Código Gerencia Catastro. Si no se indica descarga todas las provincias.
  -m, --municipio INTEGER         Código Municipio Catastro. Si no se indica descarga todos los municipios.
  --srs INTEGER                   Código EPSG final. Si no se indica, se mantendrá el de origen.
  --tipo [all|parcels|buildings|addresses] Tipo Cartografía a descargar. Default: 'all'
  --filename TEXT                 Nombre Geopackage sin la extensión
  -s, --separar_salida            Separar salida a un GeoPackage por Provincia
  --version                       Show the version and exit.
  --help                          Show this message and exit.
```

Si se ejecuta sin opciones descarga todos los municipios de España y genera un GeoPackage llamado `buildings.gpkg` de unos 25 Gb.

Un ejemplo de uso sería

```bash
cidownloader -p 36 -m 62 --srs 25829
```

## Generar MVTs desde el GeoPackage

Se puede generar un fichero mbtiles de [Mapbox Vector Tiles](https://docs.mapbox.com/vector-tiles/reference/) con las construcciones de catastro:

```bash
ogr2ogr -f "MVT" -dsco MINZOOM=14 -dsco MAXZOOM=16 -lco "NAME=buildingparts" -sql "SELECT localID AS id, substr(localid, 0, 15) as parcel, numberOfFloorsAboveGround AS floors, geom FROM BuildingPart WHERE numberOfFloorsAboveGround > 0" buildings.mbtiles buildings.gpkg
```


## Build

```bash
python3 -m pip install --upgrade build
python3 -m build
```

## Publish

```bash
python3 -m pip install --upgrade twine
python3 -m twine upload dist/*
```