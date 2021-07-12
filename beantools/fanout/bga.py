import math
from pcbnew import PAD_SHAPE_CIRCLE
from pcbnew import wxPoint
from functools import reduce

class BGAInfo:
    spacing=0.0
    rows=0
    columns=0
    center=wxPoint(0,0)
    leftTop=wxPoint(0,0)
    rightBottom=wxPoint(0,0)
    degrees=0

def detectSpacing(pads):
    minDist = 10000000000000

    for idx in range(len(pads)):
        firstPos=pads[idx].GetPosition()
        rpads=pads[idx:]

        for pad in rpads:
            padPos=pad.GetPosition()

            if firstPos.x != padPos.x :
                x=abs(firstPos.x - padPos.x)
                y=abs(firstPos.y - padPos.y)

                dist=math.sqrt(x*x+y*y)
                minDist = min(minDist, dist)

    return minDist

def IsBGA(pads):
    for pad in pads:
        if pad.GetShape() != PAD_SHAPE_CIRCLE:
            return False
    
    return True

def ParseBGAInfo(ft):
    info = BGAInfo()
    pads=ft.Pads()

    minx = reduce(lambda x, y: min(x, y), map(lambda x: x.GetPosition().x, pads))
    maxx = reduce(lambda x, y: max(x, y), map(lambda x: x.GetPosition().x, pads))
    miny = reduce(lambda x, y: min(x, y), map(lambda x: x.GetPosition().y, pads))
    maxy = reduce(lambda x, y: max(x, y), map(lambda x: x.GetPosition().y, pads))


    info.spacing=detectSpacing(pads)

    info.leftTop = wxPoint(minx, miny)
    info.rightBottom=wxPoint(maxx,maxy)
    info.center = wxPoint(maxx* 0.5 + minx* 0.5, maxy * 0.5 + miny* 0.5)
    info.degrees=ft.GetOrientationDegrees()

    info.rows=int(1+round((maxy-miny)/float(info.spacing)))
    info.columns=int(1+round((maxx-minx)/float(info.spacing)))

    return info