"""Helpful Utilities"""
import math
import os
import holodeck

from holodeck.command import DebugDrawCommand


try:
    unicode  # Python 2
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
        return {
            convert_unicode(key): convert_unicode(value) for key, value in value.items()
        }

    if isinstance(value, list):
        return [convert_unicode(item) for item in value]

    if isinstance(value, unicode):
        return value.encode("utf-8")

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


def draw_line(env, start, end, color=None, thickness=10.0):
    """Draws a debug line in the world

    Args:
        env (:class:`~holodeck.environments.HolodeckEnvironment`): Environment to draw in.
        start (:obj:`list` of :obj:`float`): The start ``[x, y, z]`` location of the line.
            (see :ref:`coordinate-system`)
        end (:obj:`list` of :obj:`float`): The end ``[x, y, z]`` location of the line
        color (:obj:`list``): ``[r, g, b]`` color value
        thickness (:obj:`float`): thickness of the line
    """
    color = [255, 0, 0] if color is None else color
    command_to_send = DebugDrawCommand(0, start, end, color, thickness)
    env._enqueue_command(command_to_send)


def draw_arrow(env, start, end, color=None, thickness=10.0):
    """Draws a debug arrow in the world

    Args:
        env (:class:`~holodeck.environments.HolodeckEnvironment`): Environment to draw in.
        start (:obj:`list` of :obj:`float`): The start ``[x, y, z]`` location of the line.
            (see :ref:`coordinate-system`)
        end (:obj:`list` of :obj:`float`): The end ``[x, y, z]`` location of the arrow
        color (:obj:`list`): ``[r, g, b]`` color value
        thickness (:obj:`float`): thickness of the arrow
    """
    color = [255, 0, 0] if color is None else color
    command_to_send = DebugDrawCommand(1, start, end, color, thickness)
    env._enqueue_command(command_to_send)


def draw_box(env, center, extent, color=None, thickness=10.0):
    """Draws a debug box in the world

    Args:
        env (:class:`~holodeck.environments.HolodeckEnvironment`): Environment to draw in.
        center (:obj:`list` of :obj:`float`): The start ``[x, y, z]`` location of the box.
            (see :ref:`coordinate-system`)
        extent (:obj:`list` of :obj:`float`): The ``[x, y, z]`` extent of the box
        color (:obj:`list`): ``[r, g, b]`` color value
        thickness (:obj:`float`): thickness of the lines
    """
    color = [255, 0, 0] if color is None else color
    command_to_send = DebugDrawCommand(2, center, extent, color, thickness)
    env._enqueue_command(command_to_send)


def draw_point(env, loc, color=None, thickness=10.0):
    """Draws a debug point in the world

    Args:
        env (:class:`~holodeck.environments.HolodeckEnvironment`): Environment to draw in.
        loc (:obj:`list` of :obj:`float`): The ``[x, y, z]`` start of the box.
            (see :ref:`coordinate-system`)
        color (:obj:`list` of :obj:`float`): ``[r, g, b]`` color value
        thickness (:obj:`float`): thickness of the point
    """
    color = [255, 0, 0] if color is None else color
    command_to_send = DebugDrawCommand(3, loc, [0, 0, 0], color, thickness)
    env._enqueue_command(command_to_send)


def _windows_check_process_alive(pid):
    import win32api
    import win32process
    import win32con

    if (
        win32process.GetExitCodeProcess(
            win32api.OpenProcess(
                win32con.PROCESS_QUERY_LIMITED_INFORMATION, win32con.FALSE, pid
            )
        )
        == win32con.STILL_ACTIVE
    ):
        return True

    return False


def _linux_check_process_alive(pid):
    return os.path.exists("/proc/{}".format(pid))


def check_process_alive(pid):
    if os.name == "posix":
        return _linux_check_process_alive(pid)
    if os.name == "nt":
        return _windows_check_process_alive(pid)


def log_paths():
    """Gets path for logs.

    Returns:
        :obj:`str`: The file path of where the logs are located
    """
    paths = []
    for package in holodeck.packagemanager.installed_packages():
        paths.append(
            os.path.join(
                get_holodeck_path(),
                "worlds",
                package,
                "{}NoEditor".format(get_os_key()),
                "Holodeck",
                "Saved",
                "Logs",
            )
        )

    return paths
