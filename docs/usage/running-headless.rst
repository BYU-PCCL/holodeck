Using Holodeck Headless
=======================

On Linux, Holodeck can run headless without opening a viewport window. This
can happen automatically, or you can force it to not appear

Headless Mode vs Disabling Viewport Rendering
---------------------------------------------

These are two different features.

**Disabling Viewport Rendering** is calling the 
(:meth:`~holodeck.environments.HolodeckEnvironment.should_render_viewport`) 
method on a :class:`~holodeck.environments.HolodeckEnvironment`. This can be
done at runtime. It will appear as if the image being rendered in the viewport
has frozen, but :class:`~holodeck.sensors.RGBCamera` s and other sensors will 
still update correctly.

**Headless Mode** is when the viewport window does not appear. If Headless
Mode is manually enabled, it will also disable viewport rendering
automatically.

Forcing Headless Mode
---------------------

In :func:`holodeck.make`, set ``show_viewport`` to ``False``. 

.. note::
   This will also
   disable viewport rendering 
   (:meth:`~holodeck.environments.HolodeckEnvironment.should_render_viewport`)

   If you still want to render the viewport (ie for the 
   :class:`~holodeck.sensors.ViewportCapture`) when running headless,
   simply set 
   (:meth:`~holodeck.environments.HolodeckEnvironment.should_render_viewport`)
   to ``True``

Automatic Headless Mode
-----------------------

If the engine does not detect the ``DISPLAY`` environment variable, it will
not open a window. This will happen automatically if Holodeck is run from a
SSH session.

.. note::
   This will not disable viewport rendering.
