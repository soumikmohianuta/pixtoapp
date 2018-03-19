# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 00:16:19 2017

@author: soumi
"""
#import numpy as np
import cv2
from viewProcessor.Canny import Canny
from viewProcessor.ContourAnalysis import ContourAnalysis
from viewProcessor.ContourAnalysis import ContourInfo
from Utils.Project import Project
from HierarchyInfo import ViewHierarchyProcessor
from Utils.DipCalculator import DipCalculator
from Utils.Resolution import Resolution
from Utils.Profile import Profile
from Utils import Environment
from ocr.TesseractOCR import TesseractOCR
from ocr.TextProcessor import TextProcessor
from Utils.ColorUtil import CColor
from ocr.TextInfo import TextInfo
from Utils import Util
from layout.RootAlignmentLayoutFilter import RootAlignmentLayoutFilter
from layout.RelativeLayoutFilter import RelativeLayoutFilter
from layout.DefaultLayoutCreator import DefaultLayoutCreator
from layout.LayoutCreatorForList import LayoutCreatorForList
from layout.LayoutCreator import LayoutCreator
import layout.LayoutHelper as LayoutHelper
from layout.LayoutFilter import LayoutFilter
from projectUtil import ProjectGenerator
import copy
from Utils import XmlUtil
from Utils import Constants
from resource.DrawableWriter import DrawableWriter
import os
from projectUtil.ProjectInfo import ProjectInfo



PROJECT_FOLDER = "templates\\uploads\\"

def generateProjectName(mFileName):
    filename, file_extension = os.path.splitext(mFileName)
    mProjectName = Util.getProjectName(filename)
    return mProjectName

def generateProject(imageLocation):

    fileExitst = os.path.isfile(imageLocation)
    if(not fileExitst):
        return "Can't access the file"
    img_color = cv2.imread(imageLocation)
    
    img_gray = copy.deepcopy(img_color)
    if (len(img_color.shape)==3):
        img_gray  = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
    
    profile =  Profile(Resolution.XXHDPI, img_gray.shape[1], img_gray.shape[0])

    dipCalculator = DipCalculator(img_color,profile)


    width = 0 
    height = 0
    if len(img_color.shape) == 2 :
        height, width = img_color.shape
    else:
        height, width,channels = img_color.shape
    
    #create a valid project name and package name
    
    mProjectName = generateProjectName(imageLocation)
    mOutProjectFolder = PROJECT_FOLDER + mProjectName 

    #create project info
    
    mProjectInfo = ProjectInfo(mProjectName, mOutProjectFolder)
    
    filename, file_extension = os.path.splitext(imageLocation)
    mDrawableWriter = DrawableWriter(file_extension, mOutProjectFolder)
	
    #generate project from project template
    ProjectGenerator.setup(mProjectInfo)


# dilate and find edges in the provided screenshot
    dst_denoised = cv2.fastNlMeansDenoising(img_gray)
    canny = Canny()
    dst_edge = canny.findEdge(img_gray)  
#    project = Project("sample")
    dst_edge_dilate = canny.addDilate(dst_edge)
    contourAnalysis = ContourAnalysis()
    contours = contourAnalysis.findContoursWithCanny(dst_edge_dilate)
    contoursOutput = contourAnalysis.analyze(dst_edge_dilate, contours)

#do the hierarchy processing
    hierarchyProcessor = ViewHierarchyProcessor(contoursOutput.rootView, img_color, canny)
    hierarchyInfo = hierarchyProcessor.process()

# use tesseract to detect the text 
    tesseractOCR = TesseractOCR(dst_denoised,dipCalculator,"English")
    textProcessor = TextProcessor(img_color,dst_denoised, hierarchyInfo.biMapViewRect, tesseractOCR, dipCalculator)
# process text to remove invalid texts    
    textInfo = textProcessor.processText(CColor.Red)
# Add text boxes to hierarchy    
    hierarchyProcessor.addTextToHierarchy(textInfo)


# List support right now not implemented
#        creator = LayoutCreatorForList(contoursOutput.rootView, mProjectName, tesseractOCR, mDrawableWriter, img_color, mFileName,
#                           mOutLogFolder, mOutProjectFolder, dipCalculator)
 #   else:
    creator = DefaultLayoutCreator(contoursOutput.rootView, mProjectName, tesseractOCR, mDrawableWriter, img_color, mOutProjectFolder, dipCalculator)

# create layout
    layoutDocument = creator.createDocument()
    layoutFilter = LayoutFilter()
#
    anotateMap = layoutFilter.anotate(layoutDocument)

    layoutFilter = RelativeLayoutFilter()
    layoutFilter.doFilter(layoutDocument, anotateMap)
    layoutFilter = RootAlignmentLayoutFilter()
    layoutFilter.doFilter(layoutDocument, anotateMap)

# write to xml
    XmlUtil.writeDocumentxml(layoutDocument, mOutProjectFolder + Constants.DEFAULT_LAYOUT_PATH + "activity_main.xml")

# write style
    styleWriter = creator.mStyleWriter
    styleDocument = styleWriter.mRoot
    XmlUtil.writeDocumentxml(styleDocument, mOutProjectFolder + "\\app\\src\\main\\res\\values\\styles.xml")
#
#write to color file    
    colorWriter = creator.mColorWriter
    colorDocument = colorWriter.mRoot
    XmlUtil.writeDocumentxml(colorDocument, mOutProjectFolder + "\\app\\src\\main\\res\\values\\colors.xml")

# write to string file
    stringWriter = creator.mWriter
    resourceDocument = stringWriter.mRoot
    XmlUtil.writeDocumentxml(resourceDocument, mOutProjectFolder + "\\app\\src\\main\\res\\values\\strings.xml")

# save drawable files
    mDrawableWriter.save()

# compile and create a zip of the project
    ProjectGenerator.prepareProject(mProjectInfo)
#    ProjectGenerator.unInstallAPK(mOutProjectFolder,mPackageName)
#    ProjectGenerator.installAPK(mOutProjectFolder,mProjectName)
    return

if __name__ =="__main__":
    filename = r"download2.png"
    generateProject(filename)
