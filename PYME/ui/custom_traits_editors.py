from traitsui.wx.editor import Editor
from traitsui.wx.basic_editor_factory import BasicEditorFactory

from traits.api import List

import wx

class _CBEditor (Editor):
    """
    Simple Traits UI date editor.  Shows a text box, and a date-picker widget.
    """

    def init ( self, parent ):
        """
        Finishes initializing the editor by creating the underlying widget.
        """


        self.control = wx.ComboBox(parent,
                                   size=(120,-1),
                                   style = wx.CB_DROPDOWN, value=self.value, choices=self.factory.choices)
        self.control.Bind(wx.EVT_COMBOBOX, self.text_changed)
        self.control.Bind(wx.EVT_TEXT, self.text_changed)
        return


    def text_changed(self, event):
        """
        Event for when calendar is selected, update/create date string.
        """
        self.value = self.control.GetValue()
        return


    def update_editor ( self ):
        """
        Updates the editor when the object trait changes externally to the
        editor.
        """
        if self.value:
            choices = [self.control.GetString(n) for n in range(self.control.GetCount())]
            try:
                n = choices.index(self.value)
                self.control.SetSelection(n)
            except ValueError:
                self.control.SetValue(self.value)

        return

class CBEditor(BasicEditorFactory):
    klass = _CBEditor

    choices = List()