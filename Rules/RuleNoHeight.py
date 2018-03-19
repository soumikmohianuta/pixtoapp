from Rules.ASingleRule import ASingleRule
from Utils import ColorUtil
from RectUtils import RectUtil
from Rules.TextValidator import TextValidator
from Utils import Constants
from ocr.OCRTextWrapper import OCRTextWrapper
from Utils import GroupUtil
from Utils import TextUtils
from Utils.ColorUtil import CColor

class RuleNoHeight(ASingleRule):
    def __init__(self,dipCalculator, tesseractOCR, matLog, ocrs, views):
            super().__init__(dipCalculator, tesseractOCR, matLog, ocrs, views)

#    @Override
    def accept(self, ocr):
        if ocr.bound().width > 0:
            return None
        
        
        tv = TextValidator(ocr, CColor.Magenta, False,"width is 0")
        return tv
