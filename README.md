Holodeck is a high fidelity simulator for reinforcement learning built in the Unreal Engine.
These bindings provide a simple interface for communicating with prebuilt environments.
Currently only support Python3 in Windows and Linux.


# Prerequisites
* Python3
* The following packages: `pip3 install numpy gym`
* Platform specific dependencies below
* About 3gb hard drive space (around 5gb needed during installation)

### Linux
* Posix ipc: `pip3 install posix_ipc`
* OpenGL3 or 4

### Windows
* pywin32: `pip3 install pywin32`

# Installation
* Clone the repository `git clone https://github.com/byu-pccl/HolodeckPythonBinding`
* Run the Python install script `python3 install.py`
* Add the HOLODECKPATH environment variable (see below)
* Add the HOLODECKPATH to your PYTHONPATH (see below)
* `source .bashrc` or open a new terminal
* Verify installation by opening python3 in terminal and running:
```
from Holodeck import Holodeck
env = Holodeck.make("MazeWorld")
```
If the world loads up then installation was successful

## Adding Environment Variables
### Linux
Add these lines to the end of your bashrc file:
```
export HOLODECKPATH="/usr/local/Holodeck"
export PYTHONPATH="${HOLODECKPATH}:${PYTHONPATH}"
```
If you didn't install at the default location, make sure to change it to the correct path.

### Windows
Press the windows button and start typing "environment variables". Click "Edit the system environment variables".
Press the Environment Variables button.
Under the System variables section, click "New".
VariableName = HOLODECKPATH
VariableValue = your path to holodeck (default: C:\Users\user_name\AppData\Local\Holodeck)

Then, click on the PYTHONPATH variable, and add the Holodeck root directory to it.
(If the PYTHONPATH variable isn't there, you should create it).

# Usage
The quickest way to get acquainted with basic Holodeck use is to view the example.py file.

The Holodeck instance is designed in the same vein as OpenAI's Gym.
All you need is to import Holodeck `from Holodeck import Holodeck` and then create an environment with the make command:
`env = Holodeck.make('MazeWorld')`.

The current world list is `MazeWorld`, `UrbanCity`, `EuropeanForest`, and `RedwoodForest`.

Each environment contains an agent, and each agent has a specific number of sensors.
The default worlds currently contain 2 supported agents:
* UAV - A quad-copter which takes as input target values for roll, pitch, yaw rate, and altitude.
* DiscreteSphere - A basic robot that moves on a plane, with four moves: forward, backward, left, and right.

UAV WORLDS
* UrbanCity
* EuropeanForest
* RedwoodForest

SPHERE ROBOT WORLDS
* MazeWorld

To interact with the environment, you simply call `env.step(cmd)` where cmd is a command for the specific agent.
Each agent has a different action space, which are detailed below.
The step function returns a tuple of `(state, reward, terminal, info)`.
The state is a dictionary of sensor enum to sensor value.
Reward is the reward received from the previous action, and terminal indicates whether the current state is a terminal state.
Info contains additional environment specific information.
The sensors for each agent are also indicated below.

## UAV
The UAV's action space is as follows:
```
[roll_target, pitch_target, yaw_rate_target, altitude_target]
```
It contains the following sensors:
* PrimaryPlayerCamera
* OrientationSensor
* LocationSensor
* VelocitySensor
* IMUSensor


## DiscreteSphereRobot
The DiscreteSphereRobot takes in an index of one of four actions:
* 0: Move Forward
* 1: Move Backward
* 2: Turn Right
* 3: Turn Left

It contains the following sensors:
* PrimaryPlayerCamera
* OrientationSensor
* LocationSensor

## AndroidAgent
The AndroidAgent action space is a 94 dimensional vector containing values for the torques to be applied at each of the Android's joints. Details can be found [here](https://github.com/BYU-PCCL/Holodeck/blob/develop/Source/Holodeck/Agents/Private/Android.cpp)

## Custom World Creation
To create custom worlds with variable start positions, number and type of agents, and different environments see [Using Custom Worlds](https://github.com/BYU-PCCL/HolodeckPythonBinding/wiki/Using-Custom-Worlds) on the wiki for details on compiling Holodeck and editing worlds with the Unreal editor.

## Using OpenGL3 in Linux
To use OpenGL3 in linux, change the argument in Holodeck.make:
```
from Holodeck import Holodeck
env = Holodeck.make("MazeWorld", Holodeck.GL_VERSION.OPENGL3)
```
