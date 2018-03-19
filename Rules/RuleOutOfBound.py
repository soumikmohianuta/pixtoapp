from Rules.ASingleRule import ASingleRule
from Utils import ColorUtil
from RectUtils import RectUtil
from Rules.TextValidator import TextValidator
from Utils import Constants
from ocr.OCRTextWrapper import OCRTextWrapper
from Utils import GroupUtil
from Utils import TextUtils
from Utils.ColorUtil import CColor

class RuleOutOfBound(ASingleRule):
    
    def __init__(self,dipCalculator, tesseractOCR, matLog, ocrs, views):
            super().__init__(dipCalculator, tesseractOCR, matLog, ocrs, views)

#    @Override
    def accept(self, ocr):
    # this is an error of tesseract when text box go beyond the
        # boundary
        width = 0 
        height = 0
    
        if len(self.mMatLog.shape) == 2 :
            height, width = self.mMatLog.shape
        else:
            height, width,channels = self.mMatLog.shape
            
        ocrBound = ocr.bound()
        test = ocrBound.x < 0 or ocrBound.y < 0 or (ocrBound.x + ocrBound.width) > int(width) or (ocrBound.y + ocrBound.height) > int(height)
        if not test:
            return None

        tv =  TextValidator(ocr, CColor.Dark_gray, False, "this is an error of tesseract when text box go beyond the boundary")
        return tv
