from Rules.AVisionRule import AVisionRule
import ocr.TextProcessorUtil as TextProcessorUtil
from Utils import ColorUtil
from Rules.TextValidator import TextValidator

class RuleVisionBoxHasSoManyInvalidTexts(AVisionRule):

    def __init__ (self,dipCalculator, tesseractOCR, matLog, ocrs, views):
        super().__init__(dipCalculator, tesseractOCR, matLog, ocrs, views)

#    @Override
    def run(self, invalidTexts, acceptedOcrTextWrappers):

        match = False
        for rectView in self.mViews:
            # we only do this for leaf view
            if (len(rectView.mChildren) != 0 and not TextProcessorUtil.areChildrenIsTooSmall(self.mDipCalculator, rectView)):
                continue
            
            wordsIn = self.mTesseractOCR.getWordsIn(rectView.bound());
            if (len(wordsIn) <= 1):
                continue
            validWords = []
            inValidWords = []
            for includeOcrText in wordsIn:
                if includeOcrText in invalidTexts: 
                    inValidWords.append(includeOcrText)
                else:
                    validWords.append(includeOcrText)

#            // now all of them should be valid, I guess :-)
            if len(validWords) > len(inValidWords):
                for wordIn in wordsIn:
                    if wordIn in invalidTexts:
                        del invalidTexts[wordIn]
#                        invalidTexts.remove(wordIn)
            else:
            #    // SaddleBrown:
            #    // http://www.w3schools.com/tags/ref_color_tryit.asp?hex=8B4513
                scalar = (139, 69, 19)
                for wordIn in wordsIn:
                #    // try to find out that is the original error
                    oldLog = "None";
                    if wordIn in invalidTexts:
                            oldLog = invalidTexts[wordIn].log
                    
            
                    textValidator = TextValidator( wordIn,scalar, False, "Rect view have to many invalid texts, the rest should be invalid too. Old log: \n\t" )
                    invalidTexts[wordIn]= textValidator
                    match = True

        return match
    