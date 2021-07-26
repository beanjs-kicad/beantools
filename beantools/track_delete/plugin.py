import wx


from os import path
from pcbnew import ActionPlugin,GetBoard,Refresh


class TrackDeletePlugin(ActionPlugin):
    """Class that gathers the actionplugin stuff"""
    def defaults(self):
        self.name = "Track Delete"
        self.category = "Modify PCB"
        self.description = "track delete"
        self.icon_file_name = path.join(path.dirname(__file__), 'icon.png')
        self.show_toolbar_button = True

    def Run(self):
        board=GetBoard()
        track=self.getSelectedTrack()

        if track is None:
            return

        trackNetCode=track.GetNetCode()
        tracks=board.TracksInNet(trackNetCode)
        for track in tracks:
            board.Remove(track)
        
        # Refresh()

    def getSelectedTrack(self):
        board = GetBoard()
        tracks = board.GetTracks()
        selectedItem=None
        for i in range(len(tracks)):
            item=tracks[i]
            if item.IsSelected():
                selectedItem=item
                break
        
        return selectedItem






            
