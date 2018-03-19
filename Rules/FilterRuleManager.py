from Rules.RuleManager import RuleManager
from Utils import Environment

class FilterRuleManager(RuleManager):
    mIndex = 0 
    def __init__(self, dipCalculator, ocrTesseractOCR, matLog, ocrTextWrappers, views):
        super().__init__(dipCalculator, ocrTesseractOCR, matLog, ocrTextWrappers, views)


#    @Override
    def initRules(self):
        self.initOCRRules()
        self.initVisionRules()
        self.mIndex = int( Environment.getValue(Environment.KEY_RULE_FILTER_INDEX))
        if (self.mIndex == None or self.mIndex < 0):
            return
        
        # mIndex = 0, 1, 2
        if self.mIndex < len(self.mVisionRules):
            self.mVisionRules.remove(int (self.mIndex))
#            System.out.println("The rule is removed (vision), total: "
#                    + (mVisionRules.size()) + ": " + mIndex);
#            // mIndex = 3, 4, 5 ...
        elif self.mIndex - len(self.mVisionRules.size()) < len(self.mOCRRules):

           self.mOCRRules.remove(self.mIndex - len(self.mVisionRules))
#            System.out.println("The rule is removed (ocr) total: "
#                    + (mOCRRules.size()) + ": "
#                    + (mIndex - mVisionRules.size()));
