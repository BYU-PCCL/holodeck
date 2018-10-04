# Holodeck
Holodeck is a high-fidelity simulator for reinforcement learning built on top of Unreal Engine 4.
[Read the docs.](https://holodeck.readthedocs.io)

## Installation
### Requirements
Windows and Linux:
* Python 3.5 or higher
* Pip3
* At least 3gb storage

Linux:
* OpenGL version 3 or higher

### Pip Installation
To install the python bindings, simply run
`pip3 install holodeck`

### Installing Packages
Holodeck currently contains one package, the `DefaultWorlds` package.
Each package in turn contains a number of worlds.
Holodeck has an internal package manager for handling packages.
The most important commands for managing these are as follows:
```
import holodeck
print(holodeck.all_packages())                 # View all packages that are available to be downloaded.
print(holodeck.installed_packages())           # View which packages are currently installed.
holodeck.install('DefaultWorlds')              # Installs the DefaultWorlds package.
print(holodeck.package_info('DefaultWorlds'))  # View information on what worlds this package
                                               # contains, and what agents are in those worlds.
holodeck.remove('DefaultWorlds')               # Removes a package.
```
You only need to install packages once. You should make sure to remove them with
`holodeck.remove(package_name)` or `holodeck.remove_all_packages()` before removing
holodeck with pip.

## Basic Usage
Holodeck's interface is designed in the same vein as [OpenAI's Gym](https://gym.openai.com/).
The quickest way to get acquainted with Holodeck use is to view the example.py file.
Here is a basic walkthrough of an example that runs a Holodeck world:
```
import holodeck
import numpy as np
env = holodeck.make("UrbanCity")    # Load the environment. This environment contains a UAV in a city.
command = np.array([0, 0, 0, 100])  # The UAV takes 3 torques and a thrust as a command.
for i in range(30):
    state, reward, terminal, info = env.step(command)  # Pass the command to the environment with step.
                                                       # This returns the state, reward, terminal and info tuple.
```
The state is a dictionary of sensor enum to sensor value.
Reward is the reward received from the previous action, and terminal indicates whether the current
state is a terminal state.
Info contains additional environment specific information.

If you want to access the data of a specific sensor, it is as simple as import Sensors and
retrieving the correct value from the state dictionary:

```
from holodeck.sensors import Sensors
print(state[Sensors.LOCATION_SENSOR])
```

## Control Schemes
Holodeck supports different control schemes for different agents.
Currently the only agent with multiple control schemes is the UAV agent.
The control scheme can be switched as follows:
```
from holodeck.agents import ControlSchemes

env.set_control_scheme('uav0', ControlSchemes.UAV_ROLL_PITCH_YAW_RATE_ALT)
```
For more control schemes, check out the [docs](https://holodeck.readthedocs.io/en/latest/holodeck/agents.html)

## Multi Agent Environments
Holodeck supports multi-agent environments. The interface is a little different, but still very easy to use.
Instead of calling `step` which passes a command to the main agent and ticks the game, you should call `act`.
`act` supplies a command to a specific agent, but doesn't tick the game.
Once all agents have received their actions, you can call `tick` to tick the game.
After act, every time you call tick the same command will be supplied to the agent.
To change the command, just call act again.
```
env = holodeck.make('CyberPunkCity')
env.reset()

env.act('uav0', np.array([0, 0, 0, 100]))
env.act('nav0', np.array([0, 0, 0]))
for i in range(300):
    s = env.tick()
```
The state returned from tick is also somewhat different.
The state is now a dictionary from agent name to sensor dictionary.
You can access the reward, terminal and location for the UAV as follows:
```
s['uav0'][Sensors.REWARD]
s['uav0'][Sensors.TERMINAL]
s['uav0'][Sensors.LOCATION_SENSOR]
```

## Basic Controls
### HotKeys 
* `C` - toggles between a directly attached camera, which allows you to see more or less what the agent sees, and relative attach, 
which is the default camera attachment.
* `V` - toggles spectator mode, which allows you detach from the agent and explore the world without affecting the agent's vision.  
### Stats
You can view stats by entering console commands. When an environment is running, type `~` to open the console and enter a command. A common one to use is `stat FPS` to display the frames per second. More commands can be found in [UDK documentation](https://api.unrealengine.com/udk/Three/ConsoleCommands.html).


## Documentation
* [Agents](https://github.com/byu-pccl/holodeck/blob/master/docs/agents.md)
* [Sensors](https://github.com/byu-pccl/holodeck/blob/master/docs/sensors.md)
* [Environment configuration](https://github.com/byu-pccl/holodeck/blob/master/docs/worlds.md)
* [Docs](https://holodeck.readthedocs.io/en/latest/)


## Custom World Creation
To create custom worlds with variable start positions, number and type of agents, and different environments see the [Holodeck Engine](https://github.com/byu-pccl/holodeck-engine) and follow the [Packaging and Using Custom Worlds wiki](https://github.com/byu-pccl/holodeck-engine/wiki/Packaging-and-Using-Custom-Worlds) to use Holodeck for editing worlds with the Unreal editor.

## Using OpenGL3 in Linux
To use OpenGL3 in linux, change the argument in Holodeck.make:
```
from Holodeck import Holodeck
env = Holodeck.make("MazeWorld", Holodeck.GL_VERSION.OPENGL3)
```
