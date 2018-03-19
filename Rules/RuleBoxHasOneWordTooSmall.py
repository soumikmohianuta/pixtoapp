from Rules.ASingleRule import ASingleRule
from Utils import ColorUtil
from RectUtils import RectUtil
from Rules.TextValidator import TextValidator
from Utils import Constants
from ocr.OCRTextWrapper import OCRTextWrapper 
from Utils import GroupUtil
from Utils import TextUtils
import ocr.TextProcessorUtil as TextProcessorUtil
from Utils.ColorUtil import CColor
class RuleBoxHasOneWordTooSmall(ASingleRule):
    
    def __init__(self,dipCalculator, tesseractOCR, matLog, ocrs, views):
            super().__init__(dipCalculator, tesseractOCR, matLog, ocrs, views)

#    @Override
    def accept(self,ocr):
         bound = ocr.bound()
         for view in self.mViews :
#            // the box may has the word is too small compare with the word
#            // itself.
#            // If the word a children view which only have on child, we need
#            // to verify if:
#            // (2) This child view really small compare to the word bound
#            // same here: the box may has the word is too big compare to the
#            // word itself we also make sure that this view may also have
#            // other view but it so tiny will be ignore when layout
#            // itself and there is only one word in here
            if TextProcessorUtil.areChildrenIsTooSmall(self.mDipCalculator, view) and RectUtil.contains(view.bound(), bound):
                if RectUtil.dimesionSmallerThan(ocr, view, 0.8):
                    # this is wrong, ignore this word
                    tv =  TextValidator(ocr, CColor.Pink, False, "The box may has the word is too big compare to the word, and there is only one word in here. This view may also have other view but it so tiny")
                    return tv
                
         return None
