"""Module containing high level interface for loading environments."""
import uuid

from holodeck.environments import HolodeckEnvironment
from holodeck.packagemanager import get_scenario, get_world_path, get_package_config_for_scenario


class GL_VERSION(object):
    """OpenGL Version enum.

    Attributes:
        OPENGL3 (:obj:`int`): The value for OpenGL3.
        OPENGL4 (:obj:`int`): The value for OpenGL4.
    """
    OPENGL4 = 4
    OPENGL3 = 3


def make(scenario_name, gl_version=GL_VERSION.OPENGL4, window_res=None, verbose=False, show_viewport=True,
         ticks_per_sec=30, copy_state=True):
    """Creates a Holodeck environment

    Args:
        world_name (:obj:`str`): 
            The name of the world to load as an environment. Must match the name of a world in an installed package.

        gl_version (:obj:`int`, optional):
            The OpenGL version to use (Linux only). Defaults to GL_VERSION.OPENGL4.

        window_res ((:obj:`int`, :obj:`int`), optional):
            The resolution to load the game window at. Defaults to (512, 512).

        verbose (:obj:`bool`, optional):
            Whether to run in verbose mode. Defaults to False.

        show_viewport (:obj:`bool`, optional):
            If the viewport window should be shown on-screen (Linux only). Defaults to True

        ticks_per_sec (:obj:`int`, optional):
            The number of frame ticks per unreal seconds. Defaults to 30.

        copy_state (:obj:`bool`, optional):
            If the state should be copied or passed as a reference when returned. Defaults to True

    Returns:
        :class:`~holodeck.environments.HolodeckEnvironment`: A holodeck environment instantiated with all the settings
            necessary for the specified world, and other supplied arguments.
    
    """
    scenario = get_scenario(scenario_name)
    binary_path = get_world_path(scenario_name)

    param_dict = dict()
    
    # Get pre-start steps
    package_config = get_package_config_for_scenario(scenario)
    world = [world for world in package_config["worlds"] if world["name"] == scenario["world"]][0]
    param_dict["pre_start_steps"] = world["pre_start_steps"]
    
    param_dict["binary_path"] = binary_path
    param_dict["scenario_key"] = scenario_name
    param_dict["window_height"] = scenario["window_height"]
    param_dict["window_width"] = scenario["window_width"]
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
