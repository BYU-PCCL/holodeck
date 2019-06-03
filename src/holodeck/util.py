"""Helpful Utilities"""
import math
import os
import holodeck
from multiprocessing import Process, Event

try:
    unicode        # Python 2
except NameError:
    unicode = str  # Python 3


def get_holodeck_version():
    """Gets the current version of holodeck

    Returns:
        (:obj:`str`): the current version
    """
    return holodeck.__version__

def _get_holodeck_folder():
    if "HOLODECKPATH" in os.environ and os.environ["HOLODECKPATH"] != "":
        return os.environ["HOLODECKPATH"]

    if os.name == "posix":
        return os.path.expanduser("~/.local/share/holodeck")

    if os.name == "nt":
        return os.path.expanduser("~\\AppData\\Local\\holodeck")

    raise NotImplementedError("holodeck is only supported for Linux and Windows")

def get_holodeck_path():
    """Gets the path of the holodeck environment

    Returns:
        (:obj:`str`): path to the current holodeck environment
    """

    return os.path.join(_get_holodeck_folder(), get_holodeck_version())


def convert_unicode(value):
    """Resolves python 2 issue with json loading in unicode instead of string

    Args:
        value (:obj:`str`): Unicode value to be converted

    Returns:
        (:obj:`str`): Converted string

    """
    if isinstance(value, dict):
        return {convert_unicode(key): convert_unicode(value)
                for key, value in value.iteritems()}

    if isinstance(value, list):
        return [convert_unicode(item) for item in value]

    if isinstance(value, unicode):
        return value.encode('utf-8')

    return value


def get_os_key():
    """Gets the key for the OS.

    Returns:
        :obj:`str`: ``Linux`` or ``Windows``. Throws ``NotImplementedError`` for other systems.
    """
    if os.name == "posix":
        return "Linux"
    if os.name == "nt":
        return "Windows"

    raise NotImplementedError("Holodeck is only supported for Linux and Windows")


def human_readable_size(size_bytes):
    """Gets a number of bytes as a human readable string.

    Args:
        size_bytes (:obj:`int`): The number of bytes to get as human readable.

    Returns:
        :obj:`str`: The number of bytes in a human readable form.
    """
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    base = int(math.floor(math.log(size_bytes, 1024)))
    power = math.pow(1024, base)
    size = round(size_bytes / power, 2)
    return "%s %s" % (size, size_name[base])
