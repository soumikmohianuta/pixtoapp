from Rules.ASingleRule import ASingleRule
from Utils import ColorUtil
from RectUtils import RectUtil
from Rules.TextValidator import TextValidator
from Utils import Constants
from ocr.OCRTextWrapper import OCRTextWrapper
from Utils import GroupUtil
from Utils import TextUtils
from Utils.ColorUtil import CColor
from Utils.ColorUtil import CColor

class RuleSmallHorizontalShape(ASingleRule):
    def __init__(self,dipCalculator, tesseractOCR, matLog, ocrs, views):
            super().__init__(dipCalculator, tesseractOCR, matLog, ocrs, views)

#    @Override
    def accept(self, ocr):
        ocrBound = ocr.bound()
        ratio = float(ocrBound.height / ocrBound.width)
        if ratio >= 0.05:
                return None
        

        tv = TextValidator(ocr, CColor.Magenta,False,"this word's height is too small in compare with its width")
        return tv
    