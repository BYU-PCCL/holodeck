"""Holodeck Exceptions"""


class HolodeckException(Exception):
    """Base class for a generic exception in Holodeck.

    Args:
        message (str): The error string.
    """

class HolodeckConfigurationException(HolodeckException):
    """The user provided an invalid configuration for Holodeck
    
    Args:
        message (str): The error string
    """

class TimeoutException(HolodeckException):
    """Exception raised when communicating with the engine timed out.

    """
