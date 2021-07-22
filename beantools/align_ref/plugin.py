import wx


from os import path
from pcbnew import ActionPlugin,GetBoard,B_SilkS,F_SilkS,User_1,User_2

class AlignRefPlugin(ActionPlugin):
    """Class that gathers the actionplugin stuff"""
    def defaults(self):
        self.name = "Align Ref"
        self.category = "Modify PCB"
        self.description = ""
        self.icon_file_name = path.join(path.dirname(__file__), 'icon.png')
        self.show_toolbar_button = True

    def Run(self):
        board=GetBoard()
        footprints=board.GetFootprints()
        designSettings=board.GetDesignSettings()

        for fp in footprints:
            fpCenter=fp.GetCenter()
            ref=fp.Reference()
            layerId=ref.GetLayer()

            if layerId==User_1 or layerId==User_2:
                continue

            if layerId == F_SilkS:
                ref.SetLayer(User_1)
            
            if layerId == B_SilkS:
                ref.SetLayer(User_2)

            textSize=designSettings.GetTextSize(layerId)
            ref.SetTextThickness(designSettings.GetTextThickness(layerId))
            ref.SetTextWidth(textSize.GetWidth())
            ref.SetTextHeight(textSize.GetHeight())
            ref.SetPosition(fpCenter)

        wx.MessageBox("align finished!!")
            






            
