# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 02:11:47 2018

@author: soumi
"""

from Utils import Util
from Utils import XmlUtil
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, parse
from Utils import Constants
import zipfile
import os
debugMode = True

TEMPLATE_FOLDER = r"templates\\"

def clearContent(projectPath):
    Util.run("rm -rf"+ projectPath+ "*")


def createProject(projectInfo):
    Util.run("mkdir " +projectInfo.mPath)
    Util.run("Xcopy /E /I " +TEMPLATE_FOLDER +"templateProject "+ projectInfo.mPath)
    Util.run("templates\\fart.exe -i -r " +projectInfo.mPath + "\\* templateProject "+ projectInfo.mBaseName)
    Util.run("templates\\fart.exe -i -r " +projectInfo.mPath + "\\* TEMPLATEPROJECT "+ projectInfo.mBaseName.upper())
    Util.run("rename " +projectInfo.mPath +"\\templateProject.iml "+ projectInfo.mBaseName + ".iml")
    Util.run("rename " +projectInfo.mPath +"\\app\\src\\test\\java\\com\\example\\remaui\\templateproject "+projectInfo.mBaseName )
    Util.run("rename " +projectInfo.mPath +"\\app\\src\\main\\java\\com\\example\\remaui\\templateproject "+projectInfo.mBaseName )
    Util.run("rename " +projectInfo.mPath +"\\app\\src\\androidTest\\java\\com\\example\\remaui\\templateproject "+projectInfo.mBaseName )


def setup(projectInfo):
    if(os.path.exists(projectInfo.mPath)):
        Util.run("rmdir /s /q " + projectInfo.mPath)
    createProject(projectInfo)

    
    
def projectCompile(projectInfo):

    Util.run(projectInfo.mPath +"//gradlew assembleDebug" )
        



def prepareProject(projectInfo):

    zipFileName = "templates\\uploads\\"+projectInfo.mName + ".zip"
    projectCompile(projectInfo)

    zipdirectory(projectInfo.mPath,zipFileName )



def zipdirectory(basedir, archivename):
    zf = zipfile.ZipFile(archivename, "w", zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(basedir):
           #NOTE: ignore empty directories
           for fn in files:
               absfn = os.path.join(root, fn)
               zfn = absfn[len(basedir)+len(os.sep):] #XXX: relative path
               zf.write(absfn,zfn)
    zf.close()	



