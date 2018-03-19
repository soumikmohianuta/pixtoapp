from Rules.ASingleRule import ASingleRule
from Utils.ColorUtil import *
from RectUtils import RectUtil
from Rules.TextValidator import TextValidator
from Utils import Constants
from ocr.OCRTextWrapper import OCRTextWrapper
from Utils import GroupUtil
from Utils import TextUtils
class RuleAlignVertically(ASingleRule):
    dotToNormalLetterRatio = 3
    
    def __init__(self,dipCalculator, tesseractOCR, matLog, ocrs, views):
            super().__init__(dipCalculator, tesseractOCR, matLog, ocrs, views)

#    @Override
            #TODO
    def accept(self,ocr):
        # this word have more than one view but align vertically
        # this may only right in English, when we write: left right, top
        # bottom

        ocrBound = ocr.bound()
        rects = []
        for view in self.mViews:
            # accept overlap here
            if not self.mDipCalculator.isViewToBeIgnoreView(view) and RectUtil.contains(ocrBound, view.bound(), 0.7):
                rects.append(view.bound())

        if len(rects) >= 2:
            maxHeight = 0
            for rect in rects:
                if(maxHeight<rect.height):
                    maxHeight = rect.height

            RectUtil.sortTopBottom(rects)
            first = rects[0] 
            # Remove dot from first
            while(self.dotToNormalLetterRatio*first.height <= maxHeight):
                del rects[0]
                first = rects[0]
            last = rects[len(rects) - 1] 
            # Remove dot from first
            while(self.dotToNormalLetterRatio*last.height <= maxHeight):
                del rects[len(rects) - 1]
                last = rects[len(rects) - 1]                       
 
            first = rects[0]
            last = rects[len(rects) - 1]                    
            if first.y + first.height <= last.y :
                tv = TextValidator(ocr,(148, 0, 211),False, "this word have more than one view but align vertically" )
                return tv
            
            
        return None
