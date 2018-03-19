# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 00:38:55 2017

@author: soumi
"""

from random import *
from RectUtils.Rect import Rect
import copy
#import Utils.ImageUtil as ImageUtil
      
MAX_AREA_SCAN = 1000

class CColor:
    White= (255,255,255)         
    Black = (0,0,0)     
    Gray =    (190,190,190)         
    Navy = (0,0,128)     
    Blue = (0,0,255)     
    Sky_Blue = (135,206,250)         
    Cyan = (0,255,255)     
    Dark_Green = (0,100,0)         
    Green_Yellow = (173,255,47) 
    Yellow_Green = (154,205,50)
    Khaki = (240,230,140)         
    Yellow = (255,255,0)         
    Gold = (255,215,0)         
    Brown = (165,42,42)     
    Orange = (255,165,0)
    Red = (255,0,0)     
    Pink = (255,192,203)     
    Violet = (238,130,238)  
    Magenta = (255,0,255)   
    Cyan = (0,255,255)  
    Light_Gray = (211,211,211)
    Dark_gray = (169,169,169)
    Green = (0,255,0)





def pixelWithinChildren(x,y , rectView):
    for child in rectView.mChildren:
        if x- child.x>=0 and x- child.x <= child.width and  y- child.y>=0 and y- child.y <= child.height:
            return False
        else:
            return True
        
def isAContainer(rect, image) :
    x = int(rect.x)
    y = int(rect.y)
    height = int(rect.height)
    width = int(rect.width)
    area = height * width
    endX = int(x + width)
    endY = int(y + height)
    if( len(image.shape) < 3):
        return -1
    
    
    channel = (image.shape)[2]
    imgHeight = (image.shape)[0]
    imgWidht = (image.shape)[1]
#    if (channel != 3 and channel != 4):
#        return -1
    if(endX >= imgWidht):
        endX = imgWidht -1
    if(endY >= imgHeight):
        endY = imgHeight -1
            
    startIndex = channel - 3
    a = 255

    elementColor = {}
    skipPixel = int((area / MAX_AREA_SCAN)**(0.5))
    if (skipPixel == 0) :
        skipPixel = 1
    cnt = 0 

    maxColor = toInt(0, 0, 0, 0) 
    totalPixelCount = 0

    for i in range(x,endX,skipPixel):
        for j in range(y,endY,skipPixel):
            if(pixelWithinChildren(i,j,rect)):
                totalPixelCount = totalPixelCount +1
#            temp = image[j] [i] [startIndex]
#            print("Coming here Atleaset")
                b = image[j] [i] [startIndex]
                g = image[j] [i] [startIndex + 1]
                r = image[j] [i] [startIndex+ 2]
                currentColor = toInt(a, r, g, b)
                if currentColor in elementColor:
                    elementColor[currentColor] = elementColor[currentColor] + 1
                else:
                    elementColor[currentColor] = 1
                if elementColor[currentColor] >= cnt :
                    cnt, maxColor = elementColor[currentColor], currentColor
    
    
    if(cnt/totalPixelCount >0.7):
        rect.mColor = maxColor
        return True
    else: 
        return False
#
#    return maxColor

def findDominateColor(rect, image) :
    x = int(rect.x)
    y = int(rect.y)
    height = int(rect.height)
    width = int(rect.width)
    area = height * width
    endX = int(x + width)
    endY = int(y + height)
    if( len(image.shape) < 3):
        return -1
    
    
    channel = (image.shape)[2]
    imgHeight = (image.shape)[0]
    imgWidht = (image.shape)[1]
#    if (channel != 3 and channel != 4):
#        return -1
    if(endX >= imgWidht):
        endX = imgWidht -1
    if(endY >= imgHeight):
        endY = imgHeight -1
            
    startIndex = channel - 3
    a = 255

    elementColor = {}
    skipPixel = int((area / MAX_AREA_SCAN)**(0.5))
    if (skipPixel == 0) :
        skipPixel = 1
    cnt = 0 

    maxColor = toInt(0, 0, 0, 0) 
#    print(image.shape)

    for i in range(x,endX,skipPixel):
        for j in range(y,endY,skipPixel):
#            temp = image[j] [i] [startIndex]
#            print("Coming here Atleaset")
            b = image[j] [i] [startIndex]
            g = image[j] [i] [startIndex + 1]
            r = image[j] [i] [startIndex+ 2]
            currentColor = toInt(a, r, g, b)
            if currentColor in elementColor:
                elementColor[currentColor] = elementColor[currentColor] + 1
            else:
                elementColor[currentColor] = 1
            if elementColor[currentColor] >= cnt :
                cnt, maxColor = elementColor[currentColor], currentColor
    

    return maxColor

def	 getImageFromRect(original, rect) :
    newImage = copy.deepcopy(original[int(rect.y):int(rect.y+rect.height),int(rect.x):int(rect.x+rect.width)])
    return newImage

def findDominateColorForTextView(rect, image) :

    elementColor = {}
    endX,endY = rect.rect.br()
    x,y = rect.rect.tl()
    img = getImageFromRect(image,rect.rect)
    if( len(img.shape) < 3):
        return -1
    imgHeight = (img.shape)[0]
    imgWidht = (img.shape)[1]

    channel = (image.shape)[2]
    startIndex = channel - 3
    a = 255
#    print(rect.mTextInfo.textWrapper.text)
    for i in range(0,imgWidht-1):
        for j in range(0,imgHeight-1):
#            temp = image[j] [i] [startIndex]
#            print("Coming here Atleaset")
            b = img[j] [i] [startIndex]
            g = img[j] [i] [startIndex + 1]
            r = img[j] [i] [startIndex+ 2]
            currentColor = (a, r, g, b)
            if currentColor in elementColor:
                elementColor[currentColor] = elementColor[currentColor] + 1
            else:
                elementColor[currentColor] = 1
#            if elementColor[currentColor] >= cnt :
#                cnt, maxColor = elementColor[currentColor], currentColor
    sorted_Color =sorted(elementColor, key=elementColor.get,reverse=True)
#    print(sorted_Color)
    backGroundColor = sorted_Color[0]
    index =1
    textColor = sorted_Color[index]
#    print(rgbDiff(backGroundColor, textColor))
    while(rgbDiff(backGroundColor, textColor)<100 and index < len(sorted_Color)):
        index = index +1
        textColor = sorted_Color[index]
        
    
    return (alphaColortoInt(backGroundColor),alphaColortoInt(textColor))
        
def rgbDiff(scaColor1, scaColor2):
    return abs(int(scaColor1[1])-int(scaColor2[1])) + abs(int(scaColor1[2])-int(scaColor2[2])) + abs(int(scaColor1[3])-int(scaColor2[3])) 

def toInt(  a ,   r,   g,   b) :
    return (a & 255) << 24 | (r & 255) << 16 | (g & 255) << 8 | (b & 255) << 0

def alphaColortoInt(cColor):
    return (cColor[0] & 255) << 24 | (cColor[1] & 255) << 16 | (cColor[1] & 255) << 8 | (cColor[2] & 255) << 0

def cColortoInt(cColor):
    a = 255
    return (a & 255) << 24 |(cColor[0] & 255) << 16 | (cColor[1] & 255) << 8 | (cColor[2] & 255) << 0

def getScalar(color):
    r = color and 255
    g = color >> 8 and 255
    b = color >> 16 and 255
    return (r, g, b)
    
    
def randomColor() :
    return (randint(0,255 ), randint(0,255 ), randint(0,255 ),randint(0,255 ))
    
def randomColorInt():
    return toInt(randomColor()[0],randomColor()[1],randomColor()[2],randomColor()[3])


class ColorWrapper:
    def __init__(self, color =cColortoInt(CColor.Black) , thicknessType=1):
            self.color = color
            self.thicknessType = thicknessType 
