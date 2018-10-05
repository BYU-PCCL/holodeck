# HolodeckTasks

A HolodeckTask calculates the reward and terminal data for any given agent. This is accessed by `env.step(command)`, which returns a 
tuple containing the reward and terminal. Tasks calculate this data differently depending on the it's type and given parameters. 
Each task has a Main Agent parameter that indicates the agent that recieves the reward. Below are listed the additional parameters of the 
different tasks as well as a description of their behavior.


## Task Types
### Proximity Task
Parameters: 
* MainAgent
* ToFollow
* OnlyWithinSight
The proximity task gives a positive reward as the main agent approaches the given ToFollow actor. This can be a basic UE4 actor
(such as a cube or wall) or a Holodeck agent. If the OnlyWithinSight parameter is set to true, then the reward will only be given when 
the ToFollow actor is visible from the main agent.

### Distance Task
Parameters:
* MainAgent
The distance task gives a positive reward as the agent moves farther away from its starting position.

### Maze Task
Parameters: 
* MainAgent
* Target
The maze task gives a positive reward as the agent approaches the Target actor.

A task's parameters are not currently controllable from the python bindings, but the details of each task in the DefaultWorlds package 
can be found [here](https://github.com/BYU-PCCL/holodeck/edit/master/docs/worlds.md).
