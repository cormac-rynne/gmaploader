from .config import SYSTEM_CONFIG
from .config import logger

logger = logger(name=__name__)


class Request:
    """Mixin superclass for holding parameters, rounding lat and lon

    Attributes
        lat (float): Latitude coordinate of top left of image.
        lon (float): Longitude coordinate of top left of image.
        zoom (int, optional): Zoom level (max 19).
        width (int, optional): Width of final image.
        height (int, optional): Height of final image.
        filepath (str): Image filepath

    Methods
        round(lat, lon):
            Rounds lat-lon coordinates to round level set in config.py


    """
    def __init__(self, lat, lon, zoom=19, height=618, width=640, **kwargs):
        """Rounds lat and lon

        Args:
            lat (float): Latitude coordinate of top left of image.
            lon (float): Longitude coordinate of top left of image.
            zoom (int, optional): Zoom level (max 19).
            width (int, optional): Width of final image.
            height (int, optional): Height of final image.
            **kwargs:
        """
        self.lat, self.lon = self._round(lat, lon)
        self.zoom = zoom
        self.height = height
        self.width = width
        self.filepath = kwargs.get('filepath')

        # if self.height:
        #     if self.height > SYSTEM_CONFIG.get('dimension_threshold'):
        #         raise DimensionTooBig(self.height)
        # if self.width:
        #     if self.width > SYSTEM_CONFIG.get('dimension_threshold'):
        #         raise DimensionTooBig(self.width)

    @staticmethod
    def _round(lat, lon):
        """Round coordinates to rounding parameter set in config

        Args:
            lat (float): latitude
            lon (float): longitude

        Returns:
            Tuple of floats, latitude and longitude
        """
        return round(lat, SYSTEM_CONFIG.get('latlon_round')), round(lon, SYSTEM_CONFIG.get('latlon_round'))
