# -*- coding: utf-8 -*-

"""
Created on Fri Oct 13 15:37:19 2017

@author: soumi
"""

from Utils import TextUtils
class FileMetadata:
    IMAGE = 0
    TEXT = 1
    VIEW = 2
    def __init__(self,listViewData, fileMetadata_type, layoutId=None):
        self.fileMetadata_type = fileMetadata_type
        self.listViewData = listViewData
        self.layoutId = layoutId
    
    def getVariableName(self):
        return self.listViewData.getVariableName(self)
    
    def getIsLast(self):
        return self.listViewData.isLast(self)
        
    def getIsText(self):
        return self.fileMetadata_type == FileMetadata.TEXT
    
    def getLayoutId(self):
        if (TextUtils.isEmpty(self.layoutId)):
            return self.getVariableName()
        
        return self.layoutId
    
    def setLayoutId(self,layoutId):
        self.layoutId = layoutId
		