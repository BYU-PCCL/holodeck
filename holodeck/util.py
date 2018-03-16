import math
import os
from holodeck.exceptions import HolodeckException


def get_holodeck_path():
    holodeck_path = os.environ["HOLODECKPATH"]
    if holodeck_path == "":
        raise HolodeckException("Couldn't find environment variable HOLODECKPATH.")
    return holodeck_path


def convert_unicode(value):
    """Resolves python 2 issue with json loading in unicode instead of string"""
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
    if os.name == "posix":
        return "Linux"
    elif os.name == "nt":
        return "Windows"
    else:
        raise NotImplementedError("holodeck is only supported for Linux and Windows")


def human_readable_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])
