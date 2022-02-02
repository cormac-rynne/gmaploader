import logging
import os
import sys


class Config:
    """Config class to hold package parameters

    Attributes
        params (dict): Parameters

    Methods
        get(param):
            Retrieve parameter
        set(param):
            Set parameter(s)

    """
    def __init__(self):

        self.params = {}

    def get(self, param):
        """Retrieves stored parameter

        Args:
            param (str): Parameter name

        Returns:

        """
        return self.params.get(param)

    def set(self, **kwargs):
        """Sets parameter

        Args:
            **kwargs:

        Returns:

        """
        for key, value in kwargs.items():
            self.params[key] = value


# create temp and output folders
TEMP_FOLDER = os.path.join(os.getcwd(), 'tmp')
OUTPUT_FOLDER = os.path.join(os.getcwd(), 'output')

# Initialise SYSTEM_CONFIG
SYSTEM_CONFIG = Config()
SYSTEM_CONFIG.set(
    url_template='https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom={zoom}&size={height}x{width}&maptype={map_type}&key={api_key}',
    temp_folder=TEMP_FOLDER,
    output_folder=OUTPUT_FOLDER,
    latlon_round=8,  # Rounding threshold for lat-lons
    dimension_threshold=3000,  # largest width or height allowed in a single image
    gmap_key=os.environ['GMAP_KEY'],  # GCP mapping services key
    logging_stdout_level=logging.DEBUG,  # Threshold for stdout
    logging_stdout=False,  # stdout on or off
    logging_files=False,  # Output logs to files or not
)


def logger(name, stdout_level=SYSTEM_CONFIG.get('logging_stdout_level'),
           file_output=SYSTEM_CONFIG.get('logging_files'),
           stdout=SYSTEM_CONFIG.get('logging_stdout')):
    """
    Creates logger object using default file and stdout settings. File outputs split into
    debug and info thresholds.

    Args:
        name (str): Logger name
        stdout_level (logging.object): Threshold for stdout
        file_output (bool): Output logs to file for records

    Returns:

    """
    handlers = []

    # Stdout settings
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_formatter = logging.Formatter('[%(asctime)s] %(message)s', '%Y-%m-%d %H:%M:%S')
    stdout_handler.setFormatter(stdout_formatter)

    # Stdout threshold
    stdout_handler.setLevel(stdout_level)

    # Collate settings, initialise
    if stdout:
        handlers.append(stdout_handler)

    # Output logs to files if applicable
    if file_output:
        # File settings
        file_formatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s',
                                           '%Y-%m-%d %H:%M:%S')

        # Generate log folder
        log_root_folder = os.getcwd()
        # log_root_folder = os.path.dirname(os.path.dirname(__file__))
        log_folder = os.path.join(log_root_folder, './logs')
        os.makedirs(log_folder, exist_ok=True)

        # debug.log file settings
        debug_file_handler = logging.FileHandler(filename='./logs/debug.log')
        debug_file_handler.setFormatter(file_formatter)
        debug_file_handler.setLevel(logging.DEBUG)

        # info.log file settings
        info_file_handler = logging.FileHandler(filename='./logs/info.log')
        info_file_handler.setFormatter(file_formatter)
        info_file_handler.setLevel(logging.INFO)

        handlers += [
            info_file_handler,
            debug_file_handler
        ]

    logging.basicConfig(handlers=handlers)
    logger_ = logging.getLogger(name)
    logger_.setLevel(logging.DEBUG)
    return logger_
