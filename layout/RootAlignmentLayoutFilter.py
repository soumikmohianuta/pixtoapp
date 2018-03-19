from Utils import XmlUtil
from Utils import Constants
from layout import LayoutFilter

class RootAlignmentLayoutFilter(LayoutFilter.LayoutFilter):

    
    def doFilter(self,root,anotateMap):
#         Update layout
        return self.doFilderInternal(root, anotateMap)


#	@Override
    def doFilderInternal(self,root, anotateMap):
        XmlUtil.addLayoutGravity(root, Constants.ATTRIBUTE_LAYOUT_GRAVITY_CENTER_VERTICAL + "|" + Constants.ATTRIBUTE_LAYOUT_GRAVITY_CENTER_HORIZONTAL)
        return root
