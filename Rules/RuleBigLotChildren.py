from Rules.ASingleRule import ASingleRule
from Utils import ColorUtil
from RectUtils import RectUtil
from Rules.TextValidator import TextValidator
from Utils import Constants
from ocr.OCRTextWrapper import OCRTextWrapper
from Utils import GroupUtil
from Utils import TextUtils
from Utils.ColorUtil import CColor
class RuleBigLotChildren(ASingleRule):
    
    def __init__(self,dipCalculator, tesseractOCR, matLog, ocrs, views):
            super().__init__(dipCalculator, tesseractOCR, matLog, ocrs, views)

#    @Override
            #TODO
    def accept(self,ocr):
        bound = ocr.bound()
#        return None
        for view in self.mViews:
            # woa this word is big and have a lot of children, not good
            # this may okay with url or special texts
            if RectUtil.contains(bound, view.bound()) and len(view.mChildren) > 0:
                tv =  TextValidator(ocr, CColor.Cyan, False, "This word is big and have a lot of children" + str(len(view.mChildren)))
                return tv
        
        return None
