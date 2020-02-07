Getting Started
===============
First, see :ref:`installation` to get the ``holodeck`` package and 
``DefaultWorlds`` installed.

A minimal Holodeck usage example is below:

::

   import holodeck
   import numpy as np

   env = holodeck.make("UrbanCity-MaxDistance")

   # The UAV takes 3 torques and a thrust as a command.
   command = np.array([0, 0, 0, 100])

   env.reset()
   for _ in range(180):
      state, reward, terminal, info = env.step(command)

Notice that:

1. You pass the name of a :ref:`scenario<scenarios>` into ``holodeck.make``
   
   See :ref:`all-packages` for all of the different worlds and scenarios that
   are available.
2. The interface of Holodeck is designed to be familiar to `OpenAI Gym`_

.. _`OpenAI Gym`: https://gym.openai.com/

3. You must call ``.reset()`` before calling ``.step()`` or ``.tick()``

You can access data from a specific sensor with the state dictionary:

::

   location_data = state["LocationSensor"]

**That's it!** Holodeck is meant to be fairly simple to use. 

Check out the different
:ref:`worlds<all-packages>` that are available, read the 
:ref:`API documentation<holodeck-api-index>`, or get started on making your own
custom :ref:`scenarios<scenarios>`.

Code Examples
-------------

Below are some snippets that show how to use different aspects of Holodeck.

.. toctree::
   :maxdepth: 1
   :caption: Contents:
   :glob:

   examples/*


There is also an `examples.py`_ in the root of the `holodeck repo`_ with more 
example code.

.. _`examples.py`: https://github.com/BYU-PCCL/holodeck/blob/master/example.py

.. _`holodeck repo`: https://github.com/BYU-PCCL/holodeck
