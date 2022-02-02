from PIL import Image
import os
import urllib.request
import matplotlib.pyplot as plt
from .request import Request
from .exceptions import DimensionTooBig
from .config import SYSTEM_CONFIG
from .config import logger

logger = logger(name=__name__)


class ImageSuper(Request):
    """Mixin parent class for images, contains attributes for filenames, methods for saving and deleting images.

    Attributes
        lat (float): Latitude coordinate of top left of image.
        lon (float): Longitude coordinate of top left of image.
        zoom (int): Zoom level (max 19).
        width (int): Width of final image.
        height (int): Height of final image.
        folder (str): folder type, either 'output_folder' or 'temp_folder'
        img_filename (str): Default filename for image, composed of lat, lon, zoom, width, height
        img_filepath (str): Default filepath for image
        img (PIL.Image): Image object

    Methods
        save(filepath=None, folder=None):
            Saves image either to a folder (saves original filename) or to an entire filepath
        delete()
            Delete image using img_filepath, if exists

    """
    def __init__(self, lat, lon, zoom, height, width, folder):
        """Constructs all the necessary attributes for the image superclass. Checks input width
        and height against config dimension threshold.

        Args:
            lat (float): Latitude coordinate of top left of image.
            lon (float): Longitude coordinate of top left of image.
            zoom (int): Zoom level (max 19).
            width (int): Width of final image.
            height (int): Height of final image.
            folder (str): folder type, either 'output_folder' or 'temp_folder'

        Raises
            DimensionTooBig: If either width or height above config dimension threshold.
        """
        super().__init__(lat, lon, zoom, height, width)

        self.img_filename = f'{self.lat}_{self.lon}_{self.zoom}_{self.width}_{self.height}.jpg'
        self.img_filepath = os.path.join(SYSTEM_CONFIG.get(folder), self.img_filename)
        self.img = None

        # Check against max image size. Size can be changed in config.py
        if self.height:
            if self.height > SYSTEM_CONFIG.get('dimension_threshold'):
                raise DimensionTooBig(self.height)
        if self.width:
            if self.width > SYSTEM_CONFIG.get('dimension_threshold'):
                raise DimensionTooBig(self.width)

    def save(self, filepath=None, folder=None):
        """Save image to specific filepath or folder

        Args:
            filepath (str, optional): Filepath to save image to
            folder (str, optional): Folder to save image to, keeps original filename

        Returns:
            None
        """

        # Replace entire filepath, if passed
        img_filepath = self.img_filepath
        if filepath:
            img_filepath = filepath

        # Replace folder path only if passed, keep filename
        if folder:
            old_folder, filename = os.path.split(img_filepath)
            img_filepath.replace(old_folder, folder)

        # Save
        os.makedirs(os.path.dirname(img_filepath), exist_ok=True)
        self.img.save(img_filepath)
        logger.info(f'File saved {img_filepath}')

    def delete(self):
        """Deletes image file from self.img_filepath

        Returns:

        """
        if os.path.exists(self.img_filepath):
            os.remove(self.img_filepath)
            logger.info(f'File removed {self.img_filepath}')
        else:
            logger.warning(f'File {self.img_filepath} doesnt exist')

    def __repr__(self):
        plt.imshow(self.img)
        return ''


