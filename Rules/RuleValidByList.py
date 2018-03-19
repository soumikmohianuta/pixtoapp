from Rules.ASingleRule import ASingleRule
from Utils import ColorUtil
from RectUtils import RectUtil
from Rules.TextValidator import TextValidator
from Utils import Constants
from ocr.OCRTextWrapper import OCRTextWrapper
from Utils import GroupUtil
from Utils import TextUtils
from Utils.ColorUtil import CColor

class RuleValidByList(ASingleRule):
    
    def __init__(self,dipCalculator, tesseractOCR, matLog, ocrs, views):
            super().__init__(dipCalculator, tesseractOCR, matLog, ocrs, views)
            self.mInvalidTexts = self.findInInvalidTextByList(ocrs)

#    @Override


    #@Override
    def accept(self, ocr):
        if ocr not in self.mInvalidTexts:
            return None

        tv = TextValidator(ocr,CColor.Magenta, False, "invalid text by list")
        return tv
       
    
    def sameGroup(self,element1, element2):
        return RectUtil.equal(element1, element2)
            

    def findInInvalidTextByList(self, ocrs) :
        invalidTexts = []
        
        groups = GroupUtil.group(ocrs, self.sameGroup)
    
        for group in groups:
            if len(group) >= Constants.MIN_ACCEPTABLE_LIST_SIZE_FOR_INVALID_LIST_TEXT :
                for ocrTextWrapper in group:
                    if ocrTextWrapper.confidence <= Constants.MIN_INVALID_LIST_TEXT_THRESHOLD and not TextUtils.isEmpty(ocrTextWrapper.text) and len(ocrTextWrapper.text) == 1 :
                        invalidTexts.append(ocrTextWrapper);
                    
        return invalidTexts;
    
