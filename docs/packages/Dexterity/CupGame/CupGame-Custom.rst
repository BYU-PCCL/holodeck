.. _`cupgame-custom`:

CupGame-Custom
==============

**Type:** :ref:`cup-game-task`

This scenario has a hand agent positioned directly in front of the cup game.
The game is not automatically set up with any configuration, which requires
the user to call the :meth:`~holodeck.sensors.CupGameTask.start_game`
method and manually configure the game.

Agents
------

- ``hand0``: Main :ref:`Hand <hand-agent>` agent

See `CupGame-Custom.json <https://github.com/BYU-PCCL/holodeck-configs/blob/master/Dexterity/CupGame-Custom.json>`_.
