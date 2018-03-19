# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 17:54:05 2018

@author: soumi
#Help to store Phone display property
"""

class Profile :
#Help to store Phone display property

    def __init__(self,  _type,  width,  height) :
        self.mType = _type
        self.mWidth = width
        self.mHeight = height
        self.mDpWidth = (width * 160) /self.mType
        #Haven't cosidered title bar. Rather consider title bar heigt
        self.mDpTitleBarHeight = 0
        self.mDpHeight = ((height * 160) /self.mType) - self.mDpTitleBarHeight