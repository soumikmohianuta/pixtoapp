# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 12:43:56 2017

@author: soumi
"""
#from RectUtils.RectUtil import *
from RectUtils.Rect import Rect
from Utils import Constants
import RectUtils.RectUtil as RectUtil
from RectUtils import RectView



class OCRTextWrapper:
    
    def __init__ (self,another=None) :
        self.x = 0
        self.y = 0 
        self.width = 0 
        self.height = 0
#        self.bottom = 0 
#        self.right = 0
        self.text = ""
        self.fontName = ""
        self.bold = False
        self.italic = False
        self.underlined = False
        self.monospace = False
        self.serif = False
        self.smallcaps = False
        self.fontSize = -1
        self.fontId = 0 
        self.confidence = 0.0 
        self.words = []
        self.blocks = []
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.boundRectView = RectView.RectView(self.rect, None)


        if another!=None :
            self.text = another.text
            self.confidence = another.confidence
            self.fontId = another.fontId
            self.fontName = another.fontName
            self.fontSize = another.fontSize
            self.y = another.y
            self.x = another.x
            self.width = another.width
#            self.bottom = another.bottom
#            self.right = another.right         
            self.height = another.height
            self.italic = another.italic
            self.bold = another.bold
            self.underlined = another.underlined
            self.monospace = another.monospace
            self.serif = another.serif
            self.smallcaps = another.smallcaps
            self.words = []
            self.blocks = []
            self.rect = Rect(self.x, self.y, self.width, self.height)
            self.boundRectView = RectView.RectView(another.rect, None)
    
    def __hash__(self):
        return hash(self.rect)

    def __eq__(self, other):
        
        if other is None:
            return self.rect.area() == 0
        elif type(other) != type(self):
                return False
        else:
            return (self.rect == other.rect and self.text == other.text)

    def __ne__(self, other):
        return not(self.__eq__(other))

    
    def getTextAttributes(self,tesseractOCR, height):
        properties = []
        wrapper = self
        
        #TODO
        properties.append((Constants.ATTRIBUTE_TEXT_SIZE, str(tesseractOCR.getPreferenceFontSize(wrapper, height))+ Constants.UNIT_DIP))
#        properties.append((Constants.ATTRIBUTE_TEXT_SIZE, str(self.fontSize)+ Constants.UNIT_DIP))

        buffer = "normal"
        if self.bold :
            buffer += "|bold"
        
        if (self.italic) :
            buffer += "|italic"
        
        properties.append((Constants.ATTRIBUTE_TEXT_STYLE, buffer))
 
        buffer = ""
        if self.serif :
            buffer += "serif"
        elif self.monospace :
            buffer += "monospace"
        else :
            buffer += "normal"
        
        properties.append((Constants.ATTRIBUTE_TYPEFACE, buffer))
        return properties
    
    def getWidth(self):
        return self.width
        
    def isSameTextInfoAndSameLine(self, other):
        if other == None:
            return False
        
        if self.fontSize != other.fontSize:
            return False
        
        if self.fontName == None:
            if other.fontName != None:
                return False
        elif not self.fontName == other.fontName :
            return False


        # same y location
        # overlap y location
        # once contain other
#        if (!(bottom == o.bottom && top == o.top || o.bottom <= bottom
#				&& o.top <= top || bottom <= o.bottom && top <= o.top
#				|| o.bottom <= bottom && top <= o.top || bottom <= o.bottom
#				&& o.top <= top)) {
#			return false;
#		}
        
        if (not(self.height == other.height and self.top == other.top or other.bottom <= self.bottom
                and other.top <= self.top or self.bottom <= other.bottom and self.top <= other.top
                or other.bottom <= self.bottom and self.top <= other.top or self.bottom <= other.bottom
                and other.top <= self.top)):
            return False
        
        spaceBetweenWord = int (Constants.SPACE_BETWEEN_WORD_RATIO * self.fontSize)

        #not to far from each other
        if (not(self.right + spaceBetweenWord > other.left and self.right < other.left or other.right+ spaceBetweenWord > self.left and other.right < self.left)):
            return False


        return True
    
    
    def toString(self):
        return self.text + "[" + self.rect + ", " + self.confidence + ", " + self.fontName + ", " + self.fontId + ", " + self.fontSize + ", " + self.serif + ", " + self.bold + ", " + len(self.text) + "]"

    def reCalculateBoundBaseOnWordList(self):
        if (len(self.words) == 0):
            return None
        
        firstWord = self.words[0]
        unionRect = firstWord.rect
        for i in range(1,len(self.words)):
            word = self.words[i]
            unionRect = RectUtil.union(unionRect, word.rect)
        self.x =  unionRect.x
        self.y =  unionRect.y
        self.width =  unionRect.width
        self.height =  unionRect.height
        return unionRect
    
    def bound(self):
        return self.rect


    def setBound(self,rect):
        self.left = rect.x
        self.top = rect.y
        self.width = rect.width
        self.height = rect.height
        

        
    
    
