from Rules.AVisionRule import AVisionRule
from Utils import ColorUtil
from RectUtils import RectUtil
from Rules.TextValidator import TextValidator
from Utils import Constants
from Utils import GroupUtil
from Utils import TextUtils


class RuleBaseOnNeighbour(AVisionRule):

    def __init__ (self,dipCalculator, tesseractOCR, matLog, ocrs, views):
        super().__init__(dipCalculator, tesseractOCR, matLog, ocrs, views)
        self.mDefaultAlignThreshold = self.mDipCalculator.dipToWidthPx(2.25)

#    @Override
    def run(self, invalidTexts, acceptedOcrTextWrappers):

        match = False
        # base on its drawable neighbours to decide if this is valid text or
        # not.
        moreInValidTexts = self.removeInvalidTextBaseOnNeighbours(acceptedOcrTextWrappers, invalidTexts);
        if len(moreInValidTexts) > 0 :
            scalar = (50, 205, 50)
            for textWrapper in moreInValidTexts:
                # LimeGreen:
                # http:#www.w3schools.com/tags/ref_color_tryit.asp?hex=32CD32
                textValidator = TextValidator(textWrapper, scalar, False,"Invalid text because of neighbours");
                invalidTexts[textWrapper]= textValidator
                match = True
            
        return match
    
    def sameGroup(self,element1, element2):
        return RectUtil.equal(element1, element2)

    def removeInvalidTextBaseOnNeighbours(self,acceptedOcrTextWrappers, invalidTexts):
        validTexts = []
        validTexts.extend(acceptedOcrTextWrappers)
        
        for invText in invalidTexts:
            if invText in validTexts:
                validTexts.remove(invText)
    

        moreInvalidText = []

        groups = GroupUtil.group(self.mViews, self.sameGroup);
        for group in groups:
            if len(group) >= Constants.TEXT_TO_BECOME_IMAGE_MIN_ACCEPTABLE_LIST_SIZE:
                alignmentType = RectUtil.getAlignmentType(group, self.mDefaultAlignThreshold)
                if alignmentType != RectUtil.ALIGNMENT_UNKNOWN:
                    skipGroup = False
                    # if all text exactly the same and have invalid text, we
                    # kill them all.
                    sameText = "";
                    inValidTextsInGroup = set()
                    for i in range(len(group)):
                        rectView = group[i]
                        texts = RectUtil.contain(rectView, validTexts)
                        # We only test views have one text
                        # And not "intersect not include" with other valid text
                        if len(texts) == 1 and RectUtil.countIntersectNotIncludeRect(rectView, validTexts) == 0:
                            # If the confident is acceptable but boundary is
                            # wrong, only one character is accept here
                            text = texts[0].text
# //TODO                            if self.mTesseractOCR.validWord(text) or len(text) > 1:
                            if len(text) > 1:
                                skipGroup = True
                                break
                            
                            if i == 0: 
                                sameText = text
                            elif not sameText == text:
                                skipGroup = True
                                break
                            
                            # if not add to group
                            inValidTextsInGroup.add(texts[0]);
                            # System.out.println("Added: " + texts);
                        else:
                            skipGroup = True
                            break
                        

                    if not skipGroup:
                        if len(inValidTextsInGroup) == len(group):
                            stillInvalid = False
                            for textWrapper in inValidTextsInGroup:
                                if textWrapper.confidence < Constants.TEXT_TO_BECOME_IMAGE_IN_LIST_THRESHOLD  or not self.mTesseractOCR.validWord(textWrapper.getText()) :
                                    stillInvalid = True
                                    break
                                
                            if stillInvalid:
                                moreInvalidText.extend(inValidTextsInGroup);
                                continue
                            
                        # We will check other rules after this
                        skipGroup = True

                    mapCountTexts = {}

                    if skipGroup:
                        for rectView in group:
                            texts = RectUtil.contain(rectView, validTexts);
                            # We only test views have one text
                            # And not "intersect not include" with other valid
                            # text
                            if len(texts) >= 2 or RectUtil.countIntersectNotIncludeRect(rectView, validTexts) > 0:
                                skipGroup = True
                                break
                            else:
                                mapCountTexts[rectView] = texts
                            
                        
                    

                    if skipGroup:
                        continue
                    
                    else:
                        countEmptyView = 0;
                        uniqueInvalidRectView = None
                        for rectView in group:
                            if len(mapCountTexts.get(rectView)) == 0:
                                countEmptyView=countEmptyView+1
                            else:
                                uniqueInvalidRectView = rectView
                        if len(group) == countEmptyView + 1 and uniqueInvalidRectView != None :
                            moreInvalidText.extend(mapCountTexts.get(uniqueInvalidRectView))

        return moreInvalidText

