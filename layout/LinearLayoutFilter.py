from layout.LayoutFilter import LayoutFilter
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from RectUtils import RectUtil
from layout import LayoutCreator
from functools import cmp_to_key


class LinearLayoutFilter(LayoutFilter):
    def __init__(self):
        super().__init__()
    

#	@Override
    def doFilderInternal(self,root, anotateMap):
#		@SuppressWarnings("unchecked")
        elements = [elem for elem in root.iter()]

        for node in elements:
            self.doFilderInternal(Element(node), anotateMap)

        if (self.isDefaultElement(root)):
            datas = []

            for  node in elements:
                child = Element(node)
                datas.append(anotateMap[child])
            if len(elements) <= 1 :
                return root

#			// Check if children are overlapped
            if (not RectUtil.noOvelap(datas)):
                return root
#            System.out.println("noOvelap");

#			// check if children order horizontally
#			if (RectUtil.isOrderHorizontally(datas)) {
#				
#				
#			} 
            if (RectUtil.isOrderVertically(datas)):
#				 check if children order vertically
                root.setName(LayoutCreator.RELATIVELAYOUT_ELEMENT);
#				// First sort all children vertically
                datas.sort(key=cmp_to_key( RectUtil.getLeftRightComparator()))
#				for (ElementData elementData : datas) {
#					
#				}
            else:
                return root;
			

#			for (Node node : elements) {
#				Element child = (Element) node;
#				
#			}
#		}

        return root;
