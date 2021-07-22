import wx
import pcbnew

from os import path
from pcbnew import ActionPlugin,GetBoard


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
            ref=fp.Reference()
            layerId=ref.GetLayer()

            if layerId==pcbnew.User_1 or layerId==pcbnew.User_2:
                continue

            if layerId == pcbnew.F_SilkS:
                ref.SetLayer(pcbnew.User_1)
            
            if layerId == pcbnew.B_SilkS:
                ref.SetLayer(pcbnew.User_2)

            textSize=designSettings.GetTextSize(layerId)
            ref.SetTextThickness(designSettings.GetTextThickness(layerId))
            ref.SetTextWidth(textSize.GetWidth())
            ref.SetTextHeight(textSize.GetHeight())


            fpBoundingBox=self.footprintBoundingBox(fp)
            fpCenter=fpBoundingBox.GetCenter()
            ref.SetPosition(fpCenter)

        wx.MessageBox("align finished!!")
        pcbnew.Refresh()
    
    def footprintBoundingBox(self,fp):
        fpLayerId=fp.GetLayer()

        ctrLayerId=pcbnew.F_CrtYd
        if fpLayerId== pcbnew.B_Cu :
            ctrLayerId=pcbnew.B_CrtYd

        gItems = fp.GraphicalItems()

        minx=1000000000000
        miny=1000000000000
        maxx=-1
        maxy=-1
        for item in gItems:
            if item.GetLayer() == ctrLayerId:
                iBox=item.GetBoundingBox()
                if iBox.GetLeft() < minx:
                    minx=iBox.GetLeft()
                
                if iBox.GetRight() > maxx:
                    maxx=iBox.GetRight()

                if iBox.GetTop() < miny:
                    miny=iBox.GetTop()
                
                if iBox.GetBottom() > maxy:
                    maxy=iBox.GetBottom()

        return pcbnew.EDA_RECT(pcbnew.wxPoint(minx,miny),pcbnew.wxSize(maxx-minx,maxy-miny))




            
