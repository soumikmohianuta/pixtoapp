from Rules.ASingleRule import ASingleRule
from Utils import ColorUtil
from RectUtils import RectUtil
from Rules.TextValidator import TextValidator
from Utils import Constants
from ocr.OCRTextWrapper import OCRTextWrapper
from Utils import GroupUtil
from Utils import TextUtils
from Utils.ColorUtil import CColor

class RuleSmallVericalShape(ASingleRule):
    
    def __init__(self,dipCalculator, tesseractOCR, matLog, ocrs, views):
            super().__init__(dipCalculator, tesseractOCR, matLog, ocrs, views)

#    @Override
    def accept(self, ocr):
        # this word's width is too small in compare with its height
        ocrBound = ocr.bound()
        ratio = float (ocrBound.width / ocrBound.height)
        if ratio >= 0.05:
            return None
        

        tv = TextValidator(ocr, CColor.Dark_gray, False,"this word's width is too small in compare with its height")
        return tv
    