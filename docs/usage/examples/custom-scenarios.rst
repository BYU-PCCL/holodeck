.. _`custom-scenarios`:

==============================
Custom Scenario Configurations
==============================

Holodeck worlds are meant to be configurable by changing out the scenario
(see :ref:`scenarios`). There are some scenarios included with Holodeck 
packages distributed as ``.json`` files, but Holodeck is intended to be used
with user-created scenarios as well. 

These can be created using a dictionary in a Python script or by creating a
``.json`` file. Both methods follow the same format, see :ref:`scenario-files`

.. _`dictionary-scenario-config`:

Using a Dictionary for a Scenario Config
----------------------------------------

Create a dictionary in Python that matches the structure specified in
:ref:`scenario-files`, and pass it in to :func:`holodeck.make`.

Example
~~~~~~~

.. code-block:: python
   :emphasize-lines: 27
   :linenos:

   import holodeck

   cfg = {
       "name": "test_rgb_camera",
       "world": "ExampleWorld",
       "package_name": "DefaultWorlds",
       "main_agent": "sphere0",
       "agents": [
           {
               "agent_name": "sphere0",
               "agent_type": "SphereAgent",
               "sensors": [
                   {
                       "sensor_type": "RGBCamera",
                       "socket": "CameraSocket",
                       "configuration": {
                           "CaptureWidth": 512,
                           "CaptureHeight": 512
                       }
                   }
               ],
              "control_scheme": 0,
               "location": [0, 0, 0]
           }
       ]
   }

   with holodeck.make(scenario_cfg=cfg) as env:
       env.tick()


Using a ``.json`` file for a Scenario Config
--------------------------------------------

You can specify a custom scenario by creating a ``.json`` file that follows
the format given in :ref:`scenario-files` and either:

1. Placing it in Holodeck's scenario search path
2. Loading it yourself and parsing it into a dictionary, and then using that 
   dictionary as described in :ref:`dictionary-scenario-config`

Holodeck's Scenario Search Path
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you give a scenario name to :func:`holodeck.make`, Holodeck will search
look each package folder (see :ref:`package-locations`) until it finds a
``.json`` file that matches the scenario name. 

So, you can place your custom scenario ``.json`` files in that folder and 
Holodeck will automatically find and use it.

.. warning::
   If you remove and re-install a package, Holodeck will clear the contents of
   that folder
