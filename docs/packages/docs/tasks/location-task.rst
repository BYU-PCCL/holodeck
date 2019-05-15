Location Task
=============

Calculates a sparse distance reward based on the distance to a location or an
actor. Can maximize or minimize a distance. A reward is only given only if the
agent exceeds the GoalDistance

Configuration
-------------

Each of the following parameters can be placed in the configuration field
for a distance task sensor (see :ref:`scenario files <scenario-files>`.)

Distance Target
~~~~~~~~~~~~~~~

The Location task needs an actor or a location to use in the distance calculations.

``"DistanceActor": "name-of-actor"``

or

``"DistanceLocation": [3.14, 2.71, 117]``

GoalDistance
~~~~~~~~~~~~~

Float value, used to determine if a reward should be given.

``"GoalDistance": 1024.0``

MaximizeDistance
~~~~~~~~~~~~~~~~

Boolean value, to indicate if a reward should be given for minimizing or maximizing
the distance to the target.


Example
-------

.. code-block:: json

   {
       "DistanceTarget": "gyrating-cube",
       "GoalDistance": 1024.0,
       "MaximizeDistance": false
   }

