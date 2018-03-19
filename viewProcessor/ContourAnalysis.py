# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 16:29:44 2017

@author: soumi
"""
import numpy as np
from RectUtils.Rect import Rect
from RectUtils.RectView import RectView
import cv2


class ContourAnalysis:
    IDENTICAL_CONTOURS_THRESHOLD = 0.75;
	#bilateralFilter
	# Diameter of each pixel neighborhood that is used during filtering. If it
	# is non-positive, it is computed from sigmaSpace .
	#/
    d = 3
    
	 # Filter sigma in the color space. A larger value of the parameter means
	 # that farther colors within the pixel neighborhood (see sigmaSpace ) will
	 # be mixed together, resulting in larger areas of semi-equal color.

    sigmaColor = 50
    
#	 * Filter sigma in the coordinate space. A larger value of the parameter
#	 * means that farther pixels will influence each other as long as their
#	 * colors are close enough (see sigmaColor ). When d>0 , it specifies the
#	 * neighborhood size regardless of sigmaSpace . Otherwise, d is proportional
#	 * to sigmaSpace .
#	 */
    sigmaSpace = 50
    

    def findContours(self, imgData):
        imageBlurr= cv2.bilateralFilter(imgData,self.d,self.sigmaColor,self.sigmaSpace)
        imageAdpTh = cv2.adaptiveThreshold(imageBlurr,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,3,5)
        contours,hierarchy = cv2.findContours(imageAdpTh,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return {'contours':contours, 'hierarchy':hierarchy}
    
    def findContoursWithCanny(self,imgData):
        img, contours,hierarchy = cv2.findContours(imgData,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return {'contours':contours, 'hierarchy':hierarchy}
    
    def analyze(self, imgData, foundContours):
        imageWithContour = np.empty_like (imgData)
        imageWithContour[:] = imgData
        
        imageAfterClearProcessedView = np.empty_like (imgData)
        imageAfterClearProcessedView[:] = imgData
        height, width = imgData.shape
        rect = Rect(0,0,width, height)
        rootView = RectView(rect,None)
        children = [] 
        self.findExternalContours(imageAfterClearProcessedView, foundContours['contours'],foundContours['hierarchy'], 0, 0, None, children) 

        for rawView in children:
            rootView.addChild(rawView)
            
        contourInfo = ContourInfo()
        contourInfo.imageAfterClearProcessedView = imageAfterClearProcessedView
        contourInfo.rootView = rootView
        map_data = {}
        contourInfo.rects = self.creatRects(rootView, map_data)
        contourInfo.map_data = map_data
        return contourInfo
    
    def creatRects(self, rootView, map_data):
        rects= []
        self.creatRectsInternal(rootView, rects, map_data);
        return rects
    def creatRectsInternal(self, rootView, rects, map_data):
        bound = rootView.rect
        rects.append(bound)
        map_data[bound] = rootView
        
        children = rootView.mChildren
        for rectView in children:
            
            bound = rectView.rect
            rects.append(bound)
            map_data[bound]= rectView
            self.creatRectsInternal(rectView, rects, map_data)
            
    def findExternalContours(self, imageAfterClearProcessedView, contours, hierarchy, index, level, parent, sibling):
        i = index
        if (i < 0):
            return
        while (i >= 0):
            buff = hierarchy[0][i]
            contour = contours[i]
            i = buff[0] #// Get the next id contour
            j = buff[2] #			// child index
            children = []
            
            if (j > 0):
                while(j>=0):
                    internalContoursBuff = hierarchy[0][j]
                    self.findExternalContours(imageAfterClearProcessedView, contours, hierarchy, internalContoursBuff[2],level + 1, contour, children)
                    j = internalContoursBuff[0]
                    
            currentView = None
            (x1,y1,width,height)= cv2.boundingRect(contour)
            currentView = RectView(Rect(x1,y1,width,height))
       # currentView = self.processRectangle(imageAfterClearProcessedView, contour)
        #print(len(sibling))
            sibling.append(currentView)
        
            if (currentView != None):
                currentView.addAllChild(children)
        
            
            
    index = 0
    
    def processRectangle(self, imageAfterClearProcessedView,contour):
        return RectView()

	#private boolean isSimilar(final MatOfPoint parentContour,
	#		final MatOfPoint thisContour) {
	#	final double parentContourArea = Imgproc.contourArea(parentContour);
	#	final double thisContourArea = Imgproc.contourArea(thisContour);
	#	if (thisContourArea / parentContourArea < IDENTICAL_CONTOURS_THRESHOLD) {
	#		return true;
	#	}
	#	return false;
	#}

# Class to hold the contour informations
class ContourInfo:
    map_data = {}
    imageAfterClearProcessedViewArr= []
    imageAfterClearProcessedView = np.array(imageAfterClearProcessedViewArr)
    rootView = RectView()
    rects = [] 

