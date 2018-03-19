from Rules import ASingleRule
from Utils import ColorUtil
from RectUtils import RectUtil
from Rules import TextValidator
from Utils import Constants
from ocr.OCRTextWrapper import OCRTextWrapper
from Utils import GroupUtil
from Utils import TextUtils
#/**
# * 
# * This word only have one child view, and the child view is too small compare
# * with it"
# *
# * @author tuannguyen
# * 
# */
#@Deprecated
class RuleWordOnlyOneTinyChild(ASingleRule.ASingleRule):
    
    def __init__(self,dipCalculator, tesseractOCR, matLog, ocrs, views):
            super().__init__(dipCalculator, tesseractOCR, matLog, ocrs, views)

#    @Override
    def accept(self,ocr):
        # Count to see how may child view this word have, if it only have
        # one child view. Test:
        # (1) This word is not messy. Mean that it did not
        # "intersect not include" with other views (except the child view)
        # (2) If the child view is too small compare with it
        foundChildRects = RectUtil.findChildRect(ocr.rect, self.mViews)
        if len(foundChildRects) == 1:
            rectView = foundChildRects[0]
            newList = []
            if rectView in newList:
                newList.remove(rectView)
            findIntersectNotIncludeRect = RectUtil.findIntersectNotIncludeRect(ocr, newList)
            if len(findIntersectNotIncludeRect) == 1:
                iRect = findIntersectNotIncludeRect[0]
                if RectUtil.dimesionEqual(ocr, iRect, 0.2) and RectUtil.dimesionSmallerThan(rectView, ocr, 0.8):
                    # this is wrong, ignore this word
                    # DarkSalmon
                    # http:#www.w3schools.com/tags/ref_color_tryit.asp?color=DarkSalmon
                    tv =  TextValidator.TextValidator(ocr, (233, 150, 122), False, "This word only have one child view, and the child view is too small compare with it")
                    return tv


        return None
