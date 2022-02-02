import unittest
import json
from gmaploader.images import GMapImage
from gmaploader.config import SYSTEM_CONFIG
from gmaploader.config import logger

logger = logger(
    name=__name__,
    stdout_level=SYSTEM_CONFIG.get('logging_stdout'),
    file_output=SYSTEM_CONFIG.get('logging_files')
)


test_dct = json.load(open('test_dct.json'))


class TestSum(unittest.TestCase):
    gmi = GMapImage(**test_dct)
    results = test_dct['results']

    #################
    # GMapImage tests
    #################

    # crop_dims
    def test_cropx_dims(self):
        crop_x, _ = self.gmi._crop_dims(row=self.results['row'], col=self.results['col'])
        self.assertEqual(crop_x, self.results['crop_x'])

    def test_cropy_dims(self):
        _, crop_y = self.gmi._crop_dims(row=1, col=1)
        self.assertEqual(crop_y, self.results['crop_y'])


if __name__ == '__main__':
    unittest.main()
