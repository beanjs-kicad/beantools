import wx


from os import path
from pcbnew import ActionPlugin
from .dialog import RoutedLengthDialog

# class BoardObserver(BOARD_LISTENER):
#     # def __init__(self):
#     #     BOARD_LISTENER.__init__(self)

#     def OnBoardItemAdded(self,board,item):
#         wx.MessageBox("OnBoardItemAdded")
#         pass
    
#     def OnBoardItemsAdded(self,board,items):
#         wx.MessageBox("OnBoardItemsAdded")
#         pass
    
#     def OnBoardItemRemoved(self,board,item):
#         wx.MessageBox("OnBoardItemRemoved")
#         pass
    
#     def OnBoardItemsRemoved(self,board,items):
#         wx.MessageBox("OnBoardItemsRemoved")
#         pass

#     def OnBoardNetSettingsChanged(self,board):
#         wx.MessageBox("OnBoardNetSettingsChanged")
#         pass

#     def OnBoardItemChanged(self,board,item):
#         wx.MessageBox("OnBoardItemChanged")
#         pass

#     def OnBoardItemsChanged(self,board,items):
#         wx.MessageBox("OnBoardItemsChanged")
#         pass

#     def OnBoardHighlightNetChanged(self,board):
#         wx.MessageBox("OnBoardHighlightNetChanged")
#         pass

class RoutedLengthPlugin(ActionPlugin):
    """Class that gathers the actionplugin stuff"""
    def defaults(self):
        self.name = "Routed Length"
        self.category = "Modify PCB"
        self.description = "Show Routed Length"
        self.icon_file_name = path.join(path.dirname(__file__), 'icon.png')
        self.show_toolbar_button = True
        self.dialog=RoutedLengthDialog()

    def Run(self):
        self.dialog.Show()
    
        




            
