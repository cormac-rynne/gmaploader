import unittest
import json
from gmaploader.coordinates import Coordinates
from gmaploader.config import logger

logger = logger(name=__name__)

test_dct = json.load(open('test_dct.json'))

class TestSum(unittest.TestCase):
    coord = Coordinates(**test_dct)
    results = test_dct['results']

    ##################
    # Coordinate tests
    ##################

    # get_tile_xy
    def test_get_tile_x(self):
        logger.info('Testing coord.get_tile_xy(), x')
        tile_x, _ = self.coord._get_tile_xy()
        self.assertEqual(tile_x, self.results['tile_x'])

    def test_get_tile_y(self):
        logger.info('Testing coord.get_tile_xy(), y')
        _, tile_y = self.coord._get_tile_xy()
        self.assertEqual(tile_y, self.results['tile_y'])

    # nearest_tile
    def test_get_nearest_tile_lattl(self):
        logger.info('Testing coord.nearest_tile(), lat_tl')
        lat_tl, _, _, _ = self.coord._nearest_tile()
        self.assertEqual(lat_tl, self.results['lat_tl'])

    def test_get_nearest_tile_lontl(self):
        logger.info('Testing coord.nearest_tile(), lon_tl')
        _, lon_tl, _, _ = self.coord._nearest_tile()
        self.assertEqual(lon_tl, self.results['lon_tl'])

    def test_get_nearest_tile_latbr(self):
        logger.info('Testing coord.nearest_tile(), lat_br')
        _, _, lat_br, _ = self.coord._nearest_tile()
        self.assertEqual(lat_br, self.results['lat_br'])

    def test_get_nearest_tile_lonbr(self):
        logger.info('Testing coord.nearest_tile(), lon_br')
        _, _, _, lon_br = self.coord._nearest_tile()
        self.assertEqual(lon_br, self.results['lon_br'])

    # latlon_pixel
    def test_lat_per_pixel(self):
        logger.info('Testing coord.latlon_pixel(), lat_pxl')
        lat_pxl, _ = self.coord._latlon_pixel()
        self.assertEqual(lat_pxl, self.results['lat_pxl'])

    def test_lon_per_pixel(self):
        logger.info('Testing coord.latlon_pixel(), lon_pxl')
        _, lon_pxl = self.coord._latlon_pixel()
        self.assertEqual(lon_pxl, self.results['lon_pxl'])

    # tile_center_latlon
    def test_tile_center_lat(self):
        logger.info('Testing coord.tile_center_latlon(), tile_lat_c')
        tile_lat_c, _ = self.coord.tile_center_latlon(row=self.results['row'], col=self.results['col'])
        self.assertEqual(tile_lat_c, self.results['tile_lat_c'])

    def test_tile_center_lon(self):
        logger.info('Testing coord.tile_center_latlon(), tile_lon_c')
        _, tile_lon_c = self.coord.tile_center_latlon(row=self.results['row'], col=self.results['col'])
        self.assertEqual(tile_lon_c, self.results['tile_lon_c'])


if __name__ == '__main__':
    unittest.main()
