
#class LayoutFilter:
#
#    public LayoutFilter() {
#
#    }
from Utils import XmlUtil
from layout.ElementData import ElementData
from layout import LayoutCreator
from functools import cmp_to_key

from Utils import Constants
class LayoutFilter:
        
    def __init__(self):
        print("do nothing")
    

    def doFilter(self,document,anotateMap):
#         Update layout
        return self.doFilderInternal(document, anotateMap)

    def doFilderInternal(self, root, anotateMap):
        return 

    def anotate(self, document):
        elementDataMap = {}
        elements = list(document.iter())
        for node in elements:
            self.anotateIntenal(node, elementDataMap)
        return elementDataMap
    
    def anotateIntenal(self, root, elementDataMap):
        top = int (XmlUtil.getDipValue(root, Constants.ATTRIBUTE_LAYOUT_MARGIN_TOP))
        left = int(XmlUtil.getDipValue(root, Constants.ATTRIBUTE_LAYOUT_MARGIN_LEFT))
        width = int (XmlUtil.getDipValue(root,Constants.ATTRIBUTE_LAYOUT_WIDTH))
        height = int(XmlUtil.getDipValue(root,Constants.ATTRIBUTE_LAYOUT_HEIGHT))

        data = ElementData(top, left, width, height)
        elementDataMap[root] = data

#        @SuppressWarnings("unchecked")  //TODO



    def isDefaultElement(self,element):
        return LayoutCreator.FRAMELAYOUT_ELEMENT == element.tag
  