from Rules.ASingleRule import ASingleRule
from Utils import ColorUtil
from RectUtils import RectUtil
from Rules.TextValidator import TextValidator
from Utils import Constants
from Utils import GroupUtil
from Utils import TextUtils
from string import printable


def containAllSpacesOrInvalidChars(text):
    if TextUtils.isEmpty(text):
        return True
    
                    
    asciiContain = all([ord(char) < 33 or ord(char)>126 for char in text])
    invalidChar = len([char for char in text if char not in printable]) != 0 
    allSpace = all([" " == c or '\n'== c for c in text])
    return not(allSpace or invalidChar  or asciiContain)
 

class RuleAllSpace(ASingleRule):
    
    def __init__(self,dipCalculator, tesseractOCR, matLog, ocrs, views):
            super().__init__(dipCalculator, tesseractOCR, matLog, ocrs, views)

#    @Override
    def accept(self,ocr):      
        if containAllSpacesOrInvalidChars(ocr.text):
            return None   
        
        
#        return None
#        
        tv = TextValidator(ocr, ( 130, 238, 255), False, "There is not text. it is all spaces")
        return tv

    
#     Contain: all spaces, all invisible chars, or all non-ascii chars
#     * 
#     * @param text
#     * @return
#     */

