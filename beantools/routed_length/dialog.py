import wx

from pcbnew import GetBoard,ToMils

class RoutedLengthDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__ ( self, None, id = wx.ID_ANY, title = u"Routed Length", pos = wx.DefaultPosition, size = wx.Size( 420,680 ), style = wx.CAPTION|wx.CLOSE_BOX)
        self.lb=wx.ListCtrl(self,id=wx.ID_ANY,pos=wx.Point(8,8),size=wx.Size(404,664),style=wx.LC_REPORT)
        self.lb.AppendColumn("Net",width=200)
        self.lb.AppendColumn("Length",width=120)

        self.Visiable=False

        self.timer=wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onInterval,self.timer)
        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)

    def Show(self):
        self.Visiable=not self.Visiable
        wx.Dialog.Show(self,self.Visiable)

        if self.Visiable:
            self.timer.Start(500)
        else:
            self.timer.Stop()

    def onCloseWindow(self,e):
        self.Visiable=False
        self.timer.Stop()
        wx.Dialog.Show(self,self.Visiable)
        # self.EndModal(wx.ID_OK)

    def onInterval(self,e):
        board=GetBoard()

        lbItems={}
        tracks=board.Tracks()

        for item in tracks:
            group=item.GetParentGroup()
            # groupName="Default"
            # if group != None:
            #     groupName=group.GetName()

            iKey=f"{item.GetShortNetname()}"
            if iKey in lbItems:
                lbItems[iKey]+=item.GetLength()
            else:
                lbItems[iKey]=item.GetLength()

        self.lb.DeleteAllItems()
        for key in lbItems.keys():
            val=f"{round(ToMils(lbItems[key]),2)} mils"
            self.lb.Append([key,val])

        pass

    def __del__(self):
        self.timer.Stop()
        pass
