.. _`follow-task`:

Follow Task
===========

The follow task calculates a reward based on the distance to an actor and
optionally if the agent has line of sight to it. 

If OnlyWithinSight is true, the reward is set to the percent distance covered from the 
MinDistance to the ToFollow target *if* the angle from the agent to target is
less than FOVRadians *and* is there is nothing blocking the agent's line of sight.
Otherwise the reward is 0.

If OnlyWithinSight is false, then the reward is set to the the percent distance
covered from the MinDistance to the ToFollow Actor.

The reward will be a value 0 to 100

Configuration
-------------

Each of the following parameters can be placed in the configuration field
for a distance task sensor (see :ref:`scenario files <scenario-files>`.)

ToFollow
~~~~~~~~

Name of the actor to follow.

``"ToFollow": "name-of-actor"``

.. TODO: Mention there is a list of actors that you can follow in the world
         documentation

OnlyWithinSight
~~~~~~~~~~~~~~~

Boolean value indicating if the reward should be calculated only when the 
actor to follow is within the agent's field of view.

``"OnlyWithinSight": true``

FOVRadians
~~~~~~~~~~

Float value, the field of view of the agent, in radians. See above how this is used in
the reward calculation.

``"FOVRadians": 23.0``

MinDistance
~~~~~~~~~~~

Float value, used to specify the minimum distance 
.. TODO: this is very confusing for me

``"MinDistance": 512.0``

TargetHeight
~~~~~~~~~~~~

The height of the target, used when determining if the agent can see the target (OnlyWithinSight)

``"TargetHeight": 10.0f``

Example
-------

.. code-block:: json

   {
       "OnlyWithinSight": true,
       "FOVRadains": 5.0,
       "MinDistance": 1024.0,
       "TargetHeight": 10.0
   }