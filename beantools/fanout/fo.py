import math
import wx

from pcbnew import PCB_TRACK,PCB_VIA,wxPoint
from pcbnew import GetBoard,EDA_UNITS_DEGREES

def BGAFanout(info,pads):
    board=GetBoard()
    design=board.GetDesignSettings()
    traceWidth=design.GetCurrentTrackWidth()
    viaDrill=design.GetCurrentViaDrill()
    viaSize=design.GetCurrentViaSize()
    
    for pad in pads:
        offset=info.spacing/2

        startPos=pad.GetPosition()

        if startPos.x == info.leftTop.x or startPos.y == info.leftTop.y or \
           startPos.x == info.leftTop.x+info.spacing or startPos.y == info.leftTop.y+info.spacing :
            continue
        
        if startPos.x == info.rightBottom.x or startPos.y == info.rightBottom.y or \
            startPos.x == info.rightBottom.x-info.spacing or startPos.y == info.rightBottom.y-info.spacing :
            continue
        
        vectorX=startPos.x-info.center.x
        vectorY=startPos.y-info.center.y

        if vectorX == 0:
            vectorX=1
        
        if vectorY == 0:
            vectorY=1

        vectorX=vectorX/abs(vectorX)
        vectorY=vectorY/abs(vectorY)
        # print(f"vectorX:{vectorX} vectorY:{vectorY}")
        
        newX = vectorX * math.cos(2 * math.pi * info.degrees/360)- vectorY * math.sin(2 * math.pi * info.degrees/360)
        newY = vectorX * math.sin(2 * math.pi * info.degrees/360)+ vectorY * math.cos(2 * math.pi * info.degrees/360)

        endPos=wxPoint(startPos.x+round(newX*offset),startPos.y+round(newY*offset))


        newTrack=PCB_TRACK(board)
        newTrack.SetStart(startPos)
        newTrack.SetEnd(endPos)
        newTrack.SetNet(pad.GetNet())
        newTrack.SetLayer(pad.GetLayer())
        newTrack.SetWidth(traceWidth)
        # newTrack.Rotate(startPos,math.sin(2 * math.pi * info.degrees/360))
        
        board.Add(newTrack)
        
        newVia=PCB_VIA(board)
        newVia.SetPosition(newTrack.GetEnd())
        newVia.SetNet(pad.GetNet())
        newVia.SetDrill(viaDrill)
        newVia.SetWidth(viaSize)

        board.Add(newVia)
        
        # break
    
    pass

