
from RectUtils import RectUtil
from Utils import Constants
from layout import LayoutFilter
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import layout.LayoutHelper as LayoutHelper
from functools import cmp_to_key

#class RelativeLayoutFilter (LayoutFilter):
class RelativeLayoutFilter ():

#    def __init__(self):
#        super().__init__()
    
    def doFilter(self,document,anotateMap):
#         Update layout
        elements = list(document.iter())
        for node in elements:
            self.doFilderInternal(node, anotateMap)
#        return self.doFilderInternal(document, anotateMap)

#    @Override
    def doFilderInternal(self, root, anotateMap):
#        @SuppressWarnings("unchecked")
        elements = list(root.iter())


        if (self.isDefaultElement(root)):
            datas = []

            for node in elements:
                datas.append(anotateMap[node])
            
            # System.out.println("elements.size(): " + elements.size())
            if (len(elements) <= 1):
                return root

            # Check if children are overlapped
            if (not RectUtil.noOverlap(datas)):
                return root
            
            # System.out.println("noOvelap")
            root.tag = LayoutCreator.RELATIVELAYOUT_ELEMENT

            # First sort all children vertically
            datas.sort(key=cmp_to_key(RectUtil.getTopBottomComparator))
            # Find the top left one
            rootElement = anotateMap[root]
            topLeftElementData = RectUtil.findTopLeft(rootElement, datas)

            processElementDatas = set()
            processElementDatas.add(topLeftElementData)
            # Make the topleft child at the top left of the parent
            
            topLeftElement = [key for key, value in anotateMap.items() if value == topLeftElementData][0]
            
            topLeftElement.set(
                    Constants.ATTRIBUTE_LAYOUT_ALIGN_PARENT_TOP, "true")
            topLeftElement.set(
                    Constants.ATTRIBUTE_LAYOUT_ALIGN_PARENT_LEFT, "true")

            # Update relative location of other children
            for elementData in datas:
                if (elementData not in processElementDatas):
                    # Find the one more top than me
                    smallerTop = RectUtil.findClosestSmallerTop(elementData, processElementDatas)
                    smallerLeft = RectUtil.findClosestSmallerLeft(elementData, processElementDatas)
                    element = [key for key, value in anotateMap.items() if value == elementData][0]
                    # System.out.println(elementData)
                    if (smallerTop != None):
                        smallerTopElement = [key for key, value in anotateMap.items() if value == smallerTop][0]
                        # System.out.println("\tsmallerTop: " + smallerTop)
                        element.set(Constants.ATTRIBUTE_LAYOUT_ALIGN_TOP, smallerTopElement.get(Constants.ATTRIBUTE_ID))
                        element.set(Constants.ATTRIBUTE_LAYOUT_MARGIN_TOP, str(elementData.y - smallerTop.y)+ Constants.UNIT_DIP)
                    else:
                        element.set(Constants.ATTRIBUTE_LAYOUT_ALIGN_PARENT_TOP,"true")
                   

                    if (smallerLeft != None):
                        # System.out.println("\tsmallerLeft: " + smallerLeft)
                        smallerLeftElement = [key for key, value in anotateMap.items() if value == smallerLeft][0]
                        element.set(Constants.ATTRIBUTE_LAYOUT_ALIGN_LEFT,smallerLeftElement.get(Constants.ATTRIBUTE_ID))
                        element.set(Constants.ATTRIBUTE_LAYOUT_MARGIN_LEFT, str(elementData.x - smallerLeft.x )+ Constants.UNIT_DIP)
                    else:
                        element.set(Constants.ATTRIBUTE_LAYOUT_ALIGN_PARENT_LEFT,"true")
                    
                    processElementDatas.add(elementData)
        return root
    
    def isDefaultElement(self,element):
        return LayoutHelper.FRAMELAYOUT_ELEMENT == element.tag