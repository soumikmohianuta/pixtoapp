# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 21:14:05 2017

@author: soumi
"""
import numpy as np
from RectUtils.Rect import Rect
import cv2
import Utils.ColorUtil as ColorUtil
import copy
from functools import cmp_to_key
import RectUtils.RectUtil as RectUtil


def	 getImageFromRect(original, rect) :
    newImage = copy.deepcopy(original[int(rect.y):int(rect.y+rect.height),int(rect.x):int(rect.x+rect.width)])
    return newImage

def	  getImageFromContour(  original, contour) :
    rect = Rect(cv2.boundingRect(contour))
    return getImageFromRect(original, rect);

	
def fillRect(  image, rect, dominantColor) :
    r = dominantColor & 255
    g = dominantColor >> 8 & 255;
    b = dominantColor >> 16 & 255
    cv2.rectangle(image, rect.tl(), rect.br(), (r, g, b), -1)
	

def	  drawRect(  image,  rect, color, thickness=2) :
    a = np.right_shift(color, 24)  & 255
    r = (color >> 16) & 255
    g = (color >> 8) & 255
    b = color & 255
#    r = 0 
#    g = 0
#    b = 255
    cv2.rectangle(image, rect.tl(), rect.br(), (b, g, r),thickness)
    return image
	

def drawWindow(_id, image):
    width = 0 
    height = 0
    
    if len(image.shape) == 2 :
        height, width = image.shape
    else:
        height, width,channels = image.shape
    cv2.namedWindow(_id, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(_id, int(width/3), int(height/3))
    cv2.imshow(_id,image)


def logDraw(_id, image, contours,randomColor= False,clearImageContent=False) :
    if not randomColor:
        logDrawColor(_id, image,contours, clearImageContent, (0,0,255))
        return
    copyImage = copy.deepcopy(image)
    width = 0 
    height = 0
    
    if len(image.shape) == 2 :
        height, width = image.shape
    else:
        height, width,channels = image.shape
    
    if (clearImageContent) :
        fillRect(copyImage, Rect(0, 0, width, height),ColorUtil.toInt(255, 255, 255, 255))
    
    for contour in contours:
        matOfPoints = []
        matOfPoints.append(contour)		
        cv2.polylines(copyImage, matOfPoints, True, ColorUtil.randomColor())
    
    drawWindow(_id,copyImage)

#def logDrawRect(_id, image, contours, clearImageContent=False) :
#    copyImage = copy.deepcopy(image)
#    height, width ,channels = copyImage.shape
#    if (clearImageContent) :
#        fillRect(copyImage, Rect(0, 0, width, height),ColorUtil.toInt(255, 255, 255, 255))
#    
#    for contour in contours:
#        (x1,y1,width,height)= cv2.boundingRect(contour)
#        rect = Rect(x1,y1,width,height)
#        #a,r,g,b = ColorUtil.randomColor()
#        a,r,g,b = ColorUtil.randomColor()
#        drawRect(copyImage, rect, ColorUtil.toInt(a,r,g,b))
#    drawWindow(_id,copyImage)
#			
def cmpArea(r1, r2):
	return r1.area() < r2.area()
				


def logDrawColor(_id, image, contours,clearImageContent,color) :
    width = 0 
    height = 0
    
    if len(image.shape) == 2 :
        height, width = image.shape
    else:
        height, width, channels = image.shape
    
    if (clearImageContent) :
        fillRect(image, Rect(0, 0, width, height),ColorUtil.toInt(255, 255, 255, 255))
    
    
    cv2.polylines(image, contours, True, color, 2)	
    
    drawWindow(_id,image)
    
    
def logDrawRects(rects,color, _id, image, clearImageContent = False):
    copyImage = copy.deepcopy(image)
    width = 0 
    height = 0
    
    if len(image.shape) == 2 :
        height, width = image.shape
    else:
        height, width, channels = image.shape
	 
    if (clearImageContent):
        fillRect(copyImage, Rect(0, 0, width,height), ColorUtil.toInt(255, 255, 255, 255))
    
    for entry in rects:
#        for rect in colorRectMap[entry]:
            drawRect(copyImage, entry, color)
    drawWindow(_id, copyImage)

    
def logDrawMap(colorRectMap, _id, image, clearImageContent = False):
    copyImage = copy.deepcopy(image)
    width = 0 
    height = 0
    
    if len(image.shape) == 2 :
        height, width = image.shape
    else:
        height, width, channels = image.shape
	 
#    if (clearImageContent):
#        fillRect(copyImage, Rect(0, 0, width,height), ColorUtil.toInt(255, 255, 255, 255))
    
    for entry in colorRectMap:
#        for rect in colorRectMap[entry]:
            drawRect(copyImage, colorRectMap[entry].bound(), entry.color)
    drawWindow(_id, copyImage)
		
def logDrawViewColor (colorRectMap, _id, image, clearImageContent = False):
    copyImage = copy.deepcopy(image)
    width = 0 
    height = 0
    
    if len(image.shape) == 2 :
        height, width = image.shape
    else:
        height, width, channels = image.shape
	 
#    if (clearImageContent):
#        fillRect(copyImage, Rect(0, 0, width,height), ColorUtil.toInt(255, 255, 255, 255))
    
    for entry in colorRectMap:
#        for rect in colorRectMap[entry]:
        drawRect(copyImage, entry.rect, colorRectMap[entry])
    drawWindow(_id, copyImage)

#def olverlayColor( src, contour, color) :
#		# black out
#        mask = np.zeros(src.shape)
#        OfPos = []
#        OfPos.append(contour)
#        logDrawRect(mask, OfPos, -1, new Scalar(255),
#				Core.FILLED);
#
#		 srcWithOverlay = new (src.rows(), src.cols(), CvType.CV_8UC3);
#		srcWithOverlay.setTo(color);
#		src.copyTo(srcWithOverlay, mask);
#
#		Core.normalize(srcWithOverlay.clone(), srcWithOverlay, 0.0, 255.0,
#				Core.NORM_MINMAX, CvType.CV_8UC1);
#		return srcWithOverlay;
#	
#

def createTransparentBackground( src, contour) :
		# black out
        mask = np.zeros(src.shape, np.int8);
        alpha = np.zeros(src.shape, np.int8);
        OfPos = []
        OfPos.add(contour);
		# Fill inner contours with white and outer contours with black
        cv2.polylines(mask, OfPos, True , ColorUtil.getScalar(255),cv2.FILLED)
		# Make the outer contour transparent
        retval, alpha =   cv2.threshold(newMask,100,255,cv2.THRESH_BINARY)
#		Imgproc.threshold(mask, alpha, 100, 255, Imgproc.THRESH_BINARY);
        b,g,r = cv2.split(src)
        merge = cv2.merge((b,g,r,alpha))
        return merge
	
	

def removeChildrenAndCreateTransparentBackground( src, view) :
    contours = []
    children = view.mChildren
		# black out
    mask = np.ones(src.shape,np.int8)
    alpha = np.zeros(src.shape,np.int8)
    if (view.contour != None) :
			# draw this contour
            thisContours = []
            contour = RectUtil.convertToParentCorrdinate(view, view.contour)
            thisContours.append(contour)

    cv2.polylines(mask, thisContours, True, ColorUtil.getScalar(0),cv2.FILLED)

#            Imgproc.drawContours(mask, contours, -1, new Scalar(0), Core.FILLED);
		

		# Extra and update x, y of children's contours and rects
    rects = []
    for child in children:
        contour = child.contour
        if (contour == None) :
                bound = RectUtil.convertToParentCorrdinate(view, child)
                (x1,y1,width,height)= cv2.boundingRect(bound)
                rect = Rect(x1,y1,width,height)
                rects.append(rect)
        else :
            contour = RectUtil.convertToParentCorrdinate(view, contour);
            contours.append(contour)
			
		

		# Fill children's inner contours with white and outer contours with
		# black
#		Imgproc.drawContours(mask, contours, -1, new Scalar(255), Core.FILLED);
    cv2.polylines(mask, contours, True, ColorUtil.getScalar(255),cv2.FILLED)

		# Fill inner rects with white and outer rects with black
    for rect in rects:
        cv2.rectangle(mask, rect.tl(), rect.br(), ColorUtil.getScalar(255), cv2.FILLED)
		

		# inverse: black -> white and white -> black
    newMask = np.zeros(src.shape, np.int8)
    cv2.bitwise_not(mask, newMask)
    retval, alpha =   cv2.threshold(newMask,100,255,cv2.THRESH_BINARY)
    b,g,r = cv2.split(src)
    merge = cv2.merge((b,g,r,alpha))
    return merge
	

def removeChildren( src, view) :
    contours = []
    children = view.mChildren
		# black out
    mask = np.ones(src.shape, np.int8)
    thisContours = []

    if (view.contour != None) :

			# draw this contour
        contour = RectUtil.convertToParentCorrdinate(view, view.contour)
        thisContours.append(contour);
#        Imgproc.drawContours(mask, contours, -1, new Scalar(0), Core.FILLED);
    cv2.polylines(mask, thisContours, True, ColorUtil.getScalar(0),-1)


		# Extra and update x, y of children's contours and rects
    rects = []
    for child in children:
        contour = child.contour
        if (contour == None) :
            rect = RectUtil.convertToParentCorrdinate(view,child)
            rects.append(rect)
        else :
            contour = RectUtil.convertToParentCorrdinateContour(view, contour)
            contours.append(contour)
			
		
    cv2.polylines(mask, contours, True, ColorUtil.getScalar(255),cv2.FILLED)

		# Fill children's inner contours with white and outer contours with
		# black
#    Imgproc.drawContours(mask, contours, -1, new Scalar(255), Core.FILLED);
		# Fill inner rects with white and outer rects with black
    for rect in rects:
        cv2.rectangle(mask, rect.tl(), rect.br(), ColorUtil.getScalar(255), cv2.FILLED)
		

		# inverse: black -> white and white -> black
    newMask = np.zeros(src.shape,np.int8)
    cv2.bitwise_not(mask, newMask)

		# let's create a new image now
#    crop = new (src.rows(), src.cols(), CvType.CV_8UC3);

		# set background to dominate color
    width = 0 
    height = 0
    
    if len(src.shape) == 2 :
        height, width = src.shape
    else:
        height, width,channels = src.shape
    crop = np.zeros(src.shape, src.dtype)
    crop[:] = ColorUtil.getScalar(ColorUtil.findDominateColor(Rect(0, 0, width, height), src))
    np.copyto(crop, src, 'unsafe', newMask.astype(bool))
    return crop
	
#
#	 void writePng( path,  ) :
#		Of Of = new Of(new [] :
#				Highgui.CV_IMWRITE_PNG_COMPRESSION, 9 );
#		Highgui.imwrite(path, , Of);
	
#
#	 void log( outLogFolder,  fileName,  type,
#			List<OfPo> contours,  image, boolean clearImageContent,
#			boolean randomColor, ImageChangeListener imageChangeListener) :
#
#		if (!randomColor) :
#			log(outLogFolder, fileName, type, contours, image,
#					clearImageContent, new Scalar(0, 0, 255), imageChangeListener);
#			return;
#		
#		
#		  copyImage = copyImage(image);
#		if (clearImageContent) :
#			fillRect(copyImage,
#					new Rect(0, 0, () copyImage.size().width,
#							() copyImage.size().height), ColorUtil.to(
#							255, 255, 255, 255));
#		
#
#		for (OfPo OfPo : contours) :
#			Scalar scalar = ColorUtil.getScalar(ColorUtil.randomColor());
#			 List<OfPo> OfPos = new ArrayList<OfPo>();
#			OfPos.add(OfPo);
#			Core.polylines(copyImage, OfPos, true, scalar);
#		
#		log(outLogFolder, fileName, type, copyImage, imageChangeListener);
#	
#
#	 void log( outLogFolder,  fileName,  type,
#			List<OfPo> contours,  image, boolean clearImageContent,
#			Scalar color, ImageChangeListener imageChangeListener) :
#		  copyImage = copyImage(image);
#		if (clearImageContent) :
#			fillRect(copyImage,
#					new Rect(0, 0, () copyImage.size().width,
#							() copyImage.size().height), ColorUtil.to(
#							255, 255, 255, 255));
#		
#		Core.polylines(copyImage, contours, true, color, 2);
#		log(outLogFolder, fileName, type, copyImage, imageChangeListener);
#	
#
#	 static BufferedImage toBufferedImage( m):
#		 type = BufferedImage.TYPE_BYTE_GRAY;
#		if ( m.channels() > 1 ) :
#			type = BufferedImage.TYPE_3BYTE_BGR;
#		
#		 bufferSize = m.channels()*m.cols()*m.rows();
#		byte [] b = new byte[bufferSize];
#		m.get(0,0,b); # get all the pixels
#		BufferedImage image = new BufferedImage(m.cols(),m.rows(), type);
#		 byte[] targetPixels = ((DataBufferByte) image.getRaster().getDataBuffer()).getData();
#		System.arraycopy(b, 0, targetPixels, 0, b.length);
#		return image;
#	
#
