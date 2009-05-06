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

    def __init__(self,*args,**kw):
        super(FviewPeriodicTrigger,self).__init__(*args,**kw)
        self.trigger_device = None

    def set_all_fview_plugins(self,plugins):
        """Get reference to 'FView external trigger' plugin"""

        # This method is called by FView to let plugins know about
        # each other.

        for plugin in plugins:
            if plugin.get_plugin_name()=='FView external trigger':
                self.trigger_device = plugin.trigger_device

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
