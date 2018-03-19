from Rules.ASingleRule import ASingleRule
from Utils import ColorUtil
from RectUtils import RectUtil
from Rules.TextValidator import TextValidator
from Utils import Constants
from ocr.OCRTextWrapper import OCRTextWrapper
from Utils import GroupUtil
from Utils import TextUtils
from Utils.ColorUtil import CColor
class RuleBoxHasWordTooSmall(ASingleRule):
    
    def __init__(self,dipCalculator, tesseractOCR, matLog, ocrs, views):
            super().__init__(dipCalculator, tesseractOCR, matLog, ocrs, views)

#    @Override
            # TODO
    def accept(self,ocr):
#        return None
        bound = ocr.bound();
        for view in self.mViews:
            # the box may has the word is too small compare with the word
            # itself.
            # If the word a children view which only have on child, we need
            # to verify if:
            # (1) This child view did not intersect with any other views
            if RectUtil.contains(bound, view.bound()) and len(view.mChildren) == 0 :
                # make sure this view did not intersect with other view,
                # include is accepted in this case
                hasIntersection = False
                for otherView in self.mViews:
                    if otherView != view and RectUtil.intersectsNotInclude(bound, otherView.bound()):
                        hasIntersection = True
                        break
                    
                if not hasIntersection:
                    if RectUtil.dimesionSmallerThan(view, ocr, 0.8):                        # this is wrong, ignore this word
                        tv = TextValidator(ocr, CColor.Black, False, "The box may has the word is too small compare with the word itself")
                        return tv
        return None
