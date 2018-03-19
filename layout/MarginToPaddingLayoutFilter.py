from Utils import Constants
from layout.LayoutFilter import LayoutFilter
from Utils import XmlUtil
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import sys

class MarginToPaddingLayoutFilter(LayoutFilter):

    
    def __init__(self):
                super().__init__()

#	@Override
    def doFilderInternal(self, root, anotateMap):
#		@SuppressWarnings("unchecked")
        elements = [elem for elem in root.iter()]

        for node in elements:
            self.doFilderInternal(Element(node), anotateMap)
		

		# Convert children margin left to parent padding left
        self.updateMargin(root, Constants.ATTRIBUTE_PADDING_LEFT, Constants.ATTRIBUTE_LAYOUT_MARGIN_LEFT)

		# Convert children margin top to parent padding top
        self.updateMargin(root, Constants.ATTRIBUTE_PADDING_TOP, Constants.ATTRIBUTE_LAYOUT_MARGIN_TOP)

        return root
	

    def updateMargin(root, attributeLayoutPaddingName, attributeLayoutMarginName) :
#		@SuppressWarnings("unchecked")
        elements = [elem for elem in root.iter()]
        
        if (len(elements) == 0) :
            return
		
		# Check if all children have margin dip value
        for node in elements:
            element = Element (node)
            if (not XmlUtil.hasDipValue(element, attributeLayoutMarginName)) :
                return
			
		

        paddingValue = 0
        if (XmlUtil.hasDipValue(root, attributeLayoutPaddingName)) :
            paddingValue = XmlUtil.getDipValue(root, attributeLayoutPaddingName)
		
		# find min margin
        minMargin = sys.maxint
        for node in elements:
            element = Element(node)
            minMargin = min(minMargin, XmlUtil.getDipValue(element,attributeLayoutMarginName))
		
		# we add more margin to the parent
        paddingValue += paddingValue + minMargin

        if (paddingValue == 0) :
            return
		

        root.addAttribute(attributeLayoutPaddingName, paddingValue + Constants.UNIT_DIP)

		# we subtract margin from children
        for node in elements:
            element = Element(node)
            root.set(attributeLayoutMarginName, XmlUtil.getDipValue(element, attributeLayoutMarginName) - minMargin + Constants.UNIT_DIP)
		
	

