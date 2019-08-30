import os
import unittest

from cidownloader.cadastral_inspire_downloader import format_codmun, parse_url, download, atom_urls


class TestCidDownloader(unittest.TestCase):
    def test_format_codmun(self):
        province_code = 36
        municipality_code = 62
        codmun = format_codmun(province_code, municipality_code)

        assert codmun == '36062'

    @unittest.skip
    def test_parse_url(self):
        parsed_url = parse_url()

        assert True is False

    def test_start_download(self):
        parcels = atom_urls['parcels']
        province_code = 36
        municipality_code = 62

        download(data_to_download=parcels, provincia=province_code, municipio=municipality_code)
        directory = os.path.dirname(os.path.abspath(__file__))
        geopackage = os.path.join(directory, 'buildings.gpkg')
        assert os.path.exists(geopackage) is True

    def tearDown(self) -> None:
        directory = os.path.dirname(os.path.abspath(__file__))
        geopackage = os.path.join(directory, 'buildings.gpkg')
        if os.path.exists(geopackage):
            os.remove(geopackage)


if __name__ == '__main__':
    unittest.main()
