"""Module containing high level interface for loading environments."""
import os
import uuid
from copy import copy

from holodeck.environments import HolodeckEnvironment, AgentDefinition
from holodeck.exceptions import HolodeckException
from holodeck.packagemanager import _iter_packages


class GL_VERSION(object):
    OPENGL4 = 4
    OPENGL3 = 3


def make(world_name, gl_version=GL_VERSION.OPENGL4, window_res=None, cam_res=None, verbose=False):
    """Creates a holodeck environment using the supplied world name.

    Positional Arguments:
    world_name -- The name of the world to load as an environment

    Keyword Arguments:
    gl_version -- The version of OpenGL to use for Linux (default GL_VERSION.OPENGL4)
    """
    holodeck_worlds = _get_worlds_map()
    if world_name not in holodeck_worlds:
        raise HolodeckException("Invalid World Name")

    param_dict = copy(holodeck_worlds[world_name])
    param_dict["start_world"] = True
    param_dict["uuid"] = str(uuid.uuid4())
    param_dict["gl_version"] = gl_version
    param_dict["verbose"] = verbose
    
    if window_res is not None:
        param_dict["window_width"] = window_res[0]
        param_dict["window_height"] = window_res[1]
    if cam_res is not None:
        param_dict["camera_width"] = cam_res[0]
        param_dict["camera_height"] = cam_res[1]

    return HolodeckEnvironment(**param_dict)


def _get_worlds_map():
    holodeck_worlds = dict()
    for config, path in _iter_packages():
        for level in config["maps"]:
            holodeck_worlds[level["name"]] = {
                "agent_definitions": [AgentDefinition(**x) for x in level["agents"]],
                "binary_path": os.path.join(path, config["path"]),
                "task_key": level["name"],
                "window_height": level["window_height"],
                "window_width": level["window_width"],
                "camera_height": level["camera_height"],
                "camera_width": level["camera_width"]}
    return holodeck_worlds
