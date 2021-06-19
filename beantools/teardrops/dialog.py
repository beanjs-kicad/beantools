#!/usr/bin/env python

# Teardrop for pcbnew using filled zones
# This is the plugin WX dialog
# (c) Niluje 2019 thewireddoesntexist.org
#
# Based on Teardrops for PCBNEW by svofski, 2014 http://sensi.org/~svo
# Cubic Bezier upgrade by mitxela, 2021 mitxela.com

import wx
import wx.xrc
import sys
import time
import pcbnew

from os import path
from .td import SetTeardrops, RmTeardrops, __version__

class TeardropDialog ( wx.Dialog ):

    def __init__(self,board):
        wx.Dialog.__init__ ( self, None, id = wx.ID_ANY, title = u"Teardrops", pos = wx.DefaultPosition, size = wx.Size( 450,353 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

        self.board=board
        self.initGui()
        self.initDialog()

    def initDialog(self):
        self.SetTitle("Teardrops (v{0})".format(__version__))
        self.rbx_action.Bind(wx.EVT_RADIOBOX, self.onAction)
        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)
        self.but_cancel.Bind(wx.EVT_BUTTON, self.onCloseWindow)
        self.but_ok.Bind(wx.EVT_BUTTON, self.onProcessAction)
        self.m_bitmap_help.SetBitmap(wx.Bitmap( path.join(path.dirname(path.realpath(__file__)), "teardrops-help.png")))
        self.SetMinSize(self.GetSize())
        
    def initGui(self):

		#self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        if sys.version_info[0] == 2:
            self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        else:
            self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bvs_main = wx.BoxSizer( wx.VERTICAL )

        rbx_actionChoices = [ u"Set Teardrops", u"Remove All Teardrops" ]
        self.rbx_action = wx.RadioBox( self, wx.ID_ANY, u"Action", wx.DefaultPosition, wx.DefaultSize, rbx_actionChoices, 1, wx.RA_SPECIFY_ROWS )
        self.rbx_action.SetSelection( 0 )
        bvs_main.Add( self.rbx_action, 0, wx.ALL, 5 )

        bhs_params = wx.BoxSizer( wx.HORIZONTAL )

        gs_params = wx.GridSizer( 0, 2, 0, 0 )

        self.st_hpercent = wx.StaticText( self, wx.ID_ANY, u"Horizontal percent", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.st_hpercent.Wrap( -1 )

        gs_params.Add( self.st_hpercent, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.EXPAND|wx.FIXED_MINSIZE, 5 )

        self.sp_hpercent = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 100, 50 )
        gs_params.Add( self.sp_hpercent, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.EXPAND|wx.FIXED_MINSIZE|wx.SHAPED, 5 )

        self.st_vpercent = wx.StaticText( self, wx.ID_ANY, u"Vertical percent", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.st_vpercent.Wrap( -1 )

        gs_params.Add( self.st_vpercent, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.EXPAND|wx.FIXED_MINSIZE, 5 )

        self.sp_vpercent = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 100, 90 )
        gs_params.Add( self.sp_vpercent, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.EXPAND|wx.FIXED_MINSIZE|wx.SHAPED, 5 )

        self.st_nbseg = wx.StaticText( self, wx.ID_ANY, u"Number of segments", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.st_nbseg.Wrap( -1 )

        gs_params.Add( self.st_nbseg, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.EXPAND|wx.FIXED_MINSIZE, 5 )

        self.sp_nbseg = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 2, 100, 10 )
        gs_params.Add( self.sp_nbseg, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.EXPAND|wx.FIXED_MINSIZE|wx.SHAPED, 5 )


        bhs_params.Add( gs_params, 1, wx.ALIGN_CENTER_VERTICAL|wx.EXPAND|wx.SHAPED, 5 )

        self.m_bitmap_help = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
        bhs_params.Add( self.m_bitmap_help, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.ALL, 5 )

        bhs_params.Add( ( 0, 0), 1, wx.EXPAND, 5 )
        bvs_main.Add( bhs_params, 1, wx.EXPAND, 5 )

        bvs_options = wx.BoxSizer( wx.VERTICAL )

        self.cb_include_smd_pads = wx.CheckBox( self, wx.ID_ANY, u"Include SMD pads", wx.DefaultPosition, wx.DefaultSize, 0 )
        bvs_options.Add( self.cb_include_smd_pads, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.ALL|wx.EXPAND, 5 )

        self.cb_discard_in_same_zone = wx.CheckBox( self, wx.ID_ANY, u"Do not insert teardrop inside same net zones", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.cb_discard_in_same_zone.SetValue(True)
        bvs_options.Add( self.cb_discard_in_same_zone, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.ALL|wx.EXPAND, 5 )

        self.cb_follow_tracks = wx.CheckBox( self, wx.ID_ANY, u"Follow tracks if shorter than needed", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.cb_follow_tracks.SetValue(True)
        bvs_options.Add( self.cb_follow_tracks, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.ALL|wx.EXPAND, 5 )

        bvs_options.Add( ( 0, 0), 1, wx.EXPAND, 5 )

        bvs_main.Add( bvs_options, 1, wx.EXPAND, 5 )

        self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bvs_main.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )

        bhs_modal = wx.BoxSizer( wx.HORIZONTAL )

        self.but_cancel = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        bhs_modal.Add( self.but_cancel, 0, wx.ALL, 5 )

        self.but_ok = wx.Button( self, wx.ID_ANY, u"Ok", wx.DefaultPosition, wx.DefaultSize, 0 )
        bhs_modal.Add( self.but_ok, 0, wx.ALL, 5 )


        bvs_main.Add( bhs_modal, 0, wx.ALIGN_RIGHT, 5 )


        self.SetSizer( bvs_main )
        self.Layout()

        self.Centre( wx.BOTH )

    def onAction(self, e):
        """Enables or disables the parameters/options elements"""
        els = [self.st_hpercent, self.sp_hpercent, self.st_vpercent,
               self.sp_vpercent, self.st_nbseg, self.sp_nbseg,
               self.cb_include_smd_pads, self.cb_discard_in_same_zone,
               self.cb_follow_tracks]
        for i, el in enumerate(els):
            if self.rbx_action.GetSelection() == 0:
                el.Enable()
            else:
                el.Disable()

    def onProcessAction(self, event):
        """Executes the requested action"""
        if self.rbx_action.GetSelection() == 0:
            start = time.time()
            count = SetTeardrops(self.sp_hpercent.GetValue(),
                                 self.sp_vpercent.GetValue(),
                                 self.sp_nbseg.GetValue(),
                                 self.board,
                                 self.cb_include_smd_pads.IsChecked(),
                                 self.cb_discard_in_same_zone.IsChecked(),
                                 self.cb_follow_tracks.IsChecked())
            wx.MessageBox("{} Teardrops inserted, took {:.3f} seconds".format(count, time.time()-start))
        else:
            count = RmTeardrops(pcb=self.board)
            wx.MessageBox("{0} Teardrops removed".format(count))
        pcbnew.Refresh() #Show up newly added vias
        self.EndModal(wx.ID_OK)

    def onCloseWindow(self, event):
        self.EndModal(wx.ID_OK)


    def __del__( self ):
        pass