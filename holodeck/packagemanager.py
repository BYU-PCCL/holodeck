"""Package manager for worlds available to download and use for Holodeck"""
import json
import os
import shutil
import sys
import tempfile
import urllib.request
import urllib.error
import fnmatch
import zipfile
import pprint
from queue import Queue
from threading import Thread

from holodeck import util
from holodeck.exceptions import HolodeckException

backend_url = "https://s3.amazonaws.com/holodeckworlds/"


def _get_from_backend(rel_url):
    """
    Gets the resource given at rel_url, assumes it is a utf-8 text file
    
    Args:
        rel_url (:obj:`str`): url relative to backend_url to fetch

    Returns:
        :obj:`str`: The resource at rel_url as a string
    """
    r = urllib.request.urlopen(backend_url + rel_url)
    data = r.read()
    return data.decode('utf-8')


def available_packages():
    """Returns a list of package names available for the current version of Holodeck

    Returns (:obj:`list` of :obj:`str`):
        List of package names
    """
    # Get the index json file from the backend
    url = "packages/{ver}/available".format(ver=util.get_holodeck_version())
    try:
        index = _get_from_backend(url)
        index = json.loads(index)
    except urllib.error.URLError as err:
        print("Unable to communicate with backend ({}), {}".format(url, err.reason), file=sys.stderr)
        raise

    return index["packages"]


def installed_packages():
    """Returns a list of all installed packages

    Returns:
        :obj:`list` of :obj:`str`: List of all the currently installed packages
    """
    _check_for_old_versions()
    return [x["name"] for x, _ in _iter_packages()]


def package_info(pkg_name):
    """Prints the information of a package.

    Args:
        pkg_name (:obj:`str`): The name of the desired package to get information
    """
    indent = "  "
    for config, _ in _iter_packages():
        if pkg_name == config["name"]:
            print("Package:", pkg_name)
            print(indent, "Platform:", config["platform"])
            print(indent, "Version:", config["version"])
            print(indent, "Path:", config["path"])
            print(indent, "Worlds:")
            for world in config["worlds"]:
                world_info(world["name"], world_config=world, base_indent=4)


def _print_agent_info(agents, base_indent=0):
    print(base_indent*' ', "Agents:")
    base_indent += 2
    for agent in agents:
        print(base_indent*' ', "Name:", agent["agent_name"])
        print(base_indent*' ', "Type:", agent["agent_type"])
        print(base_indent*' ', "Sensors:")
        for sensor in agent["sensors"]:
            print((base_indent + 2)*' ', sensor)


def world_info(world_name, world_config=None, base_indent=0):
    """Gets and prints the information of a world.

    Args:
        world_name (:obj:`str`): the name of the world to retrieve information for
        world_config (:obj:`dict`, optional): A dictionary containing the world's configuration. Will find the config if None. Defaults to None.
        base_indent (:obj:`int`, optional): How much to indent output
    """
    if world_config is None:
        for config, _ in _iter_packages():
            for world in config["worlds"]:
                if world["name"] == world_name:
                    world_config = world

    if world_config is None:
        raise HolodeckException("Couldn't find world " + world_name)

    print(base_indent*' ', world_config["name"])
    base_indent += 4

    if "agents" in world_config:
        _print_agent_info(world_config["agents"], base_indent)

    print(base_indent*' ', "Scenarios:")
    for scenario, path in _iter_scenarios(world_name):
        scenario_info(scenario=scenario, base_indent=base_indent + 2)


def _find_file_in_worlds_dir(filename):
    """
    Recursively tries to find filename in the worlds directory of holodeck

    Args:
        filename (:obj:`str`): Pattern to try and match (fnmatch)

    Returns:
        :obj:`str`: The path or an empty string if the file was not found

    """
    for root, dirnames, filenames in os.walk(util.get_holodeck_path(), "worlds"):
        for match in fnmatch.filter(filenames, filename):
            return os.path.join(root, match)
    return ""


