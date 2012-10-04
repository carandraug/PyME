#!/usr/bin/python

##################
# chanedit.py
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
# generated by wxGlade 0.3.3 on Fri Sep 24 09:22:05 2004

import wx

class ChanEditDialog(wx.Dialog):
    def __init__(self, cname, cols, hw, *args, **kwds):
        # begin wxGlade: ChanEditDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)

        self.cname = cname
        self.cols = cols
        self.hw = hw

        self.panel_1 = wx.Panel(self, -1)
        self.label_1 = wx.StaticText(self.panel_1, -1, "Name: ")
        self.tName = wx.TextCtrl(self.panel_1, -1, cname)
        self.cbSh0 = wx.CheckBox(self.panel_1, -1, "0")
        self.cbSh0.SetValue(hw&1)
        self.cbSh1 = wx.CheckBox(self.panel_1, -1, "1")
        self.cbSh1.SetValue(hw&2)
        self.cbSh2 = wx.CheckBox(self.panel_1, -1, "2")
        self.cbSh2.SetValue(hw&4)
        self.cbSh3 = wx.CheckBox(self.panel_1, -1, "3")
        self.cbSh3.SetValue(hw&8)
        self.cbSh4 = wx.CheckBox(self.panel_1, -1, "4")
        self.cbSh4.SetValue(hw&16)
        self.cbSh5 = wx.CheckBox(self.panel_1, -1, "5")
        self.cbSh5.SetValue(hw&32)
        self.cbSh6 = wx.CheckBox(self.panel_1, -1, "6")
        self.cbSh6.SetValue(hw&64)
        self.cbSh7 = wx.CheckBox(self.panel_1, -1, "7")
        self.cbSh7.SetValue(hw&128)
        self.cbBW = wx.CheckBox(self.panel_1, -1, "B/W")
        self.cbBW.SetValue(cols&1)
        self.cbRed = wx.CheckBox(self.panel_1, -1, "Red")
        self.cbRed.SetValue(cols&2)
        self.cbGreen1 = wx.CheckBox(self.panel_1, -1, "Green1")
        self.cbGreen1.SetValue(cols&4)
        self.cbGreen2 = wx.CheckBox(self.panel_1, -1, "Green2")
        self.cbGreen2.SetValue(cols&8)
        self.cbBlue = wx.CheckBox(self.panel_1, -1, "Blue")
        self.cbBlue.SetValue(cols&16)
        self.bOK = wx.Button(self.panel_1, -1, "OK")
        self.bCancel = wx.Button(self.panel_1, -1, "Cancel")

        wx.EVT_BUTTON(self, self.bOK.GetId(), self.onOK)
        wx.EVT_BUTTON(self, self.bCancel.GetId(), self.onCancel)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: ChanEditDialog.__set_properties
        self.SetTitle("Edit Channel")
        self.bOK.SetDefault()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: ChanEditDialog.__do_layout
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.BoxSizer(wx.VERTICAL)
        coloursize = wx.StaticBoxSizer(wx.StaticBox(self.panel_1, -1, "Colours"), wx.HORIZONTAL)
        shutsize = wx.StaticBoxSizer(wx.StaticBox(self.panel_1, -1, "Shutters"), wx.HORIZONTAL)
        namesize = wx.BoxSizer(wx.HORIZONTAL)
        namesize.Add(self.label_1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        namesize.Add(self.tName, 1, wx.ALL|wx.EXPAND, 3)
        grid_sizer_1.Add(namesize, 0, wx.EXPAND, 0)
        shutsize.Add(self.cbSh0, 0, wx.ALL, 3)
        shutsize.Add(self.cbSh1, 0, wx.ALL, 3)
        shutsize.Add(self.cbSh2, 0, wx.ALL, 3)
        shutsize.Add(self.cbSh3, 0, wx.ALL, 3)
        shutsize.Add(self.cbSh4, 0, wx.ALL, 3)
        shutsize.Add(self.cbSh5, 0, wx.ALL, 3)
        shutsize.Add(self.cbSh6, 0, wx.ALL, 3)
        shutsize.Add(self.cbSh7, 0, wx.ALL, 3)
        grid_sizer_1.Add(shutsize, 1, wx.ALL|wx.EXPAND, 3)
        coloursize.Add(self.cbBW, 0, wx.ALL, 3)
        coloursize.Add(self.cbRed, 0, wx.ALL, 3)
        coloursize.Add(self.cbGreen1, 0, wx.ALL, 3)
        coloursize.Add(self.cbGreen2, 0, wx.ALL, 3)
        coloursize.Add(self.cbBlue, 0, wx.ALL, 3)
        grid_sizer_1.Add(coloursize, 1, wx.ALL|wx.EXPAND, 3)
        sizer_4.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        sizer_5.Add((20, 20), 1, wx.EXPAND, 0)
        sizer_5.Add(self.bOK, 0, wx.ALL, 3)
        sizer_5.Add(self.bCancel, 0, wx.ALL, 3)
        sizer_4.Add(sizer_5, 0, wx.EXPAND, 0)
        self.panel_1.SetAutoLayout(1)
        self.panel_1.SetSizer(sizer_4)
        sizer_4.Fit(self.panel_1)
        sizer_4.SetSizeHints(self.panel_1)
        sizer_6.Add(self.panel_1, 1, wx.EXPAND, 0)
        self.SetAutoLayout(1)
        self.SetSizer(sizer_6)
        sizer_6.Fit(self)
        sizer_6.SetSizeHints(self)
        self.Layout()
        # end wxGlade

    def onOK(self, event):
        self.cname = self.tName.GetValue()
        if not (len(self.cname) > 0):
            md = wx.MessageDialog(self, 'Name cannot be empty', 'Invalid Name', wx.OK)
            md.ShowModal()
            return

        if not (self.cname.find(' ') == -1):
            md = wx.MessageDialog(self, 'Name cannot contain spaces', 'Invalid Name', wx.OK)
            md.ShowModal()
            return

        self.cols = self.cbBW.GetValue() + self.cbRed.GetValue()*2 + self.cbGreen1.GetValue()*4
        self.cols = self.cols + self.cbGreen2.GetValue()*8 + self.cbBlue.GetValue()*16

        if not self.cols > 0:
            md = wx.MessageDialog(self, 'Must select at least one colour', 'Invalid Colours', wx.OK)
            md.ShowModal()
            return
        
        self.hw = self.cbSh0.GetValue() + self.cbSh1.GetValue()*2 + self.cbSh2.GetValue()*4 + self.cbSh3.GetValue()*8
        self.hw = self.hw + self.cbSh4.GetValue()*16 + self.cbSh5.GetValue()*32 + self.cbSh6.GetValue()*64 + self.cbSh7.GetValue()*128
               
        self.EndModal(True)

    def onCancel(self, event):
        self.EndModal(False)

# end of class ChanEditDialog

