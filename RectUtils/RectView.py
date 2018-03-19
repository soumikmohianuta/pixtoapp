# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 17:20:53 2017

@author: soumi
"""

from RectUtils.Rect import Rect
import RectUtils.RectUtil as RecUtil
from Utils import FileMetadata
import RectUtils.RectViewUtil as RecViewUtil
from RectUtils.RectViewUtil import ListInfo, ListItemInfo, ListItemMetadata, ListItemType, ListMetadataRoot, IconInfo, ImageInfo
from ocr.TextInfo import TextInfo 



class RectView:

    def __init__(self,rect=Rect(),contour=None):
        self.rect = rect
        self.contour = contour
        self.mChildren = []
		#mTextWithLocations = new ArrayList<OCRTextWrapper>();
        self.mImageInfo = ImageInfo()
        self.mListInfo = ListInfo();
        self.mTextInfo = TextInfo()
        self.mType = RecViewUtil.VIEW_TYPE_DEFAULT
        self.x = rect.x
        self.y = rect.y
        self.width = rect.width
        self.height = rect.height
        self.mColor=  None
        self.mAlpha=0.0
        self.mTextChildren = []
        self.mTextWithLocations = []
        self.mImageInfo = ImageInfo()
        self.mListItemInfo = ListItemInfo()
        self.textColor =  0
    
    def area(self):
        return self.height*self.width
    
    def __hash__(self):
        return hash((self.rect, self.mType))

    def __eq__(self, other):
        
        if other is None:
            return self.rect.area() == 0
        elif type(other) != type(self):
                return False
        else:
            return (self.rect == other.rect) and (self.mType == other.mType)

    def __ne__(self, other):
        return not(self.__eq__(other))


    def includes(self,bound):
        return RectUtil.contains(self.rect, bound)

    def hasText(self):
         return len(self.mTextWithLocations) > 0


    def getOverlapRatio(self):
        overlapRatio = 0.0
        for rawView in self.mChildren :
            overlapRatio += rawView.area()
        
        return overlapRatio / self.rect.area()
    
    def addAllChild(self,child):
        self.mChildren.extend(child)
    
    def addChild(self,rawView):
        self.mChildren.append(rawView)
        
#    def getChildren(self):
#        return self.mChildren
#    
    def bound(self):
        return self.rect
#
#    def getTextChildren(self):
#        return self.mTextChildren


    def toString(self):
        textInfo = "Info: "
        if self.mType == self.VIEW_TYPE_TEXT:
            textInfo += "TEXT: " + self.mTextInfo.textWrapper.getText();
            
        elif self.mType ==  self.VIEW_TYPE_IMAGE:
            textInfo += "IMAGE: " + self.mImageInfo.drawableId + ", drawable_id: " + self.mImageInfo.drawableId;
			
        else:
            textInfo += "RECT: " + self.mTextWithLocations;
			
        return "Bound: " + self.bound() + ", Text Children: " + self.mTextChildren + ", " + self.textInfo

    def hasTextRecusive(self):
        if self.hasText():
            return True
        
        hasText = False
        
        for rectView in self.mChildren:
            hasText = rectView.hasTextRecusive()
            if (hasText):
                    return True
        return hasText



    


