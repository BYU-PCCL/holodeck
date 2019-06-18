Viewport Hotkeys
================

When the viewport window is open, and the environment is being ticked (with 
calls to :meth:`~holodeck.environment.HolodeckEnvironment.tick` or
:meth:`~holodeck.environment.HolodeckEnvironment.step`, there are a few
hotkeys you can use.

.. _`moving-viewport`:

Moving the Viewport
-------------------

The AgentFollower, or the camera that the viewport displays, can be manipulated
as follows:

+----------+------------------------+-----------------------------------------+
| Key      | Action                 | Description                             |
+----------+------------------------+-----------------------------------------+
| ``c``    | Toggle attached camera | Toggles the camera from a chase camera  |
|          |                        | and perspective camera, which shows what|
|          |                        | the agent's camera sensor sees.         |
+----------+------------------------+-----------------------------------------+
| ``v``    | Toggle spectator mode  | Toggles spectator mode, which allows you|
|          |                        | to free-cam around the world.           |
|          |                        |                                         |
|          |                        | Use the mouse, ``w``, ``a``, ``s``,     |
|          |                        | ``d``, and ``space`` to ascend and      |
|          |                        | ``shift`` to move faster.               |
+----------+------------------------+-----------------------------------------+
| ``tab``  | Cycle through agents   | When not in spectator mode, use ``tab`` |
|          |                        | to cycle through the agents in the world|
+----------+------------------------+-----------------------------------------+

Opening Console
---------------

Pressing ``~`` will open Unreal Engine 4's developer console, which has a few useful 
commands. See `the Unreal Docs <https://api.unrealengine.com/udk/Three/ConsoleCommands.html>`_
for a complete list of commands.

**Useful Commands**

- ``stat fps``
  
  Prints the frames per second on the screen.