from Rules.ASingleRule import ASingleRule
from Utils import ColorUtil
from RectUtils import RectUtil
from Rules.TextValidator import TextValidator
from Utils import Constants
from ocr.OCRTextWrapper import OCRTextWrapper
import ocr.TextProcessorUtil as TextProcessorUtil
from Utils import GroupUtil
from Utils import TextUtils
from Utils.ColorUtil import CColor

class RuleNoChildren (ASingleRule):
    def __init__(self,dipCalculator, tesseractOCR, matLog, ocrs, views):
            super().__init__(dipCalculator, tesseractOCR, matLog, ocrs, views)

#    @Override
    def accept(self, ocr):
#        return None
        hasChildren = TextProcessorUtil.hasParent(ocr, self.mOcrs)
        if not hasChildren:
            return None
        tv = TextValidator(ocr, CColor.Magenta, False, "no children")
        return tv
    

