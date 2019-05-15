# Holodeck

[![Holodeck Video](docs/images/sunrise_Moment.jpg)](https://www.youtube.com/watch?v=_huewiGqfrs)

[![Read the docs badge](https://readthedocs.org/projects/holodeck/badge/)](https://holodeck.readthedocs.io/en/develop/) ![Build Status](https://jenkins.holodeck.ml/buildStatus/icon?job=holodeck-engine%2Fdevelop)

Holodeck is a high-fidelity simulator for reinforcement learning built on top of Unreal Engine 4.
[Read the docs.](https://holodeck.readthedocs.io)

## Installation
`pip install holodeck`

(requires Python 3)

See [Installation](https://holodeck.readthedocs.io/en/latest/usage/installation.html) for complete instructions (including Docker).

## Features
 - 7+ rich worlds for training agents in, and many scenarios for those worlds
 - Easily extend and modify training scenarios
 - Train and control more than one agent at once
 - Simple, OpenAI Gym-like interface
 - High performance - simulation speeds of up to 2x real time are possible
 - Run headless or watch your agents learn

## Usage
Holodeck's interface is designed in the same vein as [OpenAI's Gym](https://gym.openai.com/).
The quickest way to get acquainted with Holodeck use is to view the example.py file.
Here is a basic walkthrough of an example that runs a Holodeck world:
```python
import holodeck
import numpy as np
env = holodeck.make("UrbanCity")    # Load the environment. This environment contains a UAV in a city.
env.reset()                         # You must call `.reset()` on a newly created environment before ticking/stepping it
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

```python
from holodeck.sensors import Sensors
print(state[Sensors.LOCATION_SENSOR])
```

## Control Schemes
Holodeck supports different control schemes for different agents.
Currently the only agent with multiple control schemes is the UAV agent.
The control scheme can be switched as follows:
```python
from holodeck.agents import ControlSchemes

env.set_control_scheme('uav0', ControlSchemes.UAV_ROLL_PITCH_YAW_RATE_ALT)
```
For more control schemes, check out the [docs](https://holodeck.readthedocs.io/en/latest/holodeck/agents.html)

## Multi Agent-Environments
Holodeck supports multi-agent environments. The interface is a little different, but still very easy to use.
Instead of calling `step` which passes a command to the main agent and ticks the game, you should call `act`.
`act` supplies a command to a specific agent, but doesn't tick the game.
Once all agents have received their actions, you can call `tick` to tick the game.
After act, every time you call tick the same command will be supplied to the agent.
To change the command, just call act again.
```python
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


## Documentation
* [Agents](https://github.com/byu-pccl/holodeck/blob/master/docs/agents.md)
* [Sensors](https://github.com/byu-pccl/holodeck/blob/master/docs/sensors.md)
* [Environment configuration](https://github.com/byu-pccl/holodeck/blob/master/docs/worlds.md)
* [Docs](https://holodeck.readthedocs.io/en/latest/)

## Using OpenGL3 in Linux
To use OpenGL3 in linux, change the argument in Holodeck.make:
```
from Holodeck import Holodeck
env = Holodeck.make("MazeWorld", Holodeck.GL_VERSION.OPENGL3)
```

## Running Holodeck on Headless Machines
Holodeck can run on headless machines with GPU accelerated rendering. This requires no extra configuration. Holodeck will automatically detect that the machine is headless and configure it's rendering process accordingly. 

## Citation:
```
@misc{HolodeckPCCL,
  Author = {Joshua Greaves and Max Robinson and Nick Walton and Mitchell Mortensen and Robert Pottorff and Connor Christopherson and Derek Hancock and Jayden Milne David Wingate},
  Title = {Holodeck: A High Fidelity Simulator},
  Year = {2018},
}
```
