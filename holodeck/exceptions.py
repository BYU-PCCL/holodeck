"""Holodeck Exceptions"""


class HolodeckException(Exception):
    """HolodeckException.

    Args:
        message (str): The error string.
    """

    def __init__(self, message):
        super(HolodeckException, self).__init__(message)
