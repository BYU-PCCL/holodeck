"""Package manager for worlds available to download and use for Holodeck"""
import json
import os
import shutil
import sys
import tempfile
import urllib.request
import zipfile
from queue import Queue
from threading import Thread

from holodeck import util
from holodeck.exceptions import HolodeckException

packages = {
    "DefaultWorlds": "DefaultWorlds_0.1.0.zip",
}


def all_packages():
    """Returns a list of all downloadable package names

    Returns:
        (list): List of all the downloadable packages
    """
    return list(packages.keys())


def installed_packages():
    """Returns a list of all installed packages

    Returns:
        (list): List of all the currently installed packages
    """
    return [x["name"] for x, _ in _iter_packages()]


def package_info(pkg_name):
    """Prints the information of a package.

    Args:
        pkg_name (str): The name of the desired package to get information
    """
    indent = "  "
    for config, _ in _iter_packages():
        if pkg_name == config["name"]:
            print("Package:", pkg_name)
            print(indent, "Platform:", config["platform"])
            print(indent, "Version:", config["version"])
            print(indent, "Path:", config["path"])
            print(indent, "Worlds:")
            for world in config["maps"]:
                world_info(world["name"], world_config=world, initial_indent="    ")


def world_info(world_name, world_config=None, initial_indent="", next_indent="  "):
    """Gets and prints the information of a world.

    Args:
        world_name (str): the name of the world to retrieve information for
        world_config (dict optional): A dictionary containing the world's configuration. Will find the config if None. Defaults to None.
        initial_indent (str optional): This indent will apply to each output line. Defaults to "".
        next_indent (str optional): This indent will be applied within each nested line. Defaults to "  ".
    """
    if world_config is None:
        for config, _ in _iter_packages():
            for world in config["maps"]:
                if world["name"] == world_name:
                    world_config = world

    if world_config is None:
        raise HolodeckException("Couldn't find world " + world_name)

    second_indent = initial_indent + next_indent
    agent_indent = second_indent + next_indent
    sensor_indent = agent_indent + next_indent

    print(initial_indent, world_config["name"])
    print(second_indent, "Resolution:", world_config["window_width"], "x", world_config["window_height"])
    print(second_indent, "Agents:")
    for agent in world_config["agents"]:
        print(agent_indent, "Name:", agent["agent_name"])
        print(agent_indent, "Type:", agent["agent_type"])
        print(agent_indent, "Sensors:")
        for sensor in agent["sensors"]:
            print(sensor_indent, sensor)


def install(package_name):
    """Installs a holodeck package.

    Args:
        package_name (str): The name of the package to install
    """
    holodeck_path = util.get_holodeck_path()
    binary_website = "https://s3.amazonaws.com/holodeckworlds/"

    if package_name not in packages:
        raise HolodeckException("Unknown package name " + package_name)
    package_url = packages[package_name]

    print("Installing " + package_name + " at " + holodeck_path)
    install_path = os.path.join(holodeck_path, "worlds")
    binary_url = binary_website + util.get_os_key() + "_" + package_url
    _download_binary(binary_url, install_path)
    if os.name == "posix":
        _make_binary_excecutable(package_name, install_path)


def remove(package_name):
    """Removes a holodeck package.

    Args:
        package_name (str): the name of the package to remove
    """
    if package_name not in packages:
        raise HolodeckException("Unknown package name " + package_name)
    for config, path in _iter_packages():
        if config["name"] == package_name:
            shutil.rmtree(path)


def remove_all_packages():
    """Removes all holodeck packages."""
    for _, path in _iter_packages():
        shutil.rmtree(path)


def _iter_packages():
    path = util.get_holodeck_path()
    worlds_path = os.path.join(path, "worlds")
    if not os.path.exists(worlds_path):
        os.makedirs(worlds_path)
    for dir_name in os.listdir(worlds_path):
        full_path = os.path.join(worlds_path, dir_name)
        if os.path.isdir(full_path):
            for file_name in os.listdir(full_path):
                if file_name == "config.json":
                    with open(os.path.join(full_path, file_name), 'r') as f:
                        config = json.load(f)
                        if sys.version_info[0] < 3:
                            config = util.convert_unicode(config)
                    yield config, full_path


def _download_binary(binary_location, worlds_path, block_size=1000000):
    def file_writer_worker(tmp_fd, length, q):
        max_width = 20
        percent_per_block = 100 // max_width
        amount_written = 0
        while amount_written < length:
            tmp_fd.write(q.get())
            amount_written += block_size
            percent_done = 100 * amount_written / length
            int_percent = int(percent_done)
            num_blocks = int_percent // percent_per_block
            blocks = chr(0x2589) * num_blocks
            spaces = " " * (max_width - num_blocks)
            try:
                sys.stdout.write("\r|" + blocks + spaces + "| %d%%" % int_percent)
            except UnicodeEncodeError:
                print("\r"+str(int_percent)+"%", end="")

            sys.stdout.flush()

    q = Queue()
    tmp_fd = tempfile.TemporaryFile(suffix=".zip")
    with urllib.request.urlopen(binary_location) as conn:
        file_size = int(conn.headers["Content-Length"])
        print("File size:", util.human_readable_size(file_size))
        amount_read = 0
        write_thread = Thread(target=file_writer_worker, args=(tmp_fd, file_size, q))
        write_thread.start()
        while amount_read < file_size:
            q.put(conn.read(block_size))
            amount_read += block_size
        write_thread.join()
        print()

    # Unzip the binary
    print("Unpacking worlds...")
    with zipfile.ZipFile(tmp_fd, 'r') as zip_file:
        zip_file.extractall(worlds_path)
    print("Finished.")


def _make_binary_excecutable(package_name, worlds_path):
    complete_name = "Linux" + package_name
    for path, _, _ in os.walk(os.path.join(worlds_path, complete_name)):
        os.chmod(path, 0o777)
    binary_path = os.path.join(worlds_path, complete_name + "/LinuxNoEditor/Holodeck/Binaries/Linux/Holodeck")
    os.chmod(binary_path, 0o755)
