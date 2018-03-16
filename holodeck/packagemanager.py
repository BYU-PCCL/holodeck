import json
import os
import sys
import urllib.request
import zipfile
from queue import Queue
from threading import Thread
import tempfile
import shutil

from holodeck import util
from holodeck.exceptions import HolodeckException

packages = {
    "DefaultWorlds": "DefaultWorlds_1.02.zip",
}


def all_packages():
    """Returns a list of all downloadable package names"""
    return [k for k in packages.keys()]


def installed_packages():
    return [x for x, _ in _iter_packages()]


def install(package_name):
    # Install constants
    binary_website = "http://pcc.byu.edu/holodeck/"

    if package_name not in packages:
        raise HolodeckException("Unknown package name " + package_name)
    package_url = packages[package_name]

    print("Installing", package_name)
    install_path = os.path.join(util.get_holodeck_path(), "worlds")
    binary_url = binary_website + util.get_os_key() + "_" + package_url
    _download_binary(binary_url, install_path)


def remove(package_name):
    if package_name not in packages:
        raise HolodeckException("Unknown package name " + package_name)
    for name, path in _iter_packages():
        if name == package_name:
            shutil.rmtree(path)


def _iter_packages():
    path = util.get_holodeck_path()
    worlds_path = os.path.join(path, "worlds")
    for dir_name in os.listdir(worlds_path):
        full_path = os.path.join(worlds_path, dir_name)
        if os.path.isdir(full_path):
            for file_name in os.listdir(full_path):
                if file_name == "config.json":
                    with open(os.path.join(full_path, file_name), 'r') as f:
                        config = json.load(f)
                        if sys.version_info[0] < 3:
                            config = util.convert_unicode(config)
                        yield config["name"], full_path


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
            sys.stdout.write("\r|" + blocks + spaces + "| %d%%" % int_percent)
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
