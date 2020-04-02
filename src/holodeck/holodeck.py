"""Module containing high level interface for loading environments."""
import uuid

from holodeck.environments import HolodeckEnvironment
from holodeck.packagemanager import get_scenario,\
    get_binary_path_for_scenario,\
    get_package_config_for_scenario,\
    get_binary_path_for_package
from holodeck.exceptions import HolodeckException


class GL_VERSION:
    """OpenGL Version enum.

    Attributes:
        OPENGL3 (:obj:`int`): The value for OpenGL3.
        OPENGL4 (:obj:`int`): The value for OpenGL4.
    """
    OPENGL4 = 4
    OPENGL3 = 3


def make(scenario_name="", scenario_cfg=None, gl_version=GL_VERSION.OPENGL4, window_res=None, verbose=False,
         show_viewport=True, ticks_per_sec=30, copy_state=True):
    """Creates a Holodeck environment

    Args:
        world_name (:obj:`str`):
            The name of the world to load as an environment. Must match the name of a world in an
            installed package.

        scenario_cfg (:obj:`dict`): Dictionary containing scenario configuration, instead of loading a scenario
            from the installed packages. Dictionary should match the format of the JSON configuration files

        gl_version (:obj:`int`, optional):
            The OpenGL version to use (Linux only). Defaults to GL_VERSION.OPENGL4.

        window_res ((:obj:`int`, :obj:`int`), optional):
            The (height, width) to load the engine window at. Overrides the (optional) resolution in the
            scenario config file

        verbose (:obj:`bool`, optional):
            Whether to run in verbose mode. Defaults to False.

        show_viewport (:obj:`bool`, optional):
            If the viewport window should be shown on-screen (Linux only). Defaults to True

        ticks_per_sec (:obj:`int`, optional):
            The number of frame ticks per unreal seconds. Defaults to 30.

        copy_state (:obj:`bool`, optional):
            If the state should be copied or passed as a reference when returned. Defaults to True

    Returns:
        :class:`~holodeck.environments.HolodeckEnvironment`: A holodeck environment instantiated
            with all the settings necessary for the specified world, and other supplied arguments.

    """

    param_dict = dict()
    binary_path = None

    if scenario_name != "":
        scenario = get_scenario(scenario_name)
        binary_path = get_binary_path_for_scenario(scenario_name)
    elif scenario_cfg is not None:
        scenario = scenario_cfg
        binary_path = get_binary_path_for_package(scenario["package_name"])
    else:
        raise HolodeckException("You must specify scenario_name or scenario_config")

    # Get pre-start steps
    package_config = get_package_config_for_scenario(scenario)
    world = [world for world in package_config["worlds"] if world["name"] == scenario["world"]][0]
    param_dict["pre_start_steps"] = world["pre_start_steps"]

    param_dict["scenario"] = scenario
    param_dict["binary_path"] = binary_path

    param_dict["start_world"] = True
    param_dict["uuid"] = str(uuid.uuid4())
    param_dict["gl_version"] = gl_version
    param_dict["verbose"] = verbose
    param_dict["show_viewport"] = show_viewport
    param_dict["copy_state"] = copy_state
    param_dict["ticks_per_sec"] = ticks_per_sec

    if window_res is not None:
        param_dict["window_size"] = window_res

    return HolodeckEnvironment(**param_dict)
