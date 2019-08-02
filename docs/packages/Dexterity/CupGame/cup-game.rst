CupGame
=======

.. image:: cup-game.png

This is a small room with a game of ball and cups sitting on a table. In order
to activate the game, an agent must have the CupGameTask added to it. If you 
want to reconfigure the task to change the number of cup shuffles or the speed
of each shuffle, call :meth:`~holodeck.sensors.CupGameTask.start_game` or 
alter the config file.

Layout
------

.. image:: cup-game-top.png
   :scale: 50%


.. toctree::
   :maxdepth: 1
   :caption: Scenarios
   :glob:

   CupGame-*

