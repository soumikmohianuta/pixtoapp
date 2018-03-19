from RectUtils import RectUtil

def areChildrenIsTooSmall(dipCalculator, view) :
    if len(view.mChildren) == 0 :
        return False
        
    for cView in view.mChildren :
        if not dipCalculator.isViewToBeIgnore(cView.width,cView.height) :
            return False
            
        return True

def hasChildren(ocrTextWrapper, ocrWrappers):
        
    
        # keep word did not have children
    hasChildren = False
    for otherOcrTextWrapper in ocrWrappers :
        if otherOcrTextWrapper != ocrTextWrapper  and RectUtil.contains(ocrTextWrapper.rect, otherOcrTextWrapper.rect):
            return True
            
    return hasChildren
def hasParent(ocrTextWrapper, ocrWrappers):
        
    
        # keep word did not have children
    hasParent = False
    for otherOcrTextWrapper in ocrWrappers :
        if otherOcrTextWrapper != ocrTextWrapper  and RectUtil.contains(otherOcrTextWrapper.rect, ocrTextWrapper.rect):
            return True
            
    return hasParent


def getTextAndRemove(viewBound, blocks) :
    childTexts = []
    for ocrTextWrapper in blocks:
        bound = ocrTextWrapper.bound()
        if (RectUtil.contains(viewBound, bound)) :
            childTexts.append(ocrTextWrapper)
        
    blocks = [x for x in blocks if x not in childTexts]
    return childTexts
