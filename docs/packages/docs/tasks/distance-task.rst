Distance Task
=============

The distance tasks calculates a dense distance based reward. It can be 
configured to have the agent either maximize or minimize the distance from a 
location, actor or the agent's starting location.


Configuration
-------------

Each of the following parameters can be placed in the configuration field
for a distance task sensor (see :ref:`scenario files <scenario-files>`.)

Target Location
~~~~~~~~~~~~~~~
One of these options must be given, otherwise the reward will be calculated
from the agent's start location.

- ``"DistanceActor": "name of an actor to follow"``
- ``"DistanceLocation": [3.14, 15, 92]``

Interval
~~~~~~~~

The interval controls the distance an agent must cover before it receives a 
reward.

``"Interval": 5``

GoalDistance
~~~~~~~~~~~~

This distance is used to determine if the task has reached its terminal state
and the agent has travelled far enough away.

``"GoalDistance": 500``

MaximizeDistance
~~~~~~~~~~~~~~~~

Boolean value to indicate if the distance should be maximized or not.

``"MaximizeDistance": true``

Example
-------
.. code-block:: json

   {
       "DistanceActor": "red-cube",
       "Interval": 10,
       "GoalDistance": 1000,
       "MaximizeDistance": true   
   }