import wx


from os import path
from pcbnew import ActionPlugin, GetBoard,Refresh
from .bga import IsBGA,ParseBGAInfo
from .fo import BGAFanout

class FanoutPlugin(ActionPlugin):
    """Class that gathers the actionplugin stuff"""
    def defaults(self):
        self.name = "Fanout"
        self.category = "Modify PCB"
        self.description = "Fanout pins withs BGA footprint"
        self.icon_file_name = path.join(path.dirname(__file__), 'icon.png')
        self.show_toolbar_button = True

    def Run(self):
        selItem=self.getSelectedFootprint()
        
        if selItem == None:
            wx.MessageBox("No footprint are selected")
            return
        
        pads=selItem.Pads()

        if not IsBGA(pads):
            wx.MessageBox("the footprint not BGA")
            return
        
        
        info=ParseBGAInfo(selItem)
        BGAFanout(info,pads)

        Refresh()
        wx.MessageBox(f"fanout finished")

    def getSelectedFootprint(self):
        board = GetBoard()
        fps = board.GetFootprints()
        selectedItem=None
        for i in range(len(fps)):
            item=fps[i]
            if item.IsSelected():
                selectedItem=item
                break
        
        return selectedItem




            
