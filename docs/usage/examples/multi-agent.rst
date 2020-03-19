Multi Agent Example
===================

With Holodeck, you can control more than one agent at once. Instead of calling 
``.step()``, which both

1. passes a single command to the main agent, and
2. ticks the simulation

you should call ``.act()``. Act supplies a command to a specific 
agent, but doesn't tick the game. 

Once all agents have received their actions, you can call ``.tick()`` to tick
the game.

After calling ``.act()``, every time you call ``.tick()`` the same command 
will be supplied to the agent. To change the command, just call ``.act()`` again.

The state returned from tick is also somewhat different. 

The state is now a dictionary from agent name to sensor dictionary. 

You can access the reward, terminal and location for the UAV as shown below.

Code
~~~~

::

   import holodeck
   import numpy as np

   env = holodeck.make('CyberPunkCity-Follow')
   env.reset()

   env.act('uav0', np.array([0, 0, 0, 100]))
   env.act('nav0', np.array([0, 0, 0]))
   for i in range(300):
      states = env.tick()

      # states is a dictionary
      task = states["uav0"]["FollowTask"]

      reward = task[0]
      terminal = task[1]
      location = states["uav0"]["LocationSensor"]
