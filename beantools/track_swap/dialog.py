import wx
import wx.xrc
import pcbnew


class TrackSwapDialog(wx.Dialog):
    def __init__(self,choices,layers,layer_map):
        wx.Dialog.__init__ ( self, None, id = wx.ID_ANY, title = u"Track Swap", pos = wx.DefaultPosition, size = wx.Size( 440,120 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER )

        self.layers=layers
        self.layer_map=layer_map

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        
        bvs_main = wx.BoxSizer( wx.VERTICAL )
        gs_params = wx.GridSizer( 0, 4, 0, 0 )

        self.src_layer_lb = wx.StaticText( self, wx.ID_ANY, u"Src Layer:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.src_layer_lb.Wrap( -1 )
        gs_params.Add( self.src_layer_lb, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.src_layer_cb = wx.ComboBox(self, id=wx.ID_ANY, value="", pos=wx.DefaultPosition,size=wx.DefaultSize, choices=choices, style=0, validator=wx.DefaultValidator)
        gs_params.Add( self.src_layer_cb, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.dst_layer_lb = wx.StaticText( self, wx.ID_ANY, u"Dst Layer:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.dst_layer_lb.Wrap( -1 )
        gs_params.Add( self.dst_layer_lb, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.dst_layer_cb = wx.ComboBox(self, id=wx.ID_ANY, value="", pos=wx.DefaultPosition,size=wx.DefaultSize, choices=choices, style=0, validator=wx.DefaultValidator)
        gs_params.Add( self.dst_layer_cb, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL, 5 )

        bhs_modal = wx.BoxSizer( wx.HORIZONTAL )

        self.but_cancel = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        bhs_modal.Add( self.but_cancel, 0, wx.ALL, 5 )

        self.but_ok = wx.Button( self, wx.ID_ANY, u"Ok", wx.DefaultPosition, wx.DefaultSize, 0 )
        bhs_modal.Add( self.but_ok, 0, wx.ALL, 5 )
        
        bvs_main.Add( gs_params, 1, wx.EXPAND, 5)
        bvs_main.Add( bhs_modal, 1, wx.ALIGN_RIGHT, 5 )
        

        self.SetSizer(bvs_main)
        self.Layout()
        self.Centre( wx.BOTH )

        self.Bind(wx.EVT_CLOSE,self.onCloseWindow)
        self.but_ok.Bind(wx.EVT_BUTTON, self.onProcessAction)
        self.but_cancel.Bind(wx.EVT_BUTTON, self.onCloseWindow)


    def __del__(self):
        # self.Destroy()
        pass

    def onCloseWindow(self, event):
        self.EndModal(wx.ID_OK)

    def onProcessAction(self, event):

        src_layer_name=self.src_layer_cb.GetStringSelection()
        dst_layer_name=self.dst_layer_cb.GetStringSelection()

        if src_layer_name == "" or dst_layer_name == "":
            wx.MessageBox("not select layer")
            return
        
        if src_layer_name == dst_layer_name:
            wx.MessageBox("layer error")
            return

        src_layer_id=self.layer_map[src_layer_name]
        dst_layer_id=self.layer_map[dst_layer_name]

        src_tracks=self.layers[src_layer_id]
        dst_tracks=self.layers[dst_layer_id]

        self.layerSwap(src_tracks,dst_layer_id)
        self.layerSwap(dst_tracks,src_layer_id)

        pcbnew.Refresh()
        wx.MessageBox("swap finished!!")

    def layerSwap(self,tracks,layer_id):
        for track in tracks:
            track.SetLayer(layer_id)
         

        
        