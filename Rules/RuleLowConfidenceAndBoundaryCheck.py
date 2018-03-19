from Rules import ASingleRule
from Utils import ColorUtil
from RectUtils.RectUtil import *
from Rules import TextValidator
from Utils import Constants
from Utils import GroupUtil
from Utils import TextUtils
from Utils.ColorUtil import CColor

class RuleLowConfidenceAndBoundaryCheck (ASingleRule.ASingleRule):

    def __init__(self,dipCalculator, tesseractOCR, matLog, ocrs, views):
            super().__init__(dipCalculator, tesseractOCR, matLog, ocrs, views)

#    @Override
    def accept(self,ocr):
#        return None

        testMessage = self.isValidTextUsingConfidentAndBoundaryCheck(ocr)
        if testMessage == None:
            return None

        tv = TextValidator.TextValidator(ocr,CColor.Magenta, False,testMessage )
        return tv

    def isValidTextUsingConfidentAndBoundaryCheck(self,ocrTextWrapper):
        if (ocrTextWrapper.confidence > Constants.TEXT_CONFIDENT_THRESHOLD + Constants.TEXT_CONFIDENT_THRESHOLD_SECONDARY_RANGE):
            return None
        self.mTesseractOCR.getRectWordForLowConfidence(ocrTextWrapper)
        if (ocrTextWrapper.confidence <= Constants.TEXT_CONFIDENT_THRESHOLD):
            return "low confident"
        #TODO
        if ocrTextWrapper.fontSize == -1:
            return "No Font Attribute"
        validTextUsingBoundaryCheck = self.mTesseractOCR.isValidTextUsingBoundaryCheck(ocrTextWrapper);
#        validTextUsingBoundaryCheck = True
        if validTextUsingBoundaryCheck:
            return None
        else:
            return "fail boundary check"

