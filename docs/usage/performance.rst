.. _`improving-performance`:

==============================
Improving Holodeck Performance
==============================

Holodeck is fairly performant by default, but you can also sacrifice
features to increase your frames per second.

.. contents::
   :local:

RGBCamera
---------

By far, the biggest single thing you can do to improve performance is to
disable the ``RGBCamera``. Rendering the camera every frame causes a
context switch deep in the rendering code of the engine, which has a 
significant performance penalty.

This chart shows how much performance you can expect to gain or loose 
adjusting the RGBCamera (left column is frame time in milleseconds)

+------------+----------+---------+-----------+---------+----------+---------+
| Resolution | UrbanCity          | MazeWorld           | AndroidPlayground  |
+============+==========+=========+===========+=========+==========+=========+
| No Camera  | 8.55 ms  | 117 fps | 4.69  ms  | 213 fps | 2.47 ms  | 405 fps |
+------------+----------+---------+-----------+---------+----------+---------+
| 64         | 17   ms  | 59 fps  | 11    ms  | 91 fps  | 4.87 ms  | 205 fps |
+------------+----------+---------+-----------+---------+----------+---------+
| 128        | 20   ms  | 50 fps  | 11.6  ms  | 86 fps  | 5.59 ms  | 179 fps |
+------------+----------+---------+-----------+---------+----------+---------+
| 256        | 22   ms  | 45 fps  | 14.71 ms  | 68 fps  | 9.02 ms  | 111 fps |
+------------+----------+---------+-----------+---------+----------+---------+
| 512        | 35   ms  | 29 fps  | 30.8  ms  | 32 fps  | 24.81 ms | 40 fps  |
+------------+----------+---------+-----------+---------+----------+---------+
| 1024       | 89   ms  | 11 fps  | 84.2  ms  | 12 fps  | 94.55 ms | 11 fps  |
+------------+----------+---------+-----------+---------+----------+---------+
| 2048       | 410  ms  | 2  fps  | 383   ms  | 3  fps  | 366   ms | 3  fps  |
+------------+----------+---------+-----------+---------+----------+---------+

Disabling the ``RGBCamera``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Remove the ``RGBCamera`` entry from the scenario configuration file you are
using. 

See :ref:`custom-scenarios`.

Lowering the ``RGBCamera`` resolution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lowering the resolution of the ``RGBCamera`` can also help speed things up.
Create a :ref:`custom scenario <custom-scenarios>` and in the 
:ref:`configuration block <configuration-block>` for the ``RGBCamera`` set the
``CaptureWidth`` and ``CaptureHeight``.

See :class:`~holodeck.sensors.RGBCamera` for more details.

Changing ticks per capture
~~~~~~~~~~~~~~~~~~~~~~~~~~

The number of ticks per capture can be adjusted to give a lower average frame
time.

See the 
:meth:`~holodeck.sensors.RGBCamera.set_ticks_per_capture` method.

Disable Viewport Rendering
--------------------------

Rendering the viewport window can be unnecessary during training. You can 
disable the viewport with the 
:meth:`~holodeck.environments.HolodeckEnvironment.should_render_viewport` 
method.

At lower ``RGBCamera`` resolutions, you can expect a ~40% frame time reduction.

Change Render Quality
---------------------

You can adjust Holodeck to render at a lower (or higher) quality to improve
performance. See the 
:meth:`~holodeck.environments.HolodeckEnvironment.set_render_quality` method

Below is a comparison of render qualities and the frame time in ms

========= =========== =========== ===================
 Quality   MazeWorld   UrbanCity   AndroidPlayground
========= =========== =========== ===================
 ``0``       10.34       12.33       6.63
 ``1``       10.53       15.06       6.84
 ``2``       14.81       19.19       8.66
 ``3``       15.58       21.78       9.2
========= =========== =========== ===================
