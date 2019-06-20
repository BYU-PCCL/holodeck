.. _`sphere-agent`:

SphereAgent
===========

Images
------

.. image:: images/sphere.png
   :scale: 30%

Description
-----------

A basic sphere robot that moves along a plane. The SphereAgent does not have 
physics - it simply computes its next location and teleports there, as 
compared to the :ref:`turtle-agent` which has mass and momentum.

See :class:`~holodeck.agents.SphereAgent` for more details.

Control Schemes
---------------

- Discrete
- Continuous Control Scheme

See :class:`~holodeck.agents.SphereAgent` for details on how to use 
the control schemes.

.. TODO: Example code?

Sockets
---------------

- ``CameraSocket`` located at the front of the sphere body
- ``Viewport`` located behind the agent

.. image:: images/sphere-sockets.png
   :scale: 30%