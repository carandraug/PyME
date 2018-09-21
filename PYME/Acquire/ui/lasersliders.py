#!/usr/bin/python

##################
# lasersliders.py
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
#import sys
from numpy import log2
import re

#redefine wxFrame with a version that hides when someone tries to close it
#dirty trick, but lets the Boa gui builder still work with frames we do this to
#from noclosefr import * 

class LaserSliders(wx.Panel):
    def __init__(self, parent, scopeState, winid=-1):
        # begin wxGlade: MyFrame1.__init__
        #kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Panel.__init__(self, parent, winid)

        #self.cam = cam
        self.scopeState = scopeState
        
        self.laserNames = []
        for k in self.scopeState.keys():
            m = re.match(r'Lasers\.(?P<laser_name>.*)\.Power', k)
            if not m is None:
                self.laserNames.append(m.group('laser_name'))
        
        self.laserNames.sort()
        #self.lasers = [l for l in lasers if l.IsPowerControlable()]
        #self.laserNames=[l.GetName() for l in lasers]
        
        self.sliders = []
        self.labels = []
        self.sliding = False
        #self.SetTitle("Piezo Control")
        
        sizer_2 = wx.BoxSizer(wx.VERTICAL)

        for c, laserName in enumerate(self.laserNames):
            sz = wx.BoxSizer(wx.HORIZONTAL)
            l = wx.StaticText(self, -1, laserName)
            self.labels.append(l)
            sz.Add(l, 0, wx.ALL, 2)

            sl = wx.Slider(self, -1, self.scopeState['Lasers.%s.Power' % laserName], 0, 10, size=wx.Size(150,-1),style=wx.SL_HORIZONTAL)#|wx.SL_AUTOTICKS|wx.SL_LABELS)
            sl.SetTickFreq(10,1)
            
            sz.Add(sl, 1, wx.ALL|wx.EXPAND, 2)
            sizer_2.Add(sz,1,wx.EXPAND,0)

            self.sliders.append(sl)

        #sizer_2.AddSpacer(5)

        wx.EVT_SCROLL(self,self.onSlide)
                
       
        #self.SetAutoLayout(1)
        self.SetSizer(sizer_2)
        sizer_2.Fit(self)
        #sizer_2.SetSizeHints(self)
        
        #self.Layout()
        # end wxGlade

    def onSlide(self, event):
        self.sliding = True
        try:
            sl = event.GetEventObject()
            ind = self.sliders.index(sl)
            #self.sl = sl
            #self.ind = ind
            #print((self.lasers[ind].power, self.lasers[ind].MAX_POWER*2**(sl.GetValue())/1024.))
            #self.lasers[ind].SetPower(self.lasers[ind].MAX_POWER*2**(sl.GetValue())/1024.)
            laserName = self.laserNames[ind]
            maxPower = self.scopeState['Lasers.%s.MaxPower' % laserName]
            self.scopeState['Lasers.%s.Power' % laserName] = (maxPower*2**(sl.GetValue())/1024.)
        finally:
            self.sliding = False

    def update(self):
        if not self.sliding:
            for ind, laserName in enumerate(self.laserNames):
                power = self.scopeState['Lasers.%s.Power' % laserName]
                maxPower = self.scopeState['Lasers.%s.MaxPower' % laserName]
                self.sliders[ind].SetValue(round(log2(max(power*1024/maxPower, 1))))
                self.labels[ind].SetLabel(laserName + ' - %3.2f'%(100*power/maxPower))
                
class LaserToggles(wx.Panel):
    def __init__(self, parent, scopeState, winid=-1):
        # begin wxGlade: MyFrame1.__init__
        #kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Panel.__init__(self, parent, winid)
        self.scopeState = scopeState
        
        #discover our siwtichable lasers
        self.laserNames = []
        for k in self.scopeState.keys():
            m = re.match(r'Lasers\.(?P<laser_name>.*)\.On', k)
            if not m is None:
                self.laserNames.append(m.group('laser_name'))
        
        self.laserNames.sort()

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        n = 0

        self.cBoxes = []

        for laserName in self.laserNames:
            cb = wx.CheckBox(self, -1, laserName)
            cb.SetValue(self.scopeState['Lasers.%s.On' % laserName])
            cb.Bind(wx.EVT_CHECKBOX, self.OnCbOn)
            
            self.cBoxes.append(cb)
            hsizer.Add(cb,1, wx.EXPAND, 0)
            n += 1
            if (n % 3) == 0:
                sizer_1.Add(hsizer,0, wx.EXPAND, 0)
                hsizer = wx.BoxSizer(wx.HORIZONTAL)

        sizer_1.Add(hsizer,0, wx.EXPAND, 0)


        #self.SetAutoLayout(1)
        self.SetSizerAndFit(sizer_1)
        
        #sizer_1.SetSizeHints(self)
        #self.Layout()
        # end wxGlade

    def OnCbOn(self, event):
        cb = event.GetEventObject()
        ind = self.cBoxes.index(cb)
        
        laserName = self.laserNames[ind]
        
        self.scopeState['Lasers.%s.On' % laserName] = cb.GetValue()


    def update(self, **kwargs):
        for laserName, cb in zip(self.laserNames, self.cBoxes):
            cb.SetValue(self.scopeState['Lasers.%s.On' % laserName])

class LaserSliders_(wx.Panel):
    def __init__(self, parent, lasers, winid=-1):
        # begin wxGlade: MyFrame1.__init__
        #kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Panel.__init__(self, parent, winid)

        #self.cam = cam
        self.lasers = [l for l in lasers if l.IsPowerControlable()]
        self.laserNames=[l.GetName() for l in self.lasers]
        
        self.sliders = []
        self.labels = []
        self.sliding = False
        #self.SetTitle("Piezo Control")
        
        sizer_2 = wx.BoxSizer(wx.VERTICAL)

        for c in range(len(self.lasers)):
            sz = wx.BoxSizer(wx.HORIZONTAL)
            l = wx.StaticText(self, -1, self.laserNames[c])
            self.labels.append(l)
            sz.Add(l, 0, wx.ALL, 2)
            #if sys.platform == 'darwin': #sliders are subtly broken on MacOS, requiring workaround
            #sl = wx.Slider(self, -1, self.lasers[c].GetPower(), 0, 10, size=wx.Size(150,-1),style=wx.SL_HORIZONTAL)#|wx.SL_AUTOTICKS|wx.SL_LABELS)
            sl = wx.Slider(self, -1, self.lasers[c].GetPower(), 0, 100, size=wx.Size(150,-1),style=wx.SL_HORIZONTAL)#|wx.SL_AUTOTICKS|wx.SL_LABELS)
            #else: #sane OS's
            #    sl = wx.Slider(self, -1, self.cam.laserPowers[c], 0, 1000, size=wx.Size(300,-1),style=wx.SL_HORIZONTAL|wx.SL_AUTOTICKS|wx.SL_LABELS)

            #sl.SetSize((800,20))
            sl.SetTickFreq(10,1)
            #sz = wx.StaticBoxSizer(wx.StaticBox(self, -1, self.laserNames[c] + " [mW]"), wx.HORIZONTAL)
            
            sz.Add(sl, 1, wx.ALL|wx.EXPAND, 2)
            sizer_2.Add(sz,1,wx.EXPAND,0)

            self.sliders.append(sl)

        #sizer_2.AddSpacer(5)

        wx.EVT_SCROLL(self,self.onSlide)
                
       
        #self.SetAutoLayout(1)
        self.SetSizer(sizer_2)
        sizer_2.Fit(self)
        #sizer_2.SetSizeHints(self)
        
        #self.Layout()
        # end wxGlade

    def onSlide(self, event):
        self.sliding = True
        try:
            sl = event.GetEventObject()
            ind = self.sliders.index(sl)
            self.sl = sl
            self.ind = ind
            print((self.lasers[ind].power, self.lasers[ind].MAX_POWER*2**(sl.GetValue())/1024.))
            self.lasers[ind].SetPower(self.lasers[ind].MAX_POWER*2**(sl.GetValue())/1024.)
        finally:
            self.sliding = False

    def update(self, **kwargs):
        if not self.sliding:
            for ind, L in enumerate(self.lasers):
                p = L.power
                self.sliders[ind].SetValue(round(log2(max(p*1024/L.MAX_POWER, 1))))
                self.labels[ind].SetLabel(self.laserNames[ind] + ' - %3.2f'%(100*p))

            


