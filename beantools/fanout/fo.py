from math import inf
from pcbnew import PCB_TRACK,PCB_VIA,wxPoint
from pcbnew import GetBoard

def BGAFanout(info,pads):
    board=GetBoard()
    design=board.GetDesignSettings()
    traceWidth=design.GetCurrentTrackWidth()
    viaDrill=design.GetCurrentViaDrill()
    viaSize=design.GetCurrentViaSize()
    
    for pad in pads:
        offset=info.spacing/2

        startPos=pad.GetPosition()

        if startPos.x == info.leftTop.x or startPos.y == info.leftTop.y:
            continue
        
        if startPos.x == info.rightBottom.x or startPos.y == info.rightBottom.y:
            continue
        
        vecDir=wxPoint(startPos.x-info.center.x,startPos.y-info.center.y)
        if vecDir.x == 0:
            vecDir.x=1
        
        if vecDir.y == 0:
            vecDir.y=1

        vecDir.x=int(vecDir.x/abs(vecDir.x))
        vecDir.y=int(vecDir.y/abs(vecDir.y))

        endPos=wxPoint(startPos.x+int(offset*vecDir.x),startPos.y+int(offset*vecDir.y))


        newTrack=PCB_TRACK(board)
        newTrack.SetStart(startPos)
        newTrack.SetEnd(endPos)
        newTrack.SetNet(pad.GetNet())
        newTrack.SetLayer(pad.GetLayer())
        newTrack.SetWidth(traceWidth)
        board.Add(newTrack)

        newVia=PCB_VIA(board)
        newVia.SetPosition(endPos)
        newVia.SetNet(pad.GetNet())
        newVia.SetDrill(viaDrill)
        newVia.SetWidth(viaSize)
        board.Add(newVia)

    
    pass

