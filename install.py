from os.path import expanduser
from pathlib import Path
from holodeck.packagemanager import *


def _linux_make_path():
    default_path = "/usr/local"

    print("Beginning Linux installation")
    path = input("Please choose installation path (Default is /usr/local): ")
    if path == "":
        path = default_path
    path = expanduser(path)
    if not os.path.isdir(path):
        print("Unable to find path: " + path)
        return

    try:
        base_path = os.path.join(path, "Holodeck")
        worlds_path = os.path.join(base_path, "worlds")
        holodeck_path = os.path.join(base_path, "Holodeck")
        if not os.path.exists(base_path):
            os.mkdir(base_path)
        if not os.path.exists(worlds_path):
            os.mkdir(worlds_path)
        if not os.path.exists(holodeck_path):
            os.mkdir(holodeck_path)
        return os.path.join(path, "Holodeck")

    except PermissionError:
        print("Insufficient permissions, cannot install at specified path. Try with sudo")


def _windows_make_path():
    default_path = os.path.join(str(Path.home()), "AppData", "Local")

    print("Beginning Windows installation")
    path = input("Please choose installation path (Default is C:\\User\\user_name\\AppData\\Local): ")
    if path == "":
        path = default_path
    path = expanduser(path)
    if not os.path.isdir(path):
        print("Unable to find path: " + path)
        return

    try:
        base_path = os.path.join(path, "Holodeck")
        worlds_path = os.path.join(base_path, "worlds")
        holodeck_path = os.path.join(base_path, "Holodeck")
        if not os.path.exists(base_path):
            os.mkdir(base_path)
        if not os.path.exists(worlds_path):
            os.mkdir(worlds_path)
        if not os.path.exists(holodeck_path):
            os.mkdir(holodeck_path)
        return os.path.join(path, "Holodeck")

    except PermissionError:
        print("Insufficient permissions, cannot install at specified path. Try running as administrator")


def _select_project():
    print("Available Unreal Projects:")
    package_names = all_packages()
    for name in package_names:
        print(" " + name)

    choice = input("Please choose an Unreal Project for installation(default is DefaultWorlds): ")

    if not choice in package_names:
        choice = "DefaultWorlds"

    return choice


def _install_world(package_name):
    # install_path = "."
    if os.name == "posix":
        install_path = _linux_make_path()
    elif os.name == "nt":
        install_path = _windows_make_path()
    else:
        print(os.name + " is not supported by Holodeck.")
        return

    try:
        install(package_name, install_path)
        print("World installation successful!")
        print("To finish installation, follow instructions on the github page")
        print("https://github.com/byu-pccl/HolodeckPythonBinding")
        print("Ensure to add the installed directory to your Python path")
    except HolodeckException:
        print("Installation failed. Your path probably didn't exist")


package_name = _select_project()
_install_world(package_name)
