import math
from .globalmaptiles import GlobalMercator
from .request import Request
from .config import SYSTEM_CONFIG
from .config import logger

logger = logger(name=__name__)


class Coordinates(Request):
    """Manages all coordinate calculations for tile coordinates and lat lon coordinates

    Attributes
        lat (float): Latitude coordinate of top left of image.
        lon (float): Longitude coordinate of top left of image.
        zoom (int): Zoom level (max 19).
        tile_x (int): Top left tile X coordinate of requested image
        tile_y (int): Top left tile y coordinate of requested image
        lat_pxl (float): Degrees in latitude per pixel in image
        lon_pxl (float): Degrees in longitude per pixel in image
        gm (object): GlobalMercator class object
        nearest_tile_latlon (tuple): (Left, top, right, bottom) lat-lon coordinates of
            top-left corner tile (tile_x, tile_y) to input lat-lon coordinates

    Methods
        tile_center_latlon(row, col)
            Generate lat-lon coordinates of center of tile
        latlon_pixel():
            Calculate degrees in lat and lon per pixel in image
        nearest_tile():
            Get lat-lon boundary coordinates of nearest tile
        get_tile_xy():
            Generate Google Map tile X-Y coordinates at coordinate lat-lon

    """
    def __init__(self, lat, lon, zoom, **kwargs):
        """

        Args:
            lat (float): Latitude coordinate of top left of image.
            lon (float): Longitude coordinate of top left of image.
            zoom (int): Zoom level (max 19).
            **kwargs:
        """
        super().__init__(lat, lon, zoom, **kwargs)
        logger.debug(f'Original coords: ({lat},{lon})')

        # Initialise GlobalMercator from globalmaptiles.py
        self.gm = GlobalMercator()

        # Get tile X-Y coodinates of input lat-lon coordinates
        self.tile_x, self.tile_y = self._get_tile_xy()

        # Get left, top, right, bottom lat-lon coordinates of tile calculated above
        self.nearest_tile_latlon = self._nearest_tile()

        # Calculate lat and lon degrees per pixel
        self.lat_pxl, self.lon_pxl = self._latlon_pixel()

    def tile_center_latlon(self, row, col):
        """Calculate lat and lon of center point of tile given row and column

        Args:
            row (int): Row coordinate of 618 pixel rows that makes up the full image
            col (int): Column coordinate of 640 pixel rows that makes up the full image

        Returns:

        """

        # Formula generalised using the following:
        # Center coord = top left coord +/- (distance to center) +/- (num rows/cols down from topleft)
        tile_lat_c = self.lat - ((640 / 2) * self.lat_pxl) - (row * 618 * self.lat_pxl)
        tile_lon_c = self.lon + ((640 / 2) * self.lon_pxl) + (col * 640 * self.lon_pxl)

        # round off lat-lon coordinates
        tile_lat_c, tile_lon_c = self._round(tile_lat_c, tile_lon_c)

        logger.debug(f'col-row:({col}, {row}): center lat-lon:({tile_lat_c},{tile_lon_c})')
        return tile_lat_c, tile_lon_c

    def _get_tile_xy(self):
        """Generates an X,Y Google Map tile coordinate based on the latitude, longitude and zoom level

        Returns:
            An X,Y Google Maps tile coordinate
        """

        # Add tiny amount to ensure in the right tile
        lat = self.lat - (1/(10**SYSTEM_CONFIG.get('latlon_round')))
        lon = self.lon + (1/(10**SYSTEM_CONFIG.get('latlon_round')))

        tile_size = 256

        # Use a left shift to get the power of 2
        # i.e. a zoom level of 2 will have 2^2 = 4 tiles
        num_tiles = 1 << self.zoom

        # Find the x_point given the longitude
        point_x = (tile_size / 2 + lon * tile_size / 360.0) * num_tiles // tile_size

        # Convert the latitude to radians and take the sine
        sin_y = math.sin(lat * (math.pi / 180.0))

        # Calculate the y coordinates
        point_y = ((tile_size / 2) + 0.5 * math.log((1 + sin_y) / (1 - sin_y)) * -(
                tile_size / (2 * math.pi))) * num_tiles // tile_size

        return int(point_x), int(point_y)

    def _latlon_pixel(self):
        """Calculates degrees of lat and lon per pixel

        Calculate degrees in lat and lon per pixel in image. This is not the same everywhere due to
        curvature of earth. Each individual image tile in Google Maps is 256 x 256, per pixel calculated
        using lat or lon differences/256
        """

        # Get left, top, right and bottom boundary lat-lons for tile
        lat_tl, lon_tl, lat_br, lon_br = self.nearest_tile_latlon

        # Calculate lat and lon/pixel of image
        self.lat_pxl = (lat_tl - lat_br)/256
        self.lon_pxl = (lon_br - lon_tl)/256
        logger.debug(f'Per pixel: lat:{self.lat_pxl}, lon:{self.lon_pxl}')

        return self.lat_pxl, self.lon_pxl

    def _nearest_tile(self):
        """Calculates left, top, right and bottom coordinates of nearest tile to input lat-lon
        coordinates. Top-left (tl), bottom-right (br)

        Returns:
            (left, top, right, bottom) lat-lon boundary coordinates of nearest tile

        """

        # # Get tile x-y coords of input lat-lon
        # self.tile_x, self.tile_y = self.get_tile_xy()

        # Get boundary lat-lon for tile
        lat_tl, lon_tl, lat_br, lon_br = self.gm.TileLatLonBounds(self.tile_x, self.tile_y, self.zoom)

        # Round outputs
        lat_tl_r, lon_tl_r = self._round(lat_tl, lon_tl)
        lat_br_r, lon_br_r = self._round(lat_br, lon_br)

        logger.debug(f'Nearest tile:({self.tile_x},{self.tile_y}), top-left:({lat_tl_r},{lon_tl_r}), bottom-right:({lat_br_r},{lon_br_r})')
        return lat_tl_r, lon_tl_r, lat_br_r, lon_br_r
