Viewport Hotkeys
================

When the viewport window is open, and the environment is being ticked (with 
calls to :meth:`~holodeck.environment.HolodeckEnvironment.tick` or
:meth:`~holodeck.environment.HolodeckEnvironment.step`, there are a few
hotkeys you can use.

.. _`hotkeys`:

Hotkeys
~~~~~~~

The AgentFollower, or the camera that the viewport displays, can be 
manipulated as follows:

+----------+-----------------------+-----------------------------------------+
| Key      | Action                | Description                             |
+==========+=======================+=========================================+
| ``c``    | Toggle camera mode    | Toggles the camera from a chase camera  |
|          |                       | and perspective camera, which shows what|
|          |                       | the agent's camera sensor sees.         |
+----------+-----------------------+-----------------------------------------+
| ``v``    | Toggle spectator mode | Toggles spectator mode, which allows you|
|          |                       | to free-cam around the world.           |
+----------+-----------------------+-----------------------------------------+
| ``w``    | Move camera           | Move the viewport camera around when in |
| ``a``    |                       | spectator/free-cam mode.                |
| ``s``    |                       |                                         |
| ``d``    |                       |                                         |
+----------+-----------------------+-----------------------------------------+
| ``q``    | Descend               | For spectator/free-cam mode             |
| ``ctrl`` |                       |                                         |
+----------+-----------------------+-----------------------------------------+
| ``e``    | Ascend                | For spectator/free-cam mode             |
| ``space``|                       |                                         |
+----------+-----------------------+-----------------------------------------+
| ``shift``| Turbo                 | Move faster when in spectator/free-cam  |
+----------+-----------------------+-----------------------------------------+
| ``tab``  | Cycle through agents  | When not in spectator/free-cam mode,    |
|          |                       | cycles through the agents in the world  |
+----------+-----------------------+-----------------------------------------+
| ``h``    | Toggle HUD            | The HUD displays the name and location  |
|          |                       | of the agent the viewport is following, |
|          |                       | or the location of the camera if the    |
|          |                       | viewport is detached (spectator mode)   |
|          |                       |                                         |
|          |                       | Note that this will interfere with the  |
|          |                       | ViewportCapture sensor                  |
+----------+-----------------------+-----------------------------------------+

Opening Console
---------------

Pressing ``~`` will open Unreal Engine 4's developer console, which has a few useful 
commands. See `the Unreal Docs <https://api.unrealengine.com/udk/Three/ConsoleCommands.html>`_
for a complete list of commands.

**Useful Commands**

- ``stat fps``
  
  Prints the frames per second on the screen.
