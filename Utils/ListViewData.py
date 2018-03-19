# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 19:08:45 2017

@author: soumi
"""
from Utils import FileMetadata

class ListViewData:
    listInfos = []
    listFieldMetatata = []
    def __init__(self,name, id, infoClassName, adapterClassName,layoutName):
        self.name = name
        self.listFieldMetatata_type = id
        self.infoClassName = infoClassName
        self.adapterClassName = adapterClassName
        self.setLayoutName(layoutName);
	
    def getName(self):
        return self.name
    
    def setName(self,name):
        self.name = name

    def getId(self):
        return self.id
    
    def setId(self,name):
        self.id = id
        
    def getInfoClassName(self):
        return self.infoClassName
    
    def setInfoClassName(self,infoClassName):
        self.infoClassName = infoClassName
        
    def getAdapterClassName(self):
        return self.adapterClassName
    
    def setAdapterClassName(self,adapterClassName):
        self.adapterClassName = adapterClassName

    def getListFieldMetatata(self):
        return self.listFieldMetatata
    
    def setListFieldMetatata(self,listFieldMetatata):
        self.listFieldMetatata = listFieldMetatata
        
    def getVariableName(self,fieldMetadata):
        indexOf = self.listFieldMetatata.index(fieldMetadata)
        count=0
        for i in range(indexOf):
            if (self.listFieldMetatata[i] != fieldMetadata and self.listFieldMetatata[i].listFieldMetatata_type == fieldMetadata.listFieldMetatata_type) :
                count +=1
        return self.getBaseName(fieldMetadata.type) + count
    
    def getBaseName(listFieldMetatata_type) :
       if(listFieldMetatata_type == FieldMetadata.IMAGE):
           return "image"
       if(listFieldMetatata_type == FieldMetadata.TEXT):
           return "image"
       else:
           return "view"
       

    def getListInfos(self):
        return self.listInfos
    
    def setListInfos(self,listInfos):
        self.listInfos = listInfos
        
    def isLast(self,fieldMetadata) :
        if (fieldMetadata == None or self.listFieldMetatata.index(fieldMetadata) == -1) :
            return False
        return self.listFieldMetatata.index(fieldMetadata) == len(self.listFieldMetatata) - 1

    def getLayoutName(self):
        return self.layoutName
    
    def setLayoutName(self,layoutName):
        self.layoutName = layoutName

