from Rules import ASingleRule
from Utils import ColorUtil
from RectUtils import RectUtil
from Rules import TextValidator
from Utils import Constants
from ocr.OCRTextWrapper import OCRTextWrapper
from Utils import GroupUtil
from Utils import TextUtils

class RuleCharacterDistance(ASingleRule.ASingleRule):

    def __init__(self,dipCalculator, tesseractOCR, matLog, ocrs, views):
            super().__init__(dipCalculator, tesseractOCR, matLog, ocrs, views)

#    @Override
    def accept(self,ocr):
        rects = []
        ocrBound = ocr.bound()
        for view in self.mViews:
            # accept overlap here
            if not self.mDipCalculator.isViewToBeIgnoreView(view) and RectUtil.contains(ocrBound, view.bound(), 0.5):
                rects.append(view.bound())

        if len(rects) >= 2 :
            RectUtil.sortTopBottom(rects)

            # distance between 2 characters are greater than the character
            # itself this have to be true for all of character
            invalidWordWithChars = False
            for i in range(len(rects) - 1):
                current = rects[i]
                next_rect = rects[i + 1]
                # ignore intersect one
                if RectUtil.intersects(current, next_rect):
                    continue

                if current.width < next_rect.x - (current.x + current.width):
                    invalidWordWithChars = True
                else:
                    invalidWordWithChars = False
                    break

            if invalidWordWithChars:
                # SkyBlue
                tv = TextValidator.TextValidator(ocr, (135,206, 235), False,"distance between 2 characters are greater than the character itself: ")
                return tv

        return None
