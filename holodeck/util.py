"""Helpful Utilities"""
import math
import os


def get_holodeck_path():
    """Gets the path of the holodeck environment

    Returns:
        (str): path to the current holodeck environment
    """
    if "HOLODECKPATH" in os.environ and os.environ["HOLODECKPATH"] != "":
        return os.environ["HOLODECKPATH"]
    if os.name == "posix":
        return os.path.expanduser("~/.local/share/holodeck")
    elif os.name == "nt":
        return os.path.expanduser("~\\AppData\\Local\\holodeck")
    else:
        raise NotImplementedError("holodeck is only supported for Linux and Windows")


def convert_unicode(value):
    """Resolves python 2 issue with json loading in unicode instead of string

    Args:
        value (str): Unicode value to be converted

    Returns:
        (str): converted string

    """
    if isinstance(value, dict):
        return {convert_unicode(key): convert_unicode(value)
                for key, value in value.iteritems()}
    elif isinstance(value, list):
        return [convert_unicode(item) for item in value]
    elif isinstance(value, unicode):
        return value.encode('utf-8')
    else:
        return value


def get_os_key():
    """Gets the key for the OS.

    Returns:
        str: "Linux" or "Windows". Throws NotImplementedError for other systems.
    """
    if os.name == "posix":
        return "Linux"
    elif os.name == "nt":
        return "Windows"
    else:
        raise NotImplementedError("holodeck is only supported for Linux and Windows")


def human_readable_size(size_bytes):
    """Gets a number of bytes as a human readable string.

    Args:
        size_bytes (int): The number of bytes to get as human readable.

    Returns:
        str: The number of bytes in a human readable form.
    """
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])
