Cup Game Task
=============

Calculates reward based on whether the correct cup is touched and whether
the ball is touched. A reward of 1 is given if the correct cup is touched
and no other cups are touched, and a reward of 2 and terminal is given
when the ball itself is touched and no incorrect cups are touched.

The cup game task only works in the CupGame world in the dexterity package.
The game will not start if a cup game task is not added to an agent.

Configuration
-------------

Each of the following parameters can be placed in the configuration field
for a cup game task sensor (see :ref:`scenario files <scenario-files>`.)
The configuration can also be changed programmatically by using


Speed
~~~~~

The cups will rotate faster with a higher speed. The speed works best between 1 and 10.

``"Speed": 3``


NumShuffles
~~~~~~~~~~~

To increase difficulty, the number of shuffles can be increased.

``"NumShuffles": 10``


Seed
~~~~

Giving a seed ensures that the cups will rotate the same way every time.
If left empty, the cups will rotate randomly.

``"Seed": 1``


Example
-------

.. code-block:: json

    {
        "Speed": 5,
        "NumShuffles": 1,
        "Seed": 0
    }

