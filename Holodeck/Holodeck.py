import json
import uuid
import sys

from .Environments import *
from .Exceptions import HolodeckException


class GL_VERSION(object):
    OPENGL4 = 4
    OPENGL3 = 3


def _get_worlds_map():
    holodeck_worlds = dict()
    # Load in all existing worlds
    holodeck_path = os.environ["HOLODECKPATH"]
    if holodeck_path == "":
        raise HolodeckException("Couldn't find environment variable HOLODECKWORLDS.")
    worlds_path = os.path.join(holodeck_path, "worlds")
    for dir_name in os.listdir(worlds_path):
        full_path = os.path.join(worlds_path, dir_name)
        if os.path.isdir(full_path):
            for file_name in os.listdir(full_path):
                if file_name == "config.json":
                    with open(os.path.join(full_path, file_name), 'r') as f:
                        config = json.load(f)
                        if sys.version_info[0] < 3:
                            config = _convert_unicode(config)
                    for level in config["maps"]:
                        holodeck_worlds[level["name"]] = {
                            "agent_definitions": [AgentDefinition(**x) for x in level["agents"]],
                            "binary_path": os.path.join(full_path, config["path"]),
                            "task_key": level["name"],
                            "height": level["resy"],
                            "width": level["resx"]}
    return holodeck_worlds


# Resolves python 2 issue with json loading in unicode instead of string
def _convert_unicode(value):
    if isinstance(value, dict):
        return {_convert_unicode(key): _convert_unicode(value)
                for key, value in value.iteritems()}
    elif isinstance(value, list):
            return [_convert_unicode(item) for item in value]
    elif isinstance(value, unicode):
        return value.encode('utf-8')
    else:
        return value


def make(world, gl_version=GL_VERSION.OPENGL4):
    holodeck_worlds = _get_worlds_map()
    if world not in holodeck_worlds:
        raise HolodeckException("Invalid World Name")

    param_dict = copy(holodeck_worlds[world])
    param_dict["start_world"] = True
    param_dict["uuid"] = str(uuid.uuid4())
    param_dict["gl_version"] = gl_version
    return HolodeckEnvironment(**param_dict)
