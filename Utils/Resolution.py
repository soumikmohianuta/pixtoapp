# -*- coding: utf-8 -*-
"""
Created on Thu Mar 15 17:51:28 2018

@author: soumi
"""

class Resolution:
# different type of android resolutions
    LDPI = 120
    MDPI = 160
    HDPI = 240
    XHDPI = 320
    XXHDPI = 480
    XXXHDPI = 640


    def __init__(self,forDeviceDensity):
        self.mForDeviceDensity = forDeviceDensity
        self.mprofileMap = {}
        
#find pix value from dp value
    def getPx(self, dp, value):
        px = dp * (value / self.mForDeviceDensity)
        return px
        
    