from Rules.RuleTextTooBigCompWords import RuleTextTooBigCompWords
from Rules.RuleVisionBoxHasSoManyInvalidTexts import RuleVisionBoxHasSoManyInvalidTexts
from Rules.RuleBaseOnNeighbour import RuleBaseOnNeighbour
from Rules.RuleAlignVertically import RuleAlignVertically
from Rules.RuleBigLotChildren import RuleBigLotChildren
from Rules.RuleBoxHasOneWordTooSmall import RuleBoxHasOneWordTooSmall
from Rules.RuleBoxHasWordTooSmall import RuleBoxHasWordTooSmall
from Rules.RuleCharacterDistance import RuleCharacterDistance
from Rules.RuleWordOnlyOneTinyChild import RuleWordOnlyOneTinyChild
from Rules.RuleAllSpace import RuleAllSpace
from Rules.RuleLowConfidenceAndBoundaryCheck import RuleLowConfidenceAndBoundaryCheck
from Rules.RuleNoChildren import RuleNoChildren
from Rules.RuleNoHeight import RuleNoHeight
from Rules.RuleNoWidth import RuleNoWidth
from Rules.RuleOutOfBound import RuleOutOfBound
from Rules.RuleSmallHorizontalShape import RuleSmallHorizontalShape
from Rules.RuleSmallVericalShape import RuleSmallVericalShape
from Rules.RuleValidByList import RuleValidByList
from Utils import Environment
from Utils import Logger


class RuleManager:
    
    def __init__(self, dipCalculator, ocrTesseractOCR, matLog, ocrTextWrappers, views):
        self.mOCRRules = []
        self.mVisionRules = []
        self.mDipCalculator = dipCalculator
        self.mViews = views
        self.mOcrTesseractOCR = ocrTesseractOCR
        self.mMatLog = matLog
        self.mOcrTextWrappers = ocrTextWrappers
        self.initOCRRules()
        self.initVisionRules()


    def initVisionRules(self):
       self.mVisionRules.append( RuleTextTooBigCompWords(self.mDipCalculator, self.mOcrTesseractOCR, self.mMatLog, self.mOcrTextWrappers, self.mViews))
       self.mVisionRules.append( RuleVisionBoxHasSoManyInvalidTexts(self.mDipCalculator, self.mOcrTesseractOCR, self.mMatLog, self.mOcrTextWrappers, self.mViews))
       self.mVisionRules.append( RuleBaseOnNeighbour(self.mDipCalculator, self.mOcrTesseractOCR, self.mMatLog, self.mOcrTextWrappers, self.mViews))
    

    def initOCRRules(self):

        self.mOCRRules.append(RuleLowConfidenceAndBoundaryCheck(self.mDipCalculator, self.mOcrTesseractOCR, self.mMatLog, self.mOcrTextWrappers, self.mViews))
        self.mOCRRules.append(RuleValidByList(self.mDipCalculator, self.mOcrTesseractOCR, self.mMatLog, self.mOcrTextWrappers, self.mViews))
        self.mOCRRules.append(RuleNoWidth(self.mDipCalculator, self.mOcrTesseractOCR, self.mMatLog, self.mOcrTextWrappers, self.mViews))
        self.mOCRRules.append(RuleNoHeight(self.mDipCalculator, self.mOcrTesseractOCR, self.mMatLog, self.mOcrTextWrappers, self.mViews))
        self.mOCRRules.append(RuleOutOfBound(self.mDipCalculator, self.mOcrTesseractOCR,self.mMatLog, self.mOcrTextWrappers, self.mViews))
        self.mOCRRules.append(RuleSmallVericalShape(self.mDipCalculator, self.mOcrTesseractOCR, self.mMatLog, self.mOcrTextWrappers, self.mViews))
        self.mOCRRules.append(RuleSmallHorizontalShape(self.mDipCalculator, self.mOcrTesseractOCR, self.mMatLog, self.mOcrTextWrappers, self.mViews))
        self.mOCRRules.append(RuleAllSpace(self.mDipCalculator, self.mOcrTesseractOCR, self.mMatLog, self.mOcrTextWrappers, self.mViews))
        self.mOCRRules.append(RuleAlignVertically(self.mDipCalculator, self.mOcrTesseractOCR, self.mMatLog, self.mOcrTextWrappers, self.mViews))
        self.mOCRRules.append(RuleCharacterDistance(self.mDipCalculator, self.mOcrTesseractOCR, self.mMatLog, self.mOcrTextWrappers, self.mViews))
        self.mOCRRules.append(RuleWordOnlyOneTinyChild(self.mDipCalculator, self.mOcrTesseractOCR, self.mMatLog, self.mOcrTextWrappers, self.mViews))
        self.mOCRRules.append(RuleBigLotChildren(self.mDipCalculator, self.mOcrTesseractOCR, self.mMatLog, self.mOcrTextWrappers, self.mViews))
        self.mOCRRules.append(RuleBoxHasWordTooSmall(self.mDipCalculator, self.mOcrTesseractOCR, self.mMatLog, self.mOcrTextWrappers, self.mViews))
        self.mOCRRules.append(RuleBoxHasOneWordTooSmall(self.mDipCalculator, self.mOcrTesseractOCR, self.mMatLog, self.mOcrTextWrappers, self.mViews))
        self.mOCRRules.append(RuleNoChildren(self.mDipCalculator, self.mOcrTesseractOCR, self.mMatLog, self.mOcrTextWrappers, self.mViews))


    def acceptOCRRules(self,ocr):
        firstTextValidator = None
        for rule in self.mOCRRules:
            textValidator = rule.accept(ocr)
            if textValidator != None and not textValidator.valid :
                firstTextValidator = textValidator
#                print(textValidator.log)
                break
        
        for rule in self.mOCRRules:
            textValidator = rule.accept(ocr)
            if textValidator != None and not textValidator.valid:
                Logger.append(Logger.RULE_INFO_LOG,"\t" + type(rule).__name__)
        
        return firstTextValidator
    

    def acceptVisionRules(self,invalidTexts, acceptedOcrTextWrappers):
        for rule in self.mVisionRules:
            match = rule.run(invalidTexts, acceptedOcrTextWrappers)
            if match:
                Logger.append(Logger.RULE_INFO_LOG, "\t" +  type(rule).__name__)
        