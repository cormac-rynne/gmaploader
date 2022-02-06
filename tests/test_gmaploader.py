import unittest
import json
import os
import shutil
from gmaploader.gmaploader import GMapLoader
from gmaploader.config import logger

logger = logger(name=__name__)

test_dct = json.load(open('test_dct.json'))


class TestSum(unittest.TestCase):
    results = test_dct['results']
    filepath = os.path.join(os.getcwd(), results['filepath'])

    # Remove if already exists
    if os.path.exists(filepath):
        os.remove(filepath)

    gml = GMapLoader(**test_dct, filepath=filepath)

    #####################
    # Image download test
    #####################

    def test_image_exists(self):
        logger.info('Testing gml')
        self.gml.save()
        self.assertTrue(os.path.exists(self.filepath))

        # Remove unnecessary files and folders after test
        self.gml.delete()
        if os.path.exists('output'):
            shutil.rmtree('output')


if __name__ == '__main__':
    unittest.main()
