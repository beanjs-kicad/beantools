import wx


from os import path
from pcbnew import ActionPlugin,GetBoard,LayerName
from .dialog import TrackSwapDialog

class TrackSwapPlugin(ActionPlugin):
    """Class that gathers the actionplugin stuff"""
    def defaults(self):
        self.name = "Layer swap"
        self.category = "Modify PCB"
        self.description = "Tracks in swap layer"
        self.icon_file_name = path.join(path.dirname(__file__), 'icon.png')
        self.show_toolbar_button = True

    def Run(self):
        choices=[]
        layers={}
        layer_map={}

        board=GetBoard()
        tracks=board.Tracks()

        # print(len(tracks))

        for track in tracks:
            layer_id=track.GetLayer()
            layer_name=LayerName(layer_id)
            if not (layer_name in choices):
                choices.append(layer_name)

            if not (layer_id in layers):
                layers[layer_id]=[]

            if not (layer_name in layer_map):
                layer_map[layer_name]=layer_id

            if track.GetClass() != "PCB_VIA":
                layers[layer_id].append(track)

            # print(f"class: {track.GetClass()}")
            # print(f"layer: {LayerName(track.GetLayer())}")

        # print(layers)
        dg=TrackSwapDialog(choices,layers,layer_map)
        dg.ShowModal()






            
