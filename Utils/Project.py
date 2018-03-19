# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 23:10:00 2017

@author: soumi
"""

from Utils import TextUtils


class Project:
    #private String mName;
   # private List<Layout> mLayouts;
   # private String mPath;

    def __init__(self,name):
        self.mName = TextUtils.removeInvalidProjectNameChars(name.lower())
        self.mPath = ""
   #     mLayouts = new ArrayList<Layout>();
    

#    public void addLayout(final Layout layout) {
#        mLayouts = new ArrayList<Layout>();
#        getLayouts().add(layout);
#    }

#    public List<Layout> getLayouts() {
#        return mLayouts;
#    }
#
#    def getName(self):
#        return self.mName
#    
#    def setName(self,name):
#        self.mName =name
#    
#    def getPath(self):
#        return self.mPath
#    
#    def setPath(self,path):
#        self.mPath =path
#

