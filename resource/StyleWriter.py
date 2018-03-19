from Utils import XmlUtil
from Utils import Constants
from Utils import TextUtils
from resource import TextResource
from xml.etree.ElementTree import Element, SubElement, Comment, tostring


class StyleWriter(TextResource.TextResource):

    def __init__(self):
        super().__init__()
#        self.mDocument = XmlUtil.createDocument();
        self.mRoot = Element(Constants.ELEMENT_RESOURCE)
        self.addDefaultStyle()
        
    def addDefaultStyle(self):
        element = SubElement(self.mRoot, Constants.ELEMENT_STYPE)
        element.set(Constants.ATTRIBUTE_NAME, "AppTheme")
        element.set("parent", "Theme.AppCompat.Light.DarkActionBar")
        itemElement = SubElement(element, Constants.ELEMENT_ITEM)
        itemElement.set(Constants.ATTRIBUTE_NAME, "colorPrimary")
        itemElement.text= "@color/colorPrimary"
        itemElement = SubElement(element, Constants.ELEMENT_ITEM)
        itemElement.set(Constants.ATTRIBUTE_NAME, "colorPrimaryDark")
        itemElement.text= "@color/colorPrimaryDark" 
        itemElement = SubElement(element, Constants.ELEMENT_ITEM)
        itemElement.set(Constants.ATTRIBUTE_NAME, "colorAccent")
        itemElement.text= "@color/colorAccent" 


    def addResource(self, properties):
        _id = "stype_" + str(self.mId)
        self.mId = self.mId + 1 
        element = SubElement(self.mRoot, Constants.ELEMENT_STYPE)
        element.set(Constants.ATTRIBUTE_NAME, _id)
        for pairProperty in properties:
            itemElement = SubElement(element, Constants.ELEMENT_ITEM)
            itemElement.set(Constants.ATTRIBUTE_NAME, pairProperty[0])
            itemElement.text= pairProperty[1] 
        
        return _id
    

