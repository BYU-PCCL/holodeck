"""Holodeck Exceptions"""


class HolodeckException(Exception):
    """HolodeckException.

    Args:
        message (str): The error string.
    """

class TimeoutException(HolodeckException):
    """Exception raised when communicating with the engine timed out.

    """