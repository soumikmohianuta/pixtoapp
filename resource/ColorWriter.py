from Utils import XmlUtil
from Utils import Constants
from resource import TextResource
from xml.etree.ElementTree import Element, SubElement, Comment, tostring


class ColorWriter(TextResource.TextResource):

    def __init__(self):
        super().__init__()
#        self.mDocument = XmlUtil.createDocument();
        self.mRoot = Element(Constants.ELEMENT_RESOURCE)
        self.mDataIndexMap = {}
        self.addDefaultResource()
    
    def addDefaultResource(self):
        
        element = SubElement(self.mRoot, Constants.ELEMENT_COLOR)
        element.set(Constants.ATTRIBUTE_NAME, "colorPrimary")
        element.text = "#3F51B5"
        element = SubElement(self.mRoot, Constants.ELEMENT_COLOR)
        element.set(Constants.ATTRIBUTE_NAME, "colorPrimaryDark")
        element.text = "#303F9F"
        element = SubElement(self.mRoot, Constants.ELEMENT_COLOR)
        element.set(Constants.ATTRIBUTE_NAME, "colorAccent")
        element.text = "#FF4081"

    def addResource(self, color):

        _id = "color_"
        if color in self.mDataIndexMap:
            index = self.mDataIndexMap[color]
            _id = _id + str(index)
        else:
            _id = _id + str(self.mId)
            self.mDataIndexMap[color] = self.mId
            self.mId = self.mId + 1
            element = SubElement(self.mRoot, Constants.ELEMENT_COLOR)
            element.set(Constants.ATTRIBUTE_NAME, _id)
            element.text = color
        
        return _id
    