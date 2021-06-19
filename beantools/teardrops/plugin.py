#!/usr/bin/env python

# Teardrop for pcbnew using filled zones
# This is the action plugin interface
# (c) Niluje 2019 thewireddoesntexist.org
#
# Based on Teardrops for PCBNEW by svofski, 2014 http://sensi.org/~svo
# Cubic Bezier upgrade by mitxela, 2021 mitxela.com

import wx

from os import path
from pcbnew import ActionPlugin, GetBoard
from .dialog import TeardropDialog

class TeardropPlugin(ActionPlugin):
    """Class that gathers the actionplugin stuff"""
    def defaults(self):
        self.name = "Teardrops"
        self.category = "Modify PCB"
        self.description = "Manages teardrops on a PCB"
        self.icon_file_name = path.join(path.dirname(__file__), 'icon.png')
        self.show_toolbar_button = True

    def Run(self):
        td=TeardropDialog(GetBoard())
        td.ShowModal()
