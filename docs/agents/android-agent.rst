.. _`android-agent`:

AndroidAgent
=============

Images
------

.. image:: images/android-front.png
   :scale: 30%

.. image:: images/android-side.png
   :scale: 30%

Description
-----------
An android agent that can be controlled via torques supplied to its joints.
See :class:`holodeck.agents.AndroidAgent` for more details.

Control Schemes
---------------
.. TODO: Link to Control Scheme page

- Android Torques

.. TODO: Don't punt on the joint layout

.. TODO: Example code

Sockets
---------------

- "CameraSocket" located in the middle of the android's face
- "Viewport" located behind the agent
- All bones in the android's mesh are sockets, and their names are documented here: :class:`holodeck.agents.AndroidAgent`
