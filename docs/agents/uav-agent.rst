.. _`uav-agent`:

UavAgent
========

Images
------

.. image:: images/uav-perspective.png
   :scale: 20%

.. image:: images/uav-top.png
   :scale: 20%

.. image:: images/uav-side.png
   :scale: 20%

Description
-----------
A quadcopter UAV agent. 

See the :class:`~holodeck.agents.UavAgent` class. 

Control Schemes
---------------
- UAV Torques
- UAV Roll / Pitch / Yaw targets

See :class:`~holodeck.agents.UavAgent` for more details on how the control
schemes work.

Sockets
-------

- ``CameraSocket`` located underneath the uav body
- ``Viewport`` located behind the agent

.. image:: images/uav-sockets.png
   :scale: 30%
