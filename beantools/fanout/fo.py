import math
import re

from pcbnew import PCB_TRACK,PCB_VIA,wxPoint
from pcbnew import GetBoard

def degreesToAngle(degrees):
    return 2 * math.pi * degrees/360

def isSkip(info,pad):
    padName = pad.GetPadName()

    pinName=re.match("[A-Z]+",padName).group()
    pinNumb=int(padName.replace(pinName,''))

    if pinName in info.skipEdges:
        return True
    
    if pinNumb in info.skipEdges:
        return True
    
    return False


def BGAFanout(info,pads):
    board=GetBoard()
    design=board.GetDesignSettings()
    traceWidth=design.GetCurrentTrackWidth()
    viaDrill=design.GetCurrentViaDrill()
    viaSize=design.GetCurrentViaSize()
    
    for pad in pads:
        offset=info.spacing/2
        angle=degreesToAngle(90-info.degrees)

        startPos=pad.GetPosition()

        if isSkip(info,pad):
            continue

        # if startPos.x == info.leftTop.x or startPos.y == info.leftTop.y or \
        #    startPos.x == info.leftTop.x+info.spacing or startPos.y == info.leftTop.y+info.spacing :
        #     continue
        
        # if startPos.x == info.rightBottom.x or startPos.y == info.rightBottom.y or \
        #     startPos.x == info.rightBottom.x-info.spacing or startPos.y == info.rightBottom.y-info.spacing :
        #     continue
        
        unitVectorX=startPos.x-info.center.x
        unitVectorY=startPos.y-info.center.y

        if unitVectorX == 0:
            unitVectorX=1
        
        if unitVectorY == 0:
            unitVectorY=1

        unitVectorX=unitVectorX/abs(unitVectorX)
        unitVectorY=unitVectorY/abs(unitVectorY)
        
        vectorX = unitVectorX * math.cos(angle) - unitVectorY * math.sin(angle)
        vectorY = unitVectorX * math.sin(angle) + unitVectorY * math.cos(angle)

        endPos=wxPoint(startPos.x+round(vectorX*offset),startPos.y+round(vectorY*offset))


        newTrack=PCB_TRACK(board)
        newTrack.SetStart(startPos)
        newTrack.SetEnd(endPos)
        newTrack.SetNet(pad.GetNet())
        newTrack.SetLayer(pad.GetLayer())
        newTrack.SetWidth(traceWidth)
        
        board.Add(newTrack)
        
        newVia=PCB_VIA(board)
        newVia.SetPosition(newTrack.GetEnd())
        newVia.SetNet(pad.GetNet())
        newVia.SetDrill(viaDrill)
        newVia.SetWidth(viaSize)

        board.Add(newVia)
        
        # break
    
    pass

