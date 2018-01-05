import os
import glob
import shutil
from pathlib import Path


def linux_installation():
    default_path = "/usr/local"

    print("Beginning Linux installation")
    path = input("Please choose installation path (Default is /usr/local): ")
    if path == "":
        path = default_path

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
        print("Installing at:", os.path.join(path, "Holodeck"))

        for file in glob.glob("Holodeck/*.py"):
            shutil.copyfile(file, os.path.join(path, "Holodeck", "Holodeck", file.split("/")[-1]))

        print("To continue installation, follow instructions on the github page")
        print("https://github.com/byu-pccl/HolodeckPythonBinding")
        print("Ensure to add the installed directory to your Python path")

    except PermissionError:
        print("Insufficient permissions, cannot install at specified path. Try with sudo")


def windows_installation():
    default_path = os.path.join(str(Path.home()), "AppData", "local")

    print("Beginning Windows installation")
    path = input("Please choose installation path (Default is /usr/local): ")
    if path == "":
        path = default_path

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
        print("Installing at:", os.path.join(path, "Holodeck"))

        for file in glob.glob("Holodeck\\*.py"):
            shutil.copyfile(file, os.path.join(path, "Holodeck", "Holodeck", file.split("\\")[-1]))

        print("To continue installation, follow instructions on the github page")
        print("https://github.com/byu-pccl/HolodeckPythonBinding")
        print("Ensure to add the installed directory to your path")

    except PermissionError:
        print("Insufficient permissions, cannot install at specified path.")


if os.name == "posix":
    linux_installation()
elif os.name == "nt":
    windows_installation()
else:
    raise NotImplementedError("Holodeck is only supported for Linux and Windows")
