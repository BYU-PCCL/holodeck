.. _scenarios:

Scenarios
===================

What is a scenario?
-------------------

A scenario is a configuration for a Holodeck world, usually distributed with a 
package. It defines:

- Which world to load
- Agent Definitions
   - What type of agent they are
   - Where they are
   - What sensors they have
- Tasks
   - Which task
   - Which agents play which role in the task

.. tip::
   You can think of scenarios like a map or gametype variant from Halo: 
   the world or map itself doesn't change, but the things in the world
   and your objective can change. 

Scenarios allow the same world to be used for many different purposes, 
and allows you to extend and customize the scenarios we provide to
suit your needs without recompiling the engine.

When you call ``holodeck.make()`` to create an environment, you pass in the name
of a scenario, eg ``holodeck.make("UrbanCity-Follow")``. This tells Holodeck
which world to load and where to place agents.

.. _`scenario-files`:

Scenario File Format
--------------------

Scenario files are distributed in packages (see :ref:`package-contents`), and
must be named ``{WorldName}-{PackageName}.json``. By default they are stored
in the ``worlds/{PackageName}``, but they can be loaded externally as well.

Scenario File
~~~~~~~~~~~~~

.. code-block:: json

   {
      "name": "{Scenario Name}",
      "world": "{world it is associated with}",

      "agents":[
         "array of agent objects"
      ],

      "window_width":  1280,
      "window_height": 720
   }

``window_width/height`` control the size of the window opened when an environment
is created.

.. note::
   The first agent in the ``agents`` array is the "main agent"

Agent objects
~~~~~~~~~~~~~

.. code-block:: json

   {
      "agent_name": "uav0",
      "agent_type": "{agent types}",
      "sensors": [
         "array of sensor objects"
      ],
      "control_scheme": "{control scheme type}",
      "location": [1.0, 2.0, 3.0],
      "rotation": [1.0, 2.0, 3.0]
   }


.. note::
   Holodeck coordinates are **left handed** in meters. See :ref:`coordinate-system`

Here are the values that should be placed in ``agent_type``:

====================== ========================
Agent Type             String in agent_type
====================== ========================
:ref:`android-agent`    ``AndroidAgent``
:ref:`turtle-agent`     ``TurtleAgent``
:ref:`nav-agent`        ``NavAgent``
:ref:`sphere-agent`     ``SphereAgent``
:ref:`turtle-agent`     ``TurtleAgent``
====================== ========================

Here are the different control scheme values:

+-----------------------+--------------------------------+
| Agent Type            | Control Scheme String          |
+=======================+================================+
| :ref:`android-agent`  | ``android_torques``            |
+-----------------------+--------------------------------+
| :ref:`sphere-agent`   | ``sphere_discrete``            |
|                       +--------------------------------+
|                       | ``sphere_continuous``          |
+-----------------------+--------------------------------+  
| :ref:`nav-agent`      | ``nav_target_location``        |
+-----------------------+--------------------------------+
| :ref:`uav-agent`      | ``uav_torques``                |
|                       +--------------------------------+
|                       | ``uav_roll_pitch_yaw_rate_alt``|
+-----------------------+--------------------------------+


Sensor Objects
~~~~~~~~~~~~~~

.. code-block:: json

   {
      "sensor_type": "RGBCamera",
      "sensor_name": "FrontCamera",
      "location": [1.0, 2.0, 3.0],
      "rotation": [1.0, 2.0, 3.0],
      "socket": "socket name or """,
      "configuration": {
         
      }
   }

The only keys that are required in a sensor object is ``"sensor_type"``, the 
rest will default as shown below

.. code-block:: json

   {
      "sensor_name": "sensor_type",
      "location": [0, 0, 0],
      "rotation": [0, 0, 0],
      "socket": "",
      "configuration": {}
   }

.. _`configuration-block`:

Configuration Block 
~~~~~~~~~~~~~~~~~~~

The contents of the ``configuration`` block are sensor-specific. That block is
passed verbatim to the sensor itself, which parses it.

For example, the docstring for :class:`~holodeck.sensors.RGBCamera` states that
it accepts ``CaptureWidth`` and ``CaptureHeight`` parameters, so an example
sensor configuration would be:

.. code-block:: json

   {
      "sensor_name": "RBGCamera",
      "socket": "CameraSocket",
      "configuration": {
         "CaptureHeight": 1920,
         "CaptureWidth": 1080
      }
   }