.. _fview-plugin-tutorial-periodic-trigger:

****************************************************************
FView plugin tutorial: periodic triggering of an external device
****************************************************************

This tutorial illustrates the steps necessary to trigger an external
device at a constant, relatively slow rate. Specifically, we will
generate a pulse on the :ref:`CamTrig device
<fview_ext_trig-overview>` every N frames.

A working copy of this can be found at http://github.com/motmot/fview_periodic_trigger/

Prerequisites
=============

 * the :ref:`CamTrig hardware device <fview_ext_trig-overview>` plugged in and
   functioning
 * :mod:`fview_ext_trig` (software for the CamTrig) installed and functioning

Step 1 - Build the file layout
==============================

Your plugin will be a standard Python package. Create the following
directories (``base`` should be your base directory, such as
"fview_periodic_trigger")::

  base
  base/motmot
  base/motmot/fview_periodic_trigger

And create the following empty files::

  base/motmot/__init__.py
  base/motmot/fview_periodic_trigger/__init__.py

Step 2 - Create setup.py
========================

Now, edit ``base/setup.py`` to contain the following (modify as necessary)::

  from setuptools import setup, find_packages
  import sys,os

  setup(name='motmot.fview_periodic_trigger',
      description='periodic trigger plugin for FView',
      version='0.0.1',
      packages = find_packages(),
      author='Andrew Straw',
      author_email='strawman@astraw.com',
      url='http://code.astraw.com/projects/motmot',
      entry_points = {
    'motmot.fview.plugins':'fview_periodic_trigger = motmot.fview_periodic_trigger.fview_periodic_trigger:FviewPeriodicTrigger',
    },
      )

This is a standard setuptools__ file for distributing and installing
Python packages that tells Python which files to install and some
associated meta-data.

__ http://pypi.python.org/pypi/setuptools

The ``packages = find_packages()`` line tells setuptools to look for
standard Python packages (directories with an __init__.py
file). Because you just created these directories and files in Step 1,
setuptools automatically knows these directories contain the files to
be installed.

The ``entry_points`` line tells setuptools that we want to register a
plugin. Our plugin is registered under the ``motmot.fview.plugins``
key. FView inquires for any plugins under this key. This particular
plugin is called ``fview_periodic_trigger``. It is defined in the
module ``motmot.fview_periodic_trigger.fview_periodic_trigger`` and
the class ``FviewPeriodicTrigger``, which we create below.

Step 3 - Create the plugin logic
================================

Now we're going to create the module
``motmot.fview_periodic_trigger.fview_periodic_trigger`` with our
new class ``FviewPeriodicTrigger``. Open a new file named::

  base/motmot/fview_periodic_trigger/fview_periodic_trigger.py

The contents of this file::

  from __future__ import with_statement, division

  import pkg_resources
  import enthought.traits.api as traits

  import motmot.fview.traited_plugin as traited_plugin
  import motmot.fview_ext_trig.ttrigger as ttrigger

  from enthought.traits.ui.api import View, Item, Group

  class FviewPeriodicTrigger(traited_plugin.HasTraits_FViewPlugin):
      plugin_name = 'periodic trigger'
      trigger_device = traits.Instance(ttrigger.DeviceModel)

      Nth_frame = traits.Int(100)

      traits_view = View(Group(Item(name='Nth_frame')))

      def set_all_fview_plugins(self,plugins):
          """Get reference to 'FView external trigger' plugin"""

          # This method is called by FView to let plugins know about
          # each other.

          for plugin in plugins:
              if plugin.get_plugin_name()=='FView external trigger':
                  self.trigger_device = plugin.trigger_device
          if self.trigger_device is None:
              raise RuntimeError('this plugin requires "FView external trigger"')

      def process_frame(self,cam_id,buf,buf_offset,timestamp,framenumber):
          if framenumber%self.Nth_frame == 0:
              if self.trigger_device is not None:

                   # fire pulse on EXT_TRIG1
                  self.trigger_device.ext_trig1 = True

                   # toggle LED
                  self.trigger_device.led1 = not self.trigger_device.led1

          draw_points = []
          draw_linesegs = []
          return draw_points, draw_linesegs

The initial several lines are standard ``import`` statements. Note
that this plugin uses Enthought's Traits__ module to facilitate event
handling and GUI elements.

__ http://code.enthought.com/projects/traits/docs/html/index.html

Next, we define the class ``FviewPeriodicTrigger``, which is derived
from the ``traited_plugin.HasTraits_FViewPlugin`` base class. This
base class implements most of the functionality required for FView
plugins, so we just have to implement or override a few things.

First, in our class, we give our plugin a name, in this case
``periodic trigger``. Next, we tell traits that we're going to have a
``trigger_device`` variable and an ``Nth_frame`` variable. The
``trigger_device`` variable is an instance of the
``motmot.fview_ext_trig.ttrigger.DeviceModel``, and is used to
interact with the Motmot CamTrig hardware. The ``Nth_frame`` variable
defines how frequently we will pulse the external trigger pin
(EXT_TRIG1) and toggle the LED.

The ``set_all_fview_plugins`` method is required because we need to
find the CamTrig trigger device. We do this by checking each of the
plugins registered with FView to see if it is the 'FView external
trigger' plugin . This plug will have an attribute called
``trigger_device``, which we want to keep a reference to.

Finally, the business end of this plugin, like most FView plugins, is
the ``process_frame`` method. This method gets called on every frame
and can be used to do realtime image analysis. We're keeping things
simple in this tutorial, however, and only testing the framecount and
pulsing the external trigger and toggling the LED if it's a multiple
of the ``Nth_frame`` variable. The return value of ``process_frame``
are any points and line segments that FView should draw over the main
display. In our case, we don't want to draw anything, so we return a
couple of empty lists.