def scenario_info(scenario_name="", scenario=None, base_indent=0):
    """Gets and prints information for a particular scenario file
    Must match this format: scenario_name.json

    Args:
        scenario_name (:obj:`str`): The name of the scenario
        scenario (:obj:`dict`, optional): Loaded dictionary config (overrides world_name and scenario_name)
        base_indent (:obj:`int`, optional): How much to indent output by
    """
    scenario_file = ""
    if scenario is None:
        # Find this file in the worlds/ directory
        filename = '{}.json'.format(scenario_name)
        scenario_file = _find_file_in_worlds_dir(filename)

        if scenario_file == "":
            raise FileNotFoundError("The file {} could not be found".format(filename))

        scenario = load_scenario_file(scenario_file)

    print(base_indent*' ', "{}-{}:".format(scenario["world"], scenario["name"]))
    base_indent += 2
    if "agents" in scenario:
        _print_agent_info(scenario["agents"], base_indent)


def install(package_name):
    """Installs a holodeck package.

    Args:
        package_name (:obj:`str`): The name of the package to install
    """
    _check_for_old_versions()
    holodeck_path = util.get_holodeck_path()

    packages = available_packages()
    if package_name not in packages:
        print("Package not found. Available package are:", file=sys.stderr)
        pprint.pprint(packages, width=10, indent=4, stream=sys.stderr)
        return

    # example: %backend%/packages/0.1.0/DefaultWorlds/Linux.zip
    binary_url = "{backend_url}packages/{holodeck_version}/{package_name}/{platform}.zip".format(
        backend_url=backend_url, 
        holodeck_version=util.get_holodeck_version(),
        package_name=package_name, 
        platform=util.get_os_key())

    install_path = os.path.join(holodeck_path, "worlds", package_name)

    print("Installing {} from {} to {}".format(package_name, binary_url, install_path))

    _download_binary(binary_url, install_path)

def _check_for_old_versions():
    """Checks for old versions of the binary and tells the user they can remove them.
    If there is an ignore_old_packages file, it will stay silent.
    """
    # holodeckpath turns off the binary folder versioning
    if "HOLODECKPATH" in os.environ:
        return

    path = util._get_holodeck_folder()

    if not os.path.exists(path):
        return

    not_matching = []
    
    for f in os.listdir(path):
        f_path = os.path.join(path, f)
        if f == "ignore_old_packages":
            return
        elif f == util.get_holodeck_version():
            continue
        elif not os.path.isfile(f_path):
            not_matching.append(f)

    if len(not_matching):
        print("**********************************************")
        print("* You have old versions of Holodeck packages *")
        print("**********************************************")
        print("Use packagemanager.prune() to delete old packages")
        print("Versions:", not_matching)
        print("Place an `ignore_old_packages` file in {} to surpress this message".format(path))
        print()

def prune():
    """Prunes old versions of holodeck, other than the running version.

    **DO NOT USE WITH HOLODECKPATH** 
    
    Don't use this function if you have overidden the path.
    """
    if "HOLODECKPATH" in os.environ:
        print("This function is not available when using HOLODECKPATH", stream=sys.stderr)
        return
    
    holodeck_folder = util._get_holodeck_folder()
    
    # Delete everything in holodeck_folder that isn't the current holodeck version
    for file in os.listdir(holodeck_folder):
        file_path = os.path.join(holodeck_folder, file)
        if os.path.isfile(file_path):
            continue
        if file == util.get_holodeck_version():
            continue
        # Delete it!
        print("Deleting {}".format(file_path))
        shutil.rmtree(file_path)

    print("Done")

def remove(package_name):
    """Removes a holodeck package.

    Args:
        package_name (:obj:`str`): the name of the package to remove
    """
    for config, path in _iter_packages():
        if config["name"] == package_name:
            shutil.rmtree(path)


def remove_all_packages():
    """Removes all holodeck packages.
    
    """
    for _, path in _iter_packages():
        shutil.rmtree(path)


