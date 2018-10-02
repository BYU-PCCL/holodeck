# Holodeck
Holodeck is a high-fidelity simulator for reinforcement learning built on top of Unreal Engine 4.
## Requirements
Windows and Linux:
* Python 3.5 or higher
* Pip3
* At least 3gb storage

Linux:
* OpenGL version 3 or higher
## Installation
To install the python bindings, simply run
`pip3 install holodeck`

The packaged Unreal worlds must now be installed. To do so, open a python shell and run the following:
```
import holodeck
holodeck.install("DefaultWorlds")
```
The `holodeck.install("DefaultWorlds")` line downloads and installs the given package and allows you to use any of its worlds. 
*This only needs to be done once.* `holodeck.package_info("DefaultWorlds")` will display information about the worlds contained in the package. If you want to download a different package, use `holodeck.all_packages()` to see a list of those available for installation.

## Basic Usage
Holodeck's interface is designed in the same vein as [OpenAI's Gym](https://gym.openai.com/).
The quickest way to get acquainted with Holodeck use is to view the example.py file.
Here is a basic walkthrough of an example that runs a Holodeck world:
```
import holodeck
env = holodeck.make("UrbanCity")
command = np.array([0, 0, 0, 100])
for i in range(30):
    state, reward, terminal, info = env.step(command)
```

The `env = holodeck.make("UrbanCity")` line stores the world in the env variable. This particular world contains a UAV quadcopter, 
which can be given commands via a 4 entry array. This command can be given when ticking the world with the `env.step` function.
The step function returns a tuple of data representing the state, reward, terminal, and info. The state is a dictionary of sensor enum to sensor value. Reward is the reward received from the previous action, and terminal indicates whether the current state is a terminal state. Info contains additional environment specific information.

That's the basic example for using holodeck! Below is another example that shows how to access sensor data.

```
import holodeck
from holodeck.sensors import Sensors
env = holodeck.make("UrbanCity")
state, reward, terminal, info = env.reset()
for i in range(30):
    state, reward, terminal, info = env.step(np.array([0, 0, 0, 100]))
    print(state[Sensors.LOCATION_SENSOR])
```

## Basic Controls
### HotKeys 
* `C` - toggles between a directly attached camera, which allows you to see more or less what the agent sees, and relative attach, 
which is the default camera attachment.
* `V` - toggles spectator mode, which allows you detach from the agent and explore the world without affecting the agent's vision.  
### Stats
You can view stats by entering console commands. When an environment is running, type `~` to open the console and enter a command. A common one to use is `stat FPS` to display the frames per second. More commands can be found in [UDK documentation](https://api.unrealengine.com/udk/Three/ConsoleCommands.html).


## Documentation
* [Agents](https://github.com/BYU-PCCL/HolodeckPythonBinding/blob/master/docs/agents.md)
* [Sensors](https://github.com/BYU-PCCL/HolodeckPythonBinding/blob/master/docs/sensors.md)
* [Environment configuration](https://github.com/BYU-PCCL/HolodeckPythonBinding/blob/master/docs/worlds.md)
* [Docs](https://holodeck.readthedocs.io/en/latest/)


## Custom World Creation
To create custom worlds with variable start positions, number and type of agents, and different environments see the [Holodeck Engine](https://github.com/BYU-PCCL/Holodeck) and follow the [Using Custom Worlds wiki](https://github.com/BYU-PCCL/HolodeckPythonBinding/wiki/Using-Custom-Worlds) to use Holodeck for editing worlds with the Unreal editor.

## Using OpenGL3 in Linux
To use OpenGL3 in linux, change the argument in Holodeck.make:
```
from Holodeck import Holodeck
env = Holodeck.make("MazeWorld", Holodeck.GL_VERSION.OPENGL3)
```
