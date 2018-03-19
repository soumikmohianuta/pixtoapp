# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 11:18:04 2017

@author: soumi
"""

import Utils.Constants as Constants
import cv2
import numpy as np

class Canny:
    
    ratio =2;
    def __init(self):
        self.lowThreshold = 100
        self.highThreshold = 200
        
    # Dilate the edge
    def addDilate(self,imgData):
        dilationSize = 1 
        kernel = np.ones((2 * dilationSize + 1, 2 * dilationSize + 1), np.uint8)
        img_dilation = cv2.dilate(imgData, kernel, iterations=1)
        return img_dilation
    #find the threshold of the image
    def updateLowHeightThreshold(self, imgData):
        imgHist = cv2.equalizeHist(imgData)
        #mean = cv2.core.Core.mean(imgHist)
        mean = np.average(imgHist)
        self.lowThreshold = int(Constants.CANNY_KERRY_WONG_LOW_THRESHOLD_RATIO * mean * Constants.CANNY_RATIO_CONTROL_THRESHOLD)
        self.highThreshold = int(Constants.CANNY_KERRY_WONG_LOW_THRESHOLD_RATIO * self.ratio * mean * Constants.CANNY_RATIO_CONTROL_THRESHOLD)
    #find Edge using canny edge detection algorithm
    def findEdge(self,imgData):
        self.updateLowHeightThreshold(imgData)
        edgeImage = cv2.Canny(imgData,self.lowThreshold,self.highThreshold)
        return edgeImage
        
        

