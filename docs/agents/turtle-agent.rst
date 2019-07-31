.. _`turtle-agent`:

TurtleAgent
===========

.. image:: images/turtle.png
   :scale: 30%

Description
-----------
A simple turtle-bot agent with an arrow pointing forwards. Its radius is 
approximately 25cm and is approximately 10cm high.

The TurtleAgent moves when forces are applied to it - so it has momentum and
mass, compared to the :ref:`sphere-agent` which teleports around. The 
TurtleAgent is subject to gravity and can climb ramps and slopes.

See :class:`~holodeck.agents.TurtleAgent` for more details.

Sockets
-------

- ``CameraSocket`` located at the front of the body
- ``Viewport`` located behind the agent

.. image:: images/turtle-sockets.png
   :scale: 30%