def load_scenario_file(scenario_path):
    """
    Loads the scenario config file and returns a dictionary containing the configuration

    Args:
        scenario_path (:obj:`str`): Path to the configuration file

    Returns:
        :obj:`dict`: A dictionary containing the configuration file

    """
    with open(scenario_path, 'r') as f:
        return json.load(f)


def get_scenario(scenario_name):
    """Gets the scenario configuration associated with the given name

    Args:
        scenario_name (:obj:`str`): name of the configuration to load - eg "UrbanCity-Follow"
            Must be an exact match. Name must be unique among all installed packages

    Returns:
        :obj:`dict`: A dictionary containing the configuration file

    """
    config_path = _find_file_in_worlds_dir(scenario_name + ".json")

    if config_path == "":
        raise FileNotFoundError(
            "The file `{file}.json` could not be found in {path}. Make sure the package that contains {file} " \
            "is installed.".format(file=scenario_name, path=util.get_holodeck_path()))

    return load_scenario_file(config_path)


def get_world_path(scenario_name):
    """Gets the scenario configuration associated with the given name

    Args:
        scenario_name (str): name of the configuration to load - eg "UrbanCity-Follow"
                     Must be an exact match. Name must be unique among all installed packages

    Returns (dict): A dictionary containing the configuration file

    """
    scenario_path = _find_file_in_worlds_dir(scenario_name + ".json")
    root = os.path.dirname(scenario_path)
    config_path = os.path.join(root, "config.json")
    with open(config_path, 'r') as f:
        config = json.load(f)
        return os.path.join(root, config["path"])


def get_package_config_for_scenario(scenario):
    """For the given scenario, returns the package config associated with it (config.json)

    Args:
        scenario (:obj:`dict`): scenario dict to look up the package for

    Returns:
        :obj:`dict`: package configuration dictionary

    """

    world_name = scenario["world"]

    for config, path in _iter_packages():
        for world in config["worlds"]:
            if world["name"] == world_name:
                return config

    raise HolodeckException("Could not find a package that contains world {}".format(world_name))


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


def _iter_scenarios(world_name):
    """Iterates over the scenarios associated with world_name.

    Note that world_name needs to be unique among all packages

    Args:
        world_name (:obj:`str`): name of the world

    Returns: config_dict, path_to_config
    """
    package_path = os.path.join(util.get_holodeck_path(), "worlds", world_name)

    # Find a scenario for this world
    a_scenario = _find_file_in_worlds_dir("{}-*".format(world_name))

    if a_scenario is None:
        return

    # Find the parent path of that file
    world_path = os.path.abspath(os.path.join(a_scenario, os.pardir))

    if not os.path.exists(world_path):
        os.makedirs(world_path)
    for file_name in os.listdir(world_path):
        if file_name == "config.json":
            continue
        if not file_name.endswith(".json"):
            continue
        if not fnmatch.fnmatch(file_name, "{}-*.json".format(world_name)):
            continue


        full_path = os.path.join(world_path, file_name)
        with open(full_path, 'r') as f:
            config = json.load(f)
            yield config, full_path


def _download_binary(binary_location, install_location, block_size=1000000):
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
            blocks = chr(0x2588) * num_blocks
            spaces = " " * (max_width - num_blocks)
            try:
                sys.stdout.write("\r|" + blocks + spaces + "| %d%%" % int_percent)
            except UnicodeEncodeError:
                print("\r" + str(int_percent) + "%", end="")

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
    # Note the contents of the ZIP file get extracted straight into the install directory, so the zip's structure should
    # look like file.zip/config.json not file.zip/file/config.json
    print("Unpacking worlds...")
    with zipfile.ZipFile(tmp_fd, 'r') as zip_file:
        zip_file.extractall(install_location)
        
    if os.name == "posix":
        print("Fixing Permissions")
        _make_excecutable(install_location)

    print("Finished.")

def _make_excecutable(install_path):
    for path, _, files in os.walk(install_path):
        for f in files:
            os.chmod(os.path.join(path, f), 0o777)
