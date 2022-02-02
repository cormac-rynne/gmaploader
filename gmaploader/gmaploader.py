from .coordinates import Coordinates
from .images import GMapImage, ImageLoader
import math
from .config import logger

logger = logger(name=__name__)


class GMapLoader(Coordinates, GMapImage):
    """
    A class to represent the final composite image. Coordinates methods from Coordinates, GMapImage and ImageLoader
    classes to generate the final image.

    Finds the slippy map tilename (https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames) of latitude
    and longitude provided then finds the boundary top left lat-lon of this tile. These boundary
    coordinates will be the top left of the image.

    Then downloads the required number of 640 x 640 image tiles from the Google Static Map API needed for
    the input width and height and stitches them together.


    Attributes
        lat (float): Latitude coordinate of top left of image.
        lon (float): Longitude coordinate of top left of image.
        zoom (int): Zoom level (max 19).
        width (int): Width of final image.
        height (int): Height of final image.
        map_type (str): Defines what map type to use
            {'roadmap', 'satellite', 'terrain', 'hybrid'}.
        save (bool): Boolean flag to save file image once loaded.
        delete_temp (bool): Boolean flag to delete tiles once each loaded into
            final composite image.
        img_filename (str): Default filename for image, composed of lat, lon,
            zoom, width, height.
        img_filepath (str): Default filepath for image.
        tile_x (int): Top left tile X coordinate of requested image.
        tile_y (int): Top left tile y coordinate of requested image.
        lat_pxl (float): Degrees in latitude per pixel in image.
        lon_pxl (float): Degree in longitude per pixel in image.
        nearest_tile_latlon (tuple): (Left, top, right, bottom) lat-lon coordinates of
            top-left corner tile (tile_x, tile_y) to input lat-lon coordinates.
        img (PIL.Image): Image object.

    Methods
        save(filepath=None, folder=None):
            Saves image either to a folder (saves original filename) or to an entire filepath
        delete()
            Delete image using img_filepath, if it has been saved or already exists

    Example usage 1
        import os
        os.environ['GMAP_KEY'] = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        from gmaploader import GMapLoader

        # Inputs
        lat = 51.563839178
        lon = -0.164794922

        # Initalise
        gml = GMapLoader(lat=lat, lon=lon)

        # Image
        img = gml.img

    Example usage 2
        import os
        os.environ['GMAP_KEY'] = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        from gmaploader import GMapLoader

        # Inputs
        lat = 51.563839178
        lon = -0.164794922
        width = 1200
        height = 300
        zoom = 16
        map_type = 'satellite'

        # Initalise
        gml = GMapLoader(
            lat=lat,
            lon=lon,
            width=width,
            height=height,
            zoom=zoom,
            map_type=map_type
        )

        # Image
        img = gml.img

    """

    def __init__(self, lat, lon, zoom=19, width=500, height=500, map_type='satellite', save=False,
                 delete_temp=True, **kwargs):
        """Calculates number of rows and columns of 640x618 tiles needed to generate entire image.
        For each 640x618 tile, calculates the latitude and longitude of the centre of the tile, loads
        image, and then stitches this to final image

        Args:
            lat (float): Latitude coordinate of top left of image.
            lon (float): Longitude coordinate of top left of image.
            zoom (int, optional): Zoom level (max 19).
            width (int, optional): Width of final image.
            height (int, optional): Height of final image.
            map_type (str, optional): Defines what map type to use
                {'roadmap', 'satellite', 'terrain', 'hybrid'}.
            save (bool, optional): Boolean flag to save file image once loaded.
            delete_temp (bool, optional): Boolean flag to delete tiles once each loaded into
                final composite image.

        """
        super().__init__(lat=lat, lon=lon, zoom=zoom, width=width, height=height, **kwargs)

        # Calculate number of rows and columns needed to build image from
        # 640 x 618 tiles
        rows = math.ceil(height / 618)
        columns = math.ceil(width / 640)

        # Display number of pictures needed
        total = rows*columns
        picture_message = f"{total} image{'s' if total > 1 else ''} required"
        print(picture_message)
        logger.info(picture_message)

        # Iterate over required rows and columns of 640 x 640 tiles for full image size
        for row in range(rows):
            for col in range(columns):

                # Generate lat-lon coordinates of centre of tile
                lat_c, lon_c = self.tile_center_latlon(row=row, col=col)

                # Initialise ImageLoader with center coordinates, zoom
                im_loader = ImageLoader(
                    lat=lat_c,
                    lon=lon_c,
                    width=640,
                    height=640,
                    zoom=zoom,
                    map_type=map_type
                )

                # Load 640x640 image from Google Maps
                img_640 = im_loader.open()

                # Paste image into GMapImage object
                self._add_image(img_640, row=row, col=col)

                # Remove from temp_folder
                if delete_temp:
                    im_loader.delete()

        logger.info(f'({self.lat}, {self.lon}), {self.width}x{self.height}, zoom:{self.zoom}')
        # Save GMapImage into output folder
        if save:
            self.save()
