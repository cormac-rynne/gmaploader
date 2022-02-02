class DimensionTooBig(Exception):
    def __init__(self, dimension):
        self.message = f"{dimension} too big, change picture dimension threshold in config.py"
        super().__init__(self.message)