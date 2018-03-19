from Rules.AVisionRule import AVisionRule
from Utils import ColorUtil
from RectUtils import RectUtil
from Utils.ColorUtil import CColor
from Rules.TextValidator import TextValidator

class RuleTextTooBigCompWords (AVisionRule):
    
    def __init__ (self, dipCalculator, tesseractOCR, matLog, ocrs, views):
        super().__init__(dipCalculator, tesseractOCR, matLog, ocrs, views)

    #@Override
    def run(self, invalidTexts, acceptedOcrTextWrappers):

        # Step 2: Validate base on view

        match = False
        for view in self.mViews:
            # the box may has the word is too big compare to the word
            # itself and there is only one word in here
            wordsIn = self.mTesseractOCR.getWordsIn(view.bound())
            
            for key in invalidTexts:
                if key in wordsIn:
                    wordsIn.remove(key)
            
            if len(wordsIn) == 1 and len(view.mChildren) == 0 :
                # TODO: Try to find if there is any other word intersect with
                # this view
                if (RectUtil.contains(view, wordsIn[0])) :
                    ocrTextWrapper = wordsIn[0]
                    ob = ocrTextWrapper.bound()
                    vb = view.bound();
                    ratioWidth = float (ob.width / vb.width)
                    ratioHeight = float(ob.height / vb.height)

                    maxDimRatio = max(ratioWidth, ratioHeight);
                    minDimRatio = min(ratioWidth, ratioHeight);
                    # 1. Both dim really small < 0.4F
                    # 2. Max dim is a little bit small < 0.7F, but min dim is
                    # small < 0.2F.
                    # 3. Max dim is big, min dim have to be really small < 0.2F
                    if (maxDimRatio < 0.4 or (maxDimRatio < 0.7 and minDimRatio < 0.4)) or (maxDimRatio >= 0.7 and minDimRatio < 0.2):
                        # this is wrong, ignore this word
                        textValidator = TextValidator(ocrTextWrapper, CColor.Green,False,"The box, which may has the word, is too big compare to the word, and there is only one word in here")
                        invalidTexts[textValidator.textWrapper] = textValidator
                        match = True
       
        return match
    
