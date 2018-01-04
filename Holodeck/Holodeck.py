import uuid

from .Environments import *
from .Exceptions import HolodeckException
from .Agents import *

string_to_agent = {"DiscreteSphereAgent": DiscreteSphereAgent,
                   "UAVAgent": UAVAgent}
holodeck_worlds = dict()

# Load in all existing worlds
holodeck_path = os.environ["HOLODECKPATH"]
if holodeck_path == "":
    raise HolodeckException("Couldn't find environment variable HOLODECKWORLDS.")
worlds_path = os.path.join(holodeck_path, "worlds")
for dir_name in os.listdir(worlds_path):
    full_path = os.path.join(worlds_path, dir_name)
    if os.path.isdir(full_path):
        for file_name in os.listdir(full_path):
            if file_name.endswith(".txt"):
                with open(os.path.join(full_path, file_name), 'r') as f:
                    lines = f.read().splitlines()
                    for line in lines[2:]:
                        entries = line.split(' ')
                        holodeck_worlds[entries[0]] = {"binary_path": os.path.join(full_path, lines[1]),
                                                       "agent_type": string_to_agent[entries[1]],
                                                       "agent_name": entries[2],
                                                       "task_key": entries[0],
                                                       "height": int(entries[3]),
                                                       "width": int(entries[4]),
                                                       "sensors": list(
                                                           map(lambda x: Sensors.name_to_sensor(x), entries[5:]))}


def make(world):
    if world not in holodeck_worlds:
        raise HolodeckException("Invalid World Name")

    param_dict = copy(holodeck_worlds[world])
    param_dict["start_world"] = True
    param_dict["uuid"] = str(uuid.uuid4())
    return HolodeckEnvironment(**param_dict)