class GMapImage(ImageSuper):
    """Representing the final image of width x height stitched together from multiple composite images.

    When you provide a latitude and longitude of an image you want captured, this

    Attributes
        lat (float): Latitude coordinate of top left of image.
        lon (float): Longitude coordinate of top left of image.
        zoom (int): Zoom level (max 19).
        width (int): Width of final image.
        height (int): Height of final image.
        folder (str): folder type, either 'output_folder' or 'temp_folder'
        img_filename (str): Default filename for image, composed of lat, lon, zoom, width, height
        img_filepath (str): Default filepath for image
        img (PIL.Image): Image object
        nearest_tile_latlon (tuple): lat-lon coordinates of top-left corner of nearest
            tile to input lat-lon coordinates

    Methods
        add_image(img, row, col):
            Adds image tile to composite image based on row and column references
        crop_dims(row, col):
            Calculate how much, if at all, to crop image to fit into composite image

    """
    def __init__(self, lat, lon, zoom, height, width, **kwargs):
        """

        Args:
            lat (float): Latitude coordinate of top left of image.
            lon (float): Longitude coordinate of top left of image.
            zoom (int): Zoom level (max 19).
            width (int): Width of final image.
            height (int): Height of final image.
            **kwargs:
        """
        super().__init__(lat, lon, zoom, height, width, 'output_folder')

        self.img = Image.new(mode='RGB', size=(width, height))

        logger.debug(f'GMapImage:{width}x{height}')

        if kwargs.get('filepath'):
            self.img_filepath = kwargs.get('filepath')

    def _add_image(self, img, row, col):
        """Pastes input image 'img' into final composite image 'self.img'

        Pastes input image based on number of rows (618 pixels) and columns (640 pixels) that
        goes into full image size. Crops boundary images to required size if necessary.

        For example a 1000 x 1000 image will required 4 (2 along, 2 high) 640 x 618 tile images.
        Each tile image is added to the final image, and the edge images are cropped to fit 1000 x
        1000

        Args:
            img (PIL.Image): Image to be pasted into full image
            row (int): Row coordinate of 618pxl rows that makes up the full image
            col (int): Column coordinate of 640pxl rows that makes up the full image

        Returns:

        """
        # calculate image x and y crop distances (if required)
        crop_x, crop_y = self._crop_dims(row, col)

        # apply crop
        img_cropped = img.crop((0, 0, crop_x, crop_y))

        # Paste image to top_left coordinates in self.img
        top_left_coords = (640 * col, 618 * row)
        logger.debug(f'Top-left coords: {top_left_coords}')
        self.img.paste(img_cropped, top_left_coords)

        # close both images, allows for files to be deleted
        img.close()
        img_cropped.close()

    def _crop_dims(self, row, col):
        """Calculates image crop coordinates for boundary images so that final image fits the
        required width x height dimensions

        For example a 1000 x 1000 image will required 4 (2 along, 2 high) 640 x 618 tile images.
        The first (0,0) tile won't need cropping, however the rest are 'edge' images and will need
        to be cropped to fit 1000 x 1000

        Args:
            row (int): Row coordinate of 618 pixel rows that makes up the full image
            col (int): Column coordinate of 640 pixel rows that makes up the full image

        Returns:
            crop_x (int), crop_y (int): boundary x and y coordinates of image to crop

        """

        # image coordinates for top left of image
        origin_x = col * 640
        origin_y = row * 618

        # image coordinates for bottom right of image
        boundary_x = origin_x + 640
        boundary_y = origin_y + 618

        logger.debug(f'patch:({origin_x},{origin_y},{boundary_x},{boundary_y})')

        # initialise default values
        crop_x = 640
        crop_y = 618

        # check against width/heights of desired output
        if boundary_x > self.width:
            crop_x = self.width - origin_x
        if boundary_y > self.height:
            crop_y = self.height - origin_y

        logger.debug(f'Crop: x:{crop_x}, y:{crop_y}')
        return crop_x, crop_y


class ImageLoader(ImageSuper):
    """Downloads image tile from Google Maps

    Attributes
        lat (float): Latitude coordinate of top left of image.
        lon (float): Longitude coordinate of top left of image.
        zoom (int): Zoom level (max 19).
        width (int): Width of final image.
        height (int): Height of final image.
        folder (str): folder type, either 'output_folder' or 'temp_folder'
        img_filename (str): Default filename for image, composed of lat, lon, zoom, width, height
        img_filepath (str): Default filepath for image
        img (PIL.Image): Image object
        map_type (str, optional): Defines what map type to use {'roadmap', 'satellite', 'terrain', 'hybrid'}.

    Methods
        download():
            Downloads image tile
        open()
            Loads image tile
    """
    def __init__(self, map_type='satellite', **kwargs):
        """

        Args:
            map_type (str, optional): Defines what map type to use {'roadmap', 'satellite', 'terrain', 'hybrid'}.
            lat (float): Latitude coordinate of top left of image.
            lon (float): Longitude coordinate of top left of image.
            zoom (int, optional): Zoom level (max 19).
            width (int, optional): Width of final image.
            height (int, optional): Height of final image.
            **kwargs:
        """
        super().__init__(folder='temp_folder', **kwargs)
        self.map_type = map_type

    def download(self):
        """Downloads image from Google Maps API

        Returns:

        """

        # build url
        url = SYSTEM_CONFIG.get('url_template')
        url = url.format(
            lat=self.lat,
            lon=self.lon,
            zoom=self.zoom,
            width=self.width,
            height=self.height,
            map_type=self.map_type,
            api_key=SYSTEM_CONFIG.get('gmap_key')
        )

        # Download image
        urllib.request.urlretrieve(url=url, filename=self.img_filepath)
        logger.debug(f'Image downloaded: {self.img_filepath}')

    def open(self):
        """Opens downloaded image tile.

        Checks if file exist in temp folder, if it doesn't then downloads image into temp folder
        before loading it

        Returns:
            PIL.Image: Image from self.img_filepath
        """
        if not os.path.exists(self.img_filepath):
            self.download()
        logger.debug(f'Image loaded:{self.img_filepath}')
        self.img = Image.open(self.img_filepath)
        return self.img
