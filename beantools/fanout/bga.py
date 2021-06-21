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

def detectSpacing(pads):
    firstPad=pads[0]
    pads=pads[1:]

    minDist = 100000000000
    for pad in pads:
        if firstPad.GetPosition().x != pad.GetPosition().x:
            minDist = min(minDist, abs(firstPad.GetPosition().x - pad.GetPosition().x))
    return minDist

def IsBGA(pads):
    for pad in pads:
        if pad.GetShape() != PAD_SHAPE_CIRCLE:
            return False
    
    return True

def ParseBGAInfo(pads):
    info = BGAInfo()

    minx = reduce(lambda x, y: min(x, y), map(lambda x: x.GetPosition().x, pads))
    maxx = reduce(lambda x, y: max(x, y), map(lambda x: x.GetPosition().x, pads))
    miny = reduce(lambda x, y: min(x, y), map(lambda x: x.GetPosition().y, pads))
    maxy = reduce(lambda x, y: max(x, y), map(lambda x: x.GetPosition().y, pads))


    info.spacing=detectSpacing(pads)

    info.leftTop = wxPoint(minx, miny)
    info.rightBottom=wxPoint(maxx,maxy)
    info.center = wxPoint(maxx* 0.5 + minx* 0.5, maxy * 0.5 + miny* 0.5)

    info.rows=int(1+round((maxy-miny)/float(info.spacing)))
    info.columns=int(1+round((maxx-minx)/float(info.spacing)))

    return info