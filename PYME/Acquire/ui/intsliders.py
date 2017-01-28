#!/usr/bin/python

##################
# intsliders.py
#
# Copyright David Baddeley, 2009
# d.baddeley@auckland.ac.nz
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##################

#!/usr/bin/env python
# generated by wxGlade 0.3.3 on Thu Sep 23 08:22:22 2004


import wx

#redefine wxFrame with a version that hides when someone tries to close it
#dirty trick, but lets the Boa gui builder still work with frames we do this to
#from PYME.Acquire.noclosefr import *

#import sys

timeChoices = ['10', '25', '50', '100', '250', '500', '1000', '2500']

class IntegrationSliders_(wx.Panel):
    def __init__(self, chaninfo, parent, scope, winid=-1):
        # begin wxGlade: MyFrame1.__init__
        #kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Panel.__init__(self, parent, winid)

        self.chaninfo = chaninfo
        self.sliders = []
        self.cboxes = []
        self.scope = scope
        #self.SetTitle("Piezo Control")
        
        sizer_2 = wx.BoxSizer(wx.VERTICAL)

        nsliders = len(self.chaninfo.itimes)
        
        for c in range(nsliders):
            #if not sys.platform == 'darwin':
            sl = wx.Slider(self, -1, self.chaninfo.itimes[c], 1, min(5*self.chaninfo.itimes[c], 10000), size=wx.Size(100,-1),style=wx.SL_HORIZONTAL|wx.SL_AUTOTICKS)#|wx.SL_LABELS)
            #else:#workaround for broken mouse event handling (and hence sliders) on MacOS
            #    sl = wx.Slider(self, -1, self.chaninfo.itimes[c], 1, min(5*self.chaninfo.itimes[c], 10000), size=wx.Size(300,-1),style=wx.SL_HORIZONTAL|wx.SL_AUTOTICKS|wx.SL_LABELS)

            sl_val = wx.ComboBox(self, -1, choices = timeChoices, value = '%d' % self.chaninfo.itimes[c], size=(65, -1), style=wx.CB_DROPDOWN|wx.TE_PROCESS_ENTER)
 
            #sl.SetSize((800,20))
            sl.SetTickFreq(100,1)

            if nsliders > 1:
                sz = wx.StaticBoxSizer(wx.StaticBox(self, -1, self.chaninfo.names[c] + " (ms)"), wx.HORIZONTAl)
            else:
                sz = wx.BoxSizer(wx.HORIZONTAL)

            sz.Add(sl, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 2)
            sz.Add(sl_val, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            sz.Add(wx.StaticText(self, -1, 'ms'), 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
            sizer_2.Add(sz,1,wx.EXPAND,0)

            self.sliders.append(sl)
            self.cboxes.append(sl_val)

            sl_val.Bind(wx.EVT_COMBOBOX, self.onCombobox)
            sl_val.Bind(wx.EVT_TEXT_ENTER, self.onCombobox)

        sizer_2.AddSpacer(5)
        wx.EVT_SCROLL_CHANGED(self,self.onSlide)
                
       
        #self.SetAutoLayout(1)
        self.SetSizer(sizer_2)
        sizer_2.Fit(self)
        #sizer_2.SetSizeHints(self)
        
        #self.Layout()
        # end wxGlade

    def onSlide(self, event):
        sl = event.GetEventObject()
        ind = self.sliders.index(sl)
        self.sl = sl
        self.ind = ind
        self.chaninfo.itimes[ind] = sl.GetValue()
        self.cboxes[ind].SetValue('%d' % sl.GetValue())
        self.sliders[ind].SetRange(1, min(5*self.chaninfo.itimes[ind], 10000))
        self.scope.frameWrangler.stop()
        self.scope.frameWrangler.start()

    def onCombobox(self, event):
        cb = event.GetEventObject()
        ind = self.cboxes.index(cb)
        print((cb.GetValue()))
        self.chaninfo.itimes[ind] = float(cb.GetValue())
        self.sliders[ind].SetValue(self.chaninfo.itimes[ind])
        self.sliders[ind].SetRange(1, min(5*self.chaninfo.itimes[ind], 10000))
        self.scope.frameWrangler.stop()
        self.scope.frameWrangler.start()


    def update(self):
        for ind in range(len(self.piezos)):
            self.sliders[ind].SetValue(self.chaninfo.itimes[ind])
            self.sliders[ind].SetRange(1, min(5*self.chaninfo.itimes[ind], 10000))

            
class IntegrationSliders(wx.Panel):
    def __init__(self, parent, scope, winid=-1):
        # begin wxGlade: MyFrame1.__init__
        #kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Panel.__init__(self, parent, winid)

        #self.chaninfo = chaninfo
        self.sliders = []
        self.cboxes = []
        self.scope = scope
        #self.SetTitle("Piezo Control")
        
        sizer_2 = wx.BoxSizer(wx.VERTICAL)

        nsliders = 1#len(self.chaninfo.itimes)
        
        #for c in range(nsliders):
        c = 1
        
        itime = 1e3*self.scope.state['Camera.IntegrationTime']

        
        sl = wx.Slider(self, -1, itime, 1, min(5*itime, 10000), size=wx.Size(100,-1),style=wx.SL_HORIZONTAL)#|wx.SL_AUTOTICKS)#|wx.SL_LABELS)
        
        sl_val = wx.ComboBox(self, -1, choices = timeChoices, value = '%d' % itime, size=(65, -1), style=wx.CB_DROPDOWN|wx.TE_PROCESS_ENTER)
 
        #sl.SetSize((800,20))
        sl.SetTickFreq(100,1)

        if nsliders > 1:
            sz = wx.StaticBoxSizer(wx.StaticBox(self, -1, self.chaninfo.names[c] + " (ms)"), wx.HORIZONTAl)
        else:
            sz = wx.BoxSizer(wx.HORIZONTAL)

        sz.Add(sl, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 2)
        sz.Add(sl_val, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        sz.Add(wx.StaticText(self, -1, 'ms'), 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        sizer_2.Add(sz,1,wx.EXPAND,0)

        self.sliders.append(sl)
        self.cboxes.append(sl_val)

        sl_val.Bind(wx.EVT_COMBOBOX, self.onCombobox)
        sl_val.Bind(wx.EVT_TEXT_ENTER, self.onCombobox)

        sizer_2.AddSpacer(5)
        #wx.EVT_SCROLL_CHANGED(self,self.onSlide)
        sl.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.onSlide)
        
        self.scope.state.registerChangeListener('Camera.IntegrationTime', self.update)
                
       
        #self.SetAutoLayout(1)
        self.SetSizer(sizer_2)
        sizer_2.Fit(self)
        #sizer_2.SetSizeHints(self)
        
        #self.Layout()
        # end wxGlade

    def onSlide(self, event):
        sl = event.GetEventObject()
        ind = self.sliders.index(sl)
        self.sl = sl
        self.ind = ind
        #self.chaninfo.itimes[ind] = sl.GetValue()
        self.scope.state['Camera.IntegrationTime'] = sl.GetValue()/1e3
        new_itime= self.scope.state['Camera.IntegrationTime']
        self.cboxes[ind].SetValue('%1.2f' % (1e3*new_itime))
        self.sliders[ind].SetValue(1e3*new_itime)
        self.sliders[ind].SetRange(1, min(5*self.scope.state['Camera.IntegrationTime']*1e3, 10000))
        #self.scope.frameWrangler.stop()
        #self.scope.frameWrangler.start()

    def onCombobox(self, event):
        cb = event.GetEventObject()
        ind = self.cboxes.index(cb)
        #   print((cb.GetValue()))
        itime = float(cb.GetValue())
        self.scope.state['Camera.IntegrationTime'] = itime/1e3
        new_itime= self.scope.state['Camera.IntegrationTime']
        self.cboxes[ind].SetValue('%1.2f' % (1e3*new_itime))
        self.sliders[ind].SetValue(new_itime*1e3)
        self.sliders[ind].SetRange(1, min(5*new_itime*1e3, 10000))
        #self.scope.frameWrangler.stop()
        #self.scope.frameWrangler.start()


    def update(self, value, **kwargs):
        ind = 0
        #print 'update: ', value
        value = value*1e3
        
        self.sliders[ind].SetValue(value)
        self.sliders[ind].SetRange(1, min(5*value, 10000))
        self.cboxes[ind].SetValue('%d' % value)

