import math
import re
from pcbnew import PAD_SHAPE_CIRCLE
from pcbnew import wxPoint
from functools import reduce,cmp_to_key

class BGAInfo:
    spacing=0.0
    center=wxPoint(0,0)
    degrees=0
    skipEdges=[]

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

def cmpPinName(a,b):
    aLen=len(a)
    bLen=len(b)

    if aLen != bLen:
        return aLen-bLen
    
    return a>b

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
    info.center = wxPoint(maxx* 0.5 + minx* 0.5, maxy * 0.5 + miny* 0.5)
    info.degrees=ft.GetOrientationDegrees()

    # for pad in pads:
    #     print(f"name:{pad.GetPadName()}")

    padNames=map(lambda pad: pad.GetPadName() ,pads)
    
    pinNames=[]
    pinNumbs=[]

    for padName in padNames:
        pinName=re.match("[A-Z]+",padName).group()
        pinNumb=int(padName.replace(pinName,''))

        if not pinName in pinNames:
            pinNames.append(pinName)
        
        if not pinNumb in pinNumbs:
            pinNumbs.append(pinNumb)

    pinNames.sort(key=cmp_to_key(cmpPinName))
    pinNumbs.sort()

    info.skipEdges += pinNames[:2]+pinNames[-2:]
    info.skipEdges += pinNumbs[:2]+pinNumbs[-2:]

    return info