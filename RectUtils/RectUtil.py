# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 17:33:31 2017

@author: soumi
"""
import sys
from RectUtils.Rect import Rect
from RectUtils.RectView import *
#from ocr.OCRTextWrapper import *
from functools import cmp_to_key
import Utils.ColorUtil as ColorUtil
#from Pygame import Rect

ALIGNMENT_LEFT = 1
ALIGNMENT_TOP = 2
ALIGNMENT_RIGHT = 3
ALIGNMENT_BOTTOM = 4
ALIGNMENT_UNKNOWN = 5



def contains(t, r , thresHold = -1):
    
    if(thresHold==-1):
        rx = r.x
        ry = r.y
        rh = r.height
        rw = r.width
        tw = t.width
        th = t.height
        if (tw < 0 or th<0 or rw<0 or rh<0):
            # At least one of the dimensions is negative...
            return False
        # Note: if any dimension is zero, tests below must return false...
        tx = t.x
        ty = t.y
        if (rx < tx or ry < ty):
            return False
        
        tw += tx
        rw += rx
        if (rw <= rx):
            # X+W overflowed or W was zero, return false if...
            # either original w or W was zero or
            # x+w did not overflow or
            # the overflowed x+w is smaller than the overflowed X+W
            if (tw >= tx or rw > tw):
                return False
        else:
        # X+W did not overflow and W was not zero, return false if...
            # original w was zero or
            # x+w did not overflow and x+w is smaller than X+W
            if (tw >= tx and rw > tw):
                return False
        
        th += ty
        rh += ry
        if (rh <= ry):
            if (th >= ty or rh > th):
                return False
            
        else:
            if (th >= ty and rh > th):
                return False
            
        return True
  
    else:
        if (intersects(t, r)):
            intersection = interection(t, r)
            ratio= float( intersection.area()) / r.area()
            if(ratio >= thresHold):
                  return True            
        return False

def boxIsALetter(t, r, threshold=1 ):
        rx = r.x
        ry = r.y
        rh = r.height
        rw = r.width
        tw = t.width
        th = t.height
        if (tw < 0 or th<0 or rw<0 or rh<0):
            # At least one of the dimensions is negative...
            return False
        # Note: if any dimension is zero, tests below must return false...
        tx = t.x
        ty = t.y
        if (rx+threshold <= tx or ry+threshold <= ty):
            return False
        
        tw += tx
        rw += rx
        
        th += ty
        rh += ry
        if (tw+threshold >= rw and rh+threshold >= th):
            return False
            
        return True
  


def intersectsNotInclude(t, r):
    return intersects(t, r) and (not contains(t, r)) and (not contains(r, t))
    

def intersects(t, r):
    tw = t.width
    th = t.height
    rw = r.width
    rh = r.height
    if (rw <= 0 or rh <= 0 or tw <= 0 or th <= 0):
        return False

    tx = t.x
    ty = t.y
    rx = r.x
    ry = r.y
    rw += rx
    rh += ry
    tw += tx
    th += ty
    # overflow or intersect
    return (rw < rx or rw > tx) and (rh < ry or rh > ty) and (tw < tx or tw > rx) and (th < ty or th > ry)

def interection(t, r):
    tx1 = t.x
    ty1 = t.y
    rx1 = r.x
    ry1 = r.y
    tx2 = tx1
    tx2 += t.width
    ty2 = ty1
    ty2 += t.height
    rx2 = rx1
    rx2 += r.width
    ry2 = ry1
    ry2 += r.height
    if (tx1 < rx1):
        tx1 = rx1
        
    if (ty1 < ry1):
        ty1 = ry1
        
    if (tx2 > rx2):
        tx2 = rx2
        
    if (ty2 > ry2):
        ty2 = ry2
        
    tx2 -= tx1
    ty2 -= ty1
    # tx2,ty2 will never overflow (they will never be
    # larger than the smallest of the two source w,h)
    # they might underflow, though...
        
    if (tx2 < - sys.maxsize ):
        tx2 = - sys.maxsize 
        
    if (ty2 < - sys.maxsize ):
        ty2 = - sys.maxsize 
        
    return Rect(tx1, ty1, tx2, ty2)

def equal(t, r):
    return t.width == r.width and t.height == r.height


def equal_wthres(t, r, threadholdWidthInPixel, threadholdHeightInPixel= 0):
    if threadholdHeightInPixel == 0:
        threadholdHeightInPixel = threadholdWidthInPixel
    return abs(t.width - r.width) <= threadholdWidthInPixel and abs(t.height - r.height) <= threadholdHeightInPixel

def equalRatio(t, r, threadholdWidthRatio,  threadholdHeightRatio):
    return min(t.width, r.width) / max(t.width, r.width) <= threadholdWidthRatio and min(t.height, r.height) / max(t.height, r.height) <= threadholdHeightRatio


def equalSize(t, r, threadholdWidthInPixel, threadholdHeightInPixel=-1):
    if (threadholdHeightInPixel==-1):
        return abs(t.width - r.width) <= threadholdWidthInPixel and abs(t.height - r.height) <= threadholdWidthInPixel
    else:
        return abs(t.width - r.width) <= threadholdWidthInPixel and abs(t.height - r.height) <= threadholdHeightInPixel        

def same(t, r, theshold = 0 ):
    if (theshold==0):
        return t.x == r.x and t.y == r.y and t.width == r.width and t.height == r.height
    else:
#        areaT = float(t.area())
#        areaR = float(r.area())
#        if (contains(t, r)):
#            return areaR / areaT > theshold
#        if (contains(r, t)):
#            return areaT / areaR > theshold
        if(contains(t,r,theshold) or contains(r,t,theshold)):
            return True
        return False


def union(t, r):
    tx2 = t.width
    ty2 = t.height
    if ((tx2 | ty2) < 0):
            # This Rect has negative dimensions...
            # If r has non-negative dimensions then it is the answer.
            # If r is non-existant (has a negative dimension), then both
            # are non-existant and we can return any non-existant Rect
            # as an answer. Thus, returning r meets that criterion.
            # Either way, r is our answer.
        return Rect(r.x, r.y, r.width, r.height)
    
    rx2 = r.width
    ry2 = r.height
    if (rx2 <0 or ry2<0):
        return Rect(t.x, t.y, t.width, t.height)
        
    tx1 = t.x
    ty1 = t.y
    tx2 += tx1
    ty2 += ty1
    rx1 = r.x
    ry1 = r.y
    rx2 += rx1
    ry2 += ry1
    if (tx1 > rx1):
        tx1 = rx1
        
    if (ty1 > ry1):
            ty1 = ry1
        
    if (tx2 < rx2):
        tx2 = rx2
    
    if (ty2 < ry2):
        ty2 = ry2
        
    tx2 -= tx1
    ty2 -= ty1
        # tx2,ty2 will never underflow since both original Rects
        # were already proven to be non-empty
        # they might overflow, though...
    if (tx2 > sys.maxsize ):
        tx2 = sys.maxsize 
        
    if (ty2 > sys.maxsize ):
        ty2 = sys.maxsize 
        
    return Rect(tx1, ty1, tx2, ty2)

     # Translates this <code>Rect</code> the indicated distance, to the right
     # along the X coordinate axis, and downward along the Y coordinate axis.
     # 
     # @param dx
     #            the distance to move this <code>Rect</code> along the X axis
     # @param dy
     #            the distance to move this <code>Rect</code> along the Y axis
     

def translate(t,dx,dy):
    oldv=t.x
    newv = oldv+dx
    if (dx < 0):
        if(newv>oldv):
            # negative overflow
            # Only adjust width if it was valid (>= 0).
            if (t.width >= 0):
                # The right edge is now conceptually at newv+width, but we may move newv to prevent overflow. But we want the right edge to
                # remain at its new location in spite of the clipping. Think of the following adjustment
                # conceptually the same as:
                # width += newv; newv = MIN_VALUE; width -= newv;
                t.width += newv  + sys.maxsize 
                    #width may go negative if the right edge went past MIN_VALUE, but it cannot overflow since it cannot
                    # have moved more than MIN_VALUE and any non-negative
                    # number + MIN_VALUE does not overflow.
            newv = - sys.maxsize 
    else:
            # moving rightward (or staying still)
        if (newv < oldv):# positive overflow
                if (t.width >= 0):
                    t.width += newv - sys.maxsize 
                    # Conceptually the same as:
                    # width += newv; newv = MAX_VALUE; width -= newv;
                    #large widths and large displacements
                    # we may overflow so we need to check it.
                    if(t.width<0):
                        t.width = sys.maxsize 
                    
                    newv = sys.maxsize 
    t.x = newv
    oldv = t.y
    newv = oldv + dy
    if (dy < 0):
        # moving upward
        if (newv > oldv):
            # negative overflow
            if (t.height >= 0):
                t.height += newv + sys.maxsize 
                # See above comment about no overflow in this case
            newv = - sys.maxsize ;
            
    else:
        # moving downward (or staying still)
        if (newv < oldv):
            # positive overflow
            if (t.height >= 0):
                t.height += newv - sys.maxsize 
                if (t.height < 0) :
                    t.height = sys.maxsize 
                newv = sys.maxsize 
            
    t.y = newv;



    # Adds a point, specified by the integer arguments {@code newx,newy} to the
    # bounds of this {@code Rect}.
    # <p>
    # If this {@code Rect} has any dimension less than zero, the rules for <a
    # href=#NonExistant>non-existant</a> Rects apply. In that case, the new
    # bounds of this {@code Rect} will have a location equal to the specified
    # coordinates and width and height equal to zero.
    # <p>
    # After adding a point, a call to <code>contains</code> with the added
    # poas an argument does not necessarily return <code>true</code>. The
    # <code>contains</code> method does not return <code>true</code> for points
    # on the right or bottom edges of a <code>Rect</code>. Therefore, if the
    # added pofalls on the right or bottom edge of the enlarged
    # <code>Rect</code>, <code>contains</code> returns <code>false</code> for
    # that point. If the specified pomust be contained within the new
    # {@code Rect}, a 1x1 Rect should be added instead:
    # 
    # <pre>
    # r.add(newx, newy, 1, 1);
    # </pre>
    # 
    # @param newx
    #            the X coordinate of the new point
    # @param newy
    #            the Y coordinate of the new point
    #/
def add( t, newx, newy):
    if(t.width<0 or t.height < 0):
        t.x = newx
        t.y = newy
        t.width = t.height = 0;
        return
        
    x1 = t.x;
    y1 = t.y;
    x2 = t.width;
    y2 = t.height;
    x2 += x1;
    y2 += y1;
    if (x1 > newx):
        x1 = newx;
        
    if (y1 > newy):
        y1 = newy;
        
    if (x2 < newx):
        x2 = newx
        
    if (y2 < newy):
            y2 = newy
    
    x2 -= x1;
    y2 -= y1;
    if (x2 > sys.maxsize ):
        x2 = sys.maxsize 
    
    if (y2 > sys.maxsize ):
        y2 = sys.maxsize 
    
    t.reshape(x1, y1, x2,y2)

    ##
     # Adds a <code>Rect</code> to this <code>Rect</code>. The resulting
     # <code>Rect</code> is the union of the two Rects.
     # <p>
     # If either {@code Rect} has any dimension less than 0, the result will
     # have the dimensions of the other {@code Rect}. If both {@code Rect}s have
     # at least one dimension less than 0, the result will have at least one
     # dimension less than 0.
     # <p>
     # If either {@code Rect} has one or both dimensions equal to 0, the result
     # a those axes with 0 dimensions will be equivalent to the results
     # obtained by adding the corresponding origin coordinate to the result Rect
     # a that axis, similar to the operation of the {@link #add(Point)}
     # method, but contribute no further dimension beyond that.
     # <p>
     # If the resulting {@code Rect} would have a dimension too large to be
     # expressed as an {@code int}, the result will have a dimension of
     # {@code sys.maxsize } a that dimension.
     # 
     # @param r
     #            the specified <code>Rect</code>
     #/
def add( t, r):
    tx2 = t.width
    ty2 = t.height
    if (tx2<0 or ty2 < 0):
            t.reshape(r.x, r.y, r.width, r.height);
    rx2 = r.width;
    ry2 = r.height;
    if (rx2<0 or  ry2< 0):
        return
    tx1 = t.x
    ty1 = t.y
    tx2 += tx1
    ty2 += ty1
    rx1 = r.x
    ry1 = r.y
    rx2 += rx1
    ry2 += ry1
    if (tx1 > rx1):
        tx1 = rx1
        
    if (ty1 > ry1):
        ty1 = ry1
        
    if (tx2 < rx2):
        tx2 = rx2
        
    if (ty2 < ry2):
        ty2 = ry2
    
    tx2 -= tx1;
    ty2 -= ty1;
    #tx2,ty2 will never underflow since both original
    #Rects were non-empty
    #they might overflow, though...
    if (tx2 > sys.maxsize ):
        tx2 = sys.maxsize 
    
    if (ty2 > sys.maxsize ):
        ty2 = sys.maxsize 

    t.reshape(tx1, ty1, tx2, ty2)
    

def reshape( t, x, y, width, height):
    t.x = x
    t.y = y
    t.width = width
    t.height = height

def findBoundRectangle(iRects):
    rect = Rect()
    if (len(iRects) == 0):
            return rect
    top = sys.maxsize 
    left = sys.maxsize 
    right = - sys.maxsize 
    bottom = - sys.maxsize 
    for e in iRects:
        left = min(left, e.x)
        top = min(top, e.y)
        right = max(right, e.x + e.width)
        bottom = max(bottom, e.y + e.height)
    
    rect.x = left
    rect.y = top
    rect.width = right - left
    rect.height = bottom - top
    return rect


def findBoundOfRects(iRects):
    rect = Rect();
    if (len(iRects) == 0):
            return rect
    top = sys.maxsize 
    left = sys.maxsize 
    right = - sys.maxsize 
    bottom = - sys.maxsize 
    for e in iRects:
        left = min(left, e.x);
        top = min(top, e.y);
        right = max(right, e.x + e.width);
        bottom = max(bottom, e.y + e.height);
    
    rect.x = left;
    rect.y = top;
    rect.width = right - left;
    rect.height = bottom - top;
    return rect;

def findChildRect(containerRect, rects):
    rs = []
    for e in rects:
        if(contains(containerRect,e)):
            rs.append(e)
    
    return rs 

    
def countChildRect(containerRect, rects):
    childCount = 0
    for e in rects:
        if(contains(containerRect,e)):
            childCount+=1
    
    return childCount

def findIntersectRect(containerRect, rects):
    rs = []
    for e in rects:
        if(intersects(containerRect,e)):
            rs.append(e)
    
    return rs 

    
def countIntersectRect(containerRect, rects):
    childCount = 0
    for e in rects:
        if(intersects(containerRect,e)):
            childCount+=1
    
    return childCount

def findIntersectNotIncludeRect(containerRect, rects):
    rs = []
    for e in rects:
        if(intersectsNotInclude(containerRect,e)):
            rs.append(e)
    
    return rs 

    
def countIntersectNotIncludeRect(containerRect, rects):
    childCount = 0
    for e in rects:
        if(intersectsNotInclude(containerRect,e)):
            childCount+=1
    
    return childCount


    
def overlapNotInclude(t, r, threadHold):
    if (intersectsNotInclude(t, r)):
        intersection = interection(t, r)
        ratioR = float(intersection.area()) / r.area()
        ratioT = float(intersection.area()) / t.area()
        if (ratioR >= threadHold and ratioT >= threadHold):
            return True        
    return False

def overlap(t, r, threadHold):
    if (intersects(t, r)):
        intersection = interection(t, r);
        ratioR = float(intersection.area()) / r.area()
        ratioT = float(intersection.area()) / t.area()
        if (ratioR >= threadHold and ratioT >= threadHold):
            return True
    return False



def cmpLeftRightTopBottom(r1, r2):
    xDiff = r1.x - r2.x
    if (xDiff == 0):
        return r1.y > r2.y
    else:
        return r1.x > r2.x
                

def sortLeftRightTopBottom(viewBounds) :
    viewBounds.sort(key=cmp_to_key(cmpLeftRightTopBottom))



def cmpTopBottomLeftRight(r1, r2):
    yDiff = r1.y - r2.y
    if (yDiff == 0):
        return r1.x - r2.x
    else:
        return r1.y - r2.y
                

def sortTopBottomLeftRight(viewBounds) :
    viewBounds.sort(key=cmp_to_key(cmpTopBottomLeftRight))

def cmpTopBottom(r1, r2):
    return r1.y - r2.y
                
def cmpArea(r1,r2):
    return  r1.area() < r2.area()

def sortTopBottom(viewBounds) :
    viewBounds.sort(key=cmp_to_key(cmpTopBottom))


def sortByArea(viewBounds) :
    viewBounds.sort(key=cmp_to_key(cmpArea))
    
def left(t, r):
    return t.x < r.x

def right(t, r):
    return r.x < t.x

def above(t, r):
    return t.y < r.y

def below(t, r):
    return r.y < t.y

def alignLeft(t, r, delta):
    return abs(t.x - r.x) <= delta 

def alignRight(t, r, delta):
    return abs(t.x - r.x) <= delta

def alignLeftContainer(t, r, delta):
    return abs(t.x - r.x) <= delta and abs(t.height - r.height) <= delta

def alignRightContainer(t, r, delta):
    return abs(t.x - r.x) <= delta and abs(t.height - r.height) <= delta



def alignTop(t, r, delta):
    return abs(t.y - r.y) <= delta

def alignBottom(t, r, delta):
    return abs(t.y - r.y) <= delta

def alignTopContainer(t, r, delta):
    return abs(t.y - r.y) <= delta and abs(t.width - r.width) <= delta

def alignBottomContainer(t, r, delta):
    return abs(t.y - r.y) <= delta and abs(t.width - r.width) <= delta

def closerLeft(t, r):
    return t.x >= r.x

def closerTop(t, r):
    return t.y >= r.y

def closerRight(t, r):
    return t.x >= r.x

def closerBottom(t, r):
    return t.y >= r.y
    
def getTopBottomComparator(r1,r2):
    return  r1.y > r2.y
    
def getLeftRightComparator(r1,r2):
    return  r1.x > r2.x




def containAll(rect, rects):
    if (len(rects) == 0):
        return False
    containAll = True;
    for r in rects:
        if (not contains(rect, r)):
            return False
    return containAll
    

def contain( rect, rects):
    children = []
    if (len(rects) == 0):
        return children

    for r in rects:
        if (r != rect and contains(rect, r)):
                children.append(r)

    return children

def retainAll(rect, rects):
    retainList = []
    if (len(rects) == 0):
        return retainList
    
    for r in rects:
        if (contains(rect, r)):
            retainList.append(r)
    return retainList
    
def alignTest(rects, delta, function):

    if (len(rects) == 0 or len(rects) == 1):
        return False
        
    alignVerification = True;
    for i in range(len(rects)-1):
        if (not function(rects[i],rects[i+1],delta)):
                return False;
    return alignVerification    

def getAlignmentType(rects, delta):

    if (alignTest(rects, delta, alignLeft)):
        return ALIGNMENT_LEFT
    elif (alignTest(rects, delta, alignRight)):
        return ALIGNMENT_RIGHT 
    elif (alignTest(rects, delta, alignTop)):
        return ALIGNMENT_TOP
    elif (alignTest(rects, delta, alignBottom)):
        return ALIGNMENT_BOTTOM
    
    return ALIGNMENT_UNKNOWN

def getLeafNodes(view):
    rectViews = []
    getLeafNodesInternal(None, view, rectViews)
    return rectViews

def getLeafNodesInternal(parent, view, rectViews):
        if (view != None):
            if (parent != None and len(view.mChildren) == 0):
                rectViews.append((parent, view))
            else:
                for child in view.mChildren:
                        getLeafNodesInternal(view, child, rectViews)

class CompareInfo:
    rectFirst = Rect()
    rectSecond = Rect()
    delta=0.0
    def __init__(self,rectFirst, rectSecond, delta):
        self.rectFirst = rectFirst
        self.rectSecond = rectSecond
        self.delta = delta

def verticalDistance(tb, rb):
    return abs(rb.y - tb.y)

def horizontalDistance( tb, rb):
    return abs(rb.x - tb.x)

def dimesionSmallerThan( t, r, maxRatio, minRatio=0):
        
    ratioWidth = float(t.width) / r.width
    ratioHeight = float(t.height) / r.height
    if (minRatio==0):
        return ratioWidth < maxRatio or ratioHeight < maxRatio
    else:
        maxDimRatio = max(ratioWidth, ratioHeight)
        minDimRatio = min(ratioWidth, ratioHeight)
        return maxDimRatio < maxRatio or minDimRatio < minRatio

def dimesionGreaterThan(t, r, ratio):
    ratioWidth = float (t.width) / r.width
    ratioHeight = float (t.height) / r.height
    return ratioWidth > ratio or ratioHeight > ratio

def dimensionEqual(t , r, threshold):

    ratioTRWidth = float (t.width) / r.width
    ratioTRHeight = float (t.height) / r.height
    ratioRTWidth = float (r.width) / t.width
    ratioRTHeight = float (r.height) / t.height
    
    return abs(ratioTRWidth - 1) < 1 - threshold and abs(ratioTRHeight - 1) < 1 - threshold and abs(ratioRTWidth - 1) < 1 - threshold and abs(ratioRTHeight - 1) < 1 - threshold

def noOverlap(rects):
    for i in range(len(rects)):
        for j in range(len(rects)):
            if (contains(rects[i], rects[j]) or contains(rects[j], rects[i])):
                return False               
    return True

def isOrderHorizontally(rects):
    if (len(rects) <= 1):
        return True
        newRects = rects
        newRects.sort(key=cmp_to_key(getLeftRightComparator))
        for i in len(newRects)-1:
            current = newRects[i]
            next = newRects[i+1]
            if (current.x + current.width >= next.x):
                return False
    return True

def isOrderVertically(rects):
    if (len(rects) <= 1):
        return True
        newRects = rects
        newRects.sort(key=cmp_to_key(getTopBottomComparator))
        for i in len(newRects)-1:
            current = newRects[i]
            next = newRects[i+1]
            if (current.y + current.height >= next.y):
                return False
    return True

def distanceTop(r, o):
    return (((r.x - o.x)**2) + ((r.y - o.y)**2))**(.05)

def expand1Px( rect):
    return Rect(rect.x - 1, rect.y - 1, rect.width + 2, rect.height + 2)
    
def onTheLeft(t,r):
    return t.x < r.x


def findTopLeft(parent, rects):
    if (len(rects) == 0):
        return None
    
    if (len(rects) == 1):
        return rects[0]
    
        distances = sys.float_info.max
        topLeft = None
        for i in rects:
            currentDis = distanceTop(i, parent)

            if (distances > currentDis):
                distances = currentDis
                topLeft = i;
        
        return topLeft
    

def findClosestSmallerTop(rect, others):
    if (len(others) == 0):
        return None
    
    closest = None
    for i in others:
        if (rect.x >= i.x):
            if (closest == None or closest.x <= i.x):
                closest = i
        
    return closest

def findClosestSmallerLeft(rect, others):
    if (len(others) == 0):
        return None
    
    closest = None
    for i in others:
        if (rect.x >= i.x):
            if (closest == None or closest.y <= i.y):
                    closest = i
        
    return closest


def toMapRect(rectView):
        mapRects = {}
        toMapRectsInternal(mapRects, rectView);
        return mapRects
    
    
def toMapRects(rectViews):
        mapRects = {}
        for item in rectViews:
            toMapRectsInternal(mapRects, item)

        return mapRects

def toMapRectsInternal( mapRects, rectView):
    color = getColorWrapperBaseOnType(rectView.mType)
    iRects = []
    if color not in mapRects:
        iRects = []
        mapRects[color]= iRects
    else:
        iRects = mapRects[color]

    iRects.append(rectView)

    for child in rectView.mChildren:
        toMapRectsInternal(mapRects, child)
            
def getColorWrapperBaseOnType(_type):
        color = ColorWrapper()
        if _type == RectView.VIEW_TYPE_TEXT:
            color.color = ColorUtil.cColortoInt(CColor.Red)
            
        elif _type == RectView.VIEW_TYPE_IMAGE:
            color.color = ColorUtil.cColortoInt(CColor.Green)
            
        elif _type == RectView.VIEW_TYPE_LIST_ITEM:
            color.color = ColorUtil.cColortoInt(CColor.Blue)
            color.thicknessType = 4
        elif _type == RectView.VIEW_TYPE_LIST:
            color.color = ColorUtil.cColortoInt(CColor.Orange)
            color.thicknessType = 0
        else:
            color.color = ColorUtil.cColortoInt(CColor.Black)
            color.thicknessType = 3;
            
        return color

def convertToParentCorrdinateContour(rectView, contour):
		for point in contour:
			point.x = point.x - rectView.x
			point.y = point.y - rectView.y
#		Point[] ap = new Point[listPoints.size()];
#		listPoints.toArray(ap);
#		contour = new MatOfPoint(ap);
		return contour
    
def convertToParentCorrdinate(rectView, childBound):
    rect= Rect()
    rect.x = childBound.x - rectView.x
    rect.y = childBound.y - rectView.y
    rect.height = childBound.height
    rect.width = childBound.width
    
#		Point[] ap = new Point[listPoints.size()];
#		listPoints.toArray(ap);
#		contour = new MatOfPoint(ap);
    return rect
