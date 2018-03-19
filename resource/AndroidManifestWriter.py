from Utils import Environment
from Utils import Util
from Utils import XmlUtil
from Utils import Constants
from xml.etree.ElementTree import Element, SubElement, Comment, tostring, parse
import xml.etree.ElementTree as ET
import layout.LayoutHelper as LayoutHelper


class AndroidManifestWriter:

    MIN_SDK_VERSION = "19";
    TARGET_SDK_VERSION = "21";

#	private String mAndroidManifestPath;
#	private String mOutputFolderPath;
#	private Document mDocument;

    def __init__(self,outputFolderPath):
        self.mOutputFolderPath = outputFolderPath
        self.mAndroidManifestPath = outputFolderPath + "/app/src/main/AndroidManifest.xml"
        self.mDocument = parse(self.mAndroidManifestPath).getroot()
	

    def updateManifestFile(self,orientation):

#		@SuppressWarnings("unchecked")
        selectNode = self.mDocument.find('application')
        selectNodes= selectNode.findall('activity')

        if (Environment.getValue(Environment.KEY_WITH_TITLE_BAR) == False):
#			 change theme
            for node in selectNodes:
#                element = Element(node)
                node.set("android:theme","@android:style/Theme.Black.NoTitleBar")
#		// change orientation
        if (orientation == LayoutHelper.ORIENTATION_LANDSCAPE):
            for node in selectNodes:
#                element = Element(node)
                node.set("android:screenOrientation", "landscape")

    def write(self):
        XmlUtil.writeDocumentxml(self.mDocument, self.mAndroidManifestPath)


    def addUseSDKTag(self):
        applicationNode = self.mDocument.find('manifest')
        if (applicationNode != None and type(applicationNode) == Element):
            applicationElement = Element(applicationNode)
            useSdkElement = SubElement(applicationElement,"uses-sdk")
            useSdkElement.set(Constants.ATTRIBUTE_MIN_SDK_VERSION,self.MIN_SDK_VERSION);
            useSdkElement.set(Constants.ATTRIBUTE_TARGET_SDK_VERSION, self.TARGET_SDK_VERSION);
