"""Module containing high level interface for loading environments."""
import os
import uuid
from copy import copy

from holodeck.environments import HolodeckEnvironment
from holodeck.exceptions import HolodeckException
from holodeck.packagemanager import _iter_packages, _iter_scenarios


class GL_VERSION(object):
    """OpenGL Version enum.

    Attributes:
        OPENGL3 (int): The value for OpenGL3.
        OPENGL4 (int): The value for OpenGL4.
    """
    OPENGL4 = 4
    OPENGL3 = 3


def make(scenario_name, gl_version=GL_VERSION.OPENGL4, window_res=None, verbose=False, show_viewport=True,
         ticks_per_sec=30, copy_state=True):
    """Creates a holodeck environment using the supplied world name.

    Args:
        scenario_name (str): The name of the world to load as an environment. Must match the name of a world in an
            installed package.
        gl_version (int, optional): The OpenGL version to use (Linux only). Defaults to GL_VERSION.OPENGL4.
        window_res ((int, int), optional): The resolution to load the game window at. Defaults to (512, 512).
        verbose (bool, optional): Whether to run in verbose mode. Defaults to False.
        show_viewport (bool, optional): If the viewport window should be shown on-screen (Linux only). Defaults to True
        ticks_per_sec (int, optional): The number of frame ticks per unreal seconds. Defaults to 30.
        copy_state (bool, optional): If the state should be copied or passed as a reference when returned. Defaults to True
    Returns:
        HolodeckEnvironment: A holodeck environment instantiated with all the settings necessary for the specified
            world, and other supplied arguments.
    """
    holodeck_scenarios = _get_scenarios_map()
    if scenario_name not in holodeck_scenarios:
        raise HolodeckException("Invalid Scenario Name")

    param_dict = copy(holodeck_scenarios[scenario_name])
    param_dict["start_world"] = True
    param_dict["uuid"] = str(uuid.uuid4())
    param_dict["gl_version"] = gl_version
    param_dict["verbose"] = verbose
    param_dict["show_viewport"] = show_viewport
    param_dict["copy_state"] = copy_state
    param_dict["ticks_per_sec"] = ticks_per_sec

    if window_res is not None:
        param_dict["window_width"] = window_res[0]
        param_dict["window_height"] = window_res[1]

    return HolodeckEnvironment(**param_dict)


def _get_scenarios_map():
    holodeck_worlds = dict()
    for pack_config, pack_path in _iter_packages():
        for scenario_config in _iter_scenarios(pack_config["name"]):
            scenario_key = pack_config["name"] + "-" + scenario_config["name"]

            holodeck_worlds[scenario_key] = {
                "binary_path": os.path.join(pack_path, pack_config["path"]),
                "scenario_key": scenario_key,
                "window_height": scenario_config["window_height"],
                "window_width": scenario_config["window_width"]
            }
    return holodeck_worlds
