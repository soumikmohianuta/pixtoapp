# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 22:24:31 2017

@author: soumi
"""

import copy
from Utils.ColorUtil import CColor, ColorWrapper
from RectUtils import RectUtil
from RectUtils.Rect import Rect
from Utils import ColorUtil
from Utils import ImageUtil
from Rules.FilterRuleManager import *
import cv2
from functools import cmp_to_key
from ocr import OCRTextWrapper
from Utils import Constants
from Rules import RuleAllSpace
from ocr.TextInfo import TextInfo



    
class TextProcessor :
    isDebugMode = False

    def __init__(self, image,img_gray, biMapViewRect, ocr, dipCalculator) :
        self.mRgbaImage = image
        self.grayImage = img_gray
        self.mBiMapViewRect = biMapViewRect
        self.mOcr = ocr
        self.mDipCalculator = dipCalculator
        
        values = set([biMapViewRect[k] for k in biMapViewRect])
        self.mViewBounds = []
        self.mViewBounds.extend(values)
        RectUtil.sortLeftRightTopBottom(self.mViewBounds)
        self.mViews = [k for k in biMapViewRect]
        self.isDebugMode =True
        
    

    def processText(self, color):
        ocrTextWrappers = self.mOcr.mOcrTextWrappers
        width = 0
        height = 0
        copyImage = copy.deepcopy(self.mRgbaImage)
        
        if len(copyImage.shape) == 2 :
            height, width = copyImage.shape
        else:
            height, width,channels = copyImage.shape
        
         
#        ocrOnlyProcessingStepImage = copy.deepcopy(self.mRgbaImage)

        
        acceptedOcrTextWrappers = []
        ruleManager = FilterRuleManager(self.mDipCalculator, self.mOcr,self.mRgbaImage,ocrTextWrappers, self.mViews)
        invalidTexts = {}
      
        for ocrTextWrapper in ocrTextWrappers:
            
            textValidator = ruleManager.acceptOCRRules(ocrTextWrapper)
            if textValidator != None and not textValidator.valid:
                invalidTexts[ocrTextWrapper]= textValidator

#                if(self.isDebugMode) :
#                    cv2.rectangle(ocrOnlyProcessingStepImage, ocrTextWrapper.bound().tl(), ocrTextWrapper.bound().br(),   CColor.Red, 2)
            else :
                acceptedOcrTextWrappers.append(ocrTextWrapper)
#                if(self.isDebugMode) :
#                    cv2.rectangle(ocrOnlyProcessingStepImage, ocrTextWrapper.bound().tl(), ocrTextWrapper.bound().br(), CColor.Blue, 2)
                
        ruleManager.acceptVisionRules(invalidTexts, acceptedOcrTextWrappers)

      
        validTexts = []
        validTexts.extend(acceptedOcrTextWrappers) 
        validTexts = [x for x in validTexts if x not in invalidTexts]

            

#        ImageUtil.drawWindow( "basic Text",ocrOnlyProcessingStepImage)

        ocrLineWrappers = self.mOcr.mOcrLineWrappers
        # sort top bottom
        copyLines = []
        copyLines.extend(ocrLineWrappers)
        
        copyLines.sort(key=cmp_to_key(RectUtil.getTopBottomComparator))

        validLines = []
        addedWords = []
        for ocrLineWrapper in copyLines:
            words = []
            line = OCRTextWrapper.OCRTextWrapper(ocrLineWrapper);
            for ocrWordWrapper in validTexts:
                if (ocrWordWrapper not in addedWords) and RectUtil.contains(ocrLineWrapper.bound(),ocrWordWrapper.bound()):
                    words.append(ocrWordWrapper)
                    addedWords.append(ocrWordWrapper)
            # Some line contain 2 words which are vertically alignment
            if len(words) > 0 :
                notHorizontalAlignmentWords = self.getNotHorizontalAlignmentWords(words)
                if len(notHorizontalAlignmentWords) == 0:
                    validLines.append(line)
                    
                    words.sort(key=cmp_to_key(RectUtil.getLeftRightComparator))
                    line.words = words
                else :
                    # Take it from addedWords. This will help these words be
                    # added to other lines, since this line is invalid
                    addedWords = [x for x in addedWords if x not in notHorizontalAlignmentWords]
                    # remove bad guy
                    words = [x for x in words if x not in notHorizontalAlignmentWords]
                    validLines.append(line);
                    words.sort(key=cmp_to_key(RectUtil.getLeftRightComparator))
                    line.words = words
        # We still want to add word as line when it did not get add to any
        # lines

        remainWords =[]
        remainWords.extend(validTexts)
        remainWords = [x for x in remainWords if x not in addedWords]


        for word in remainWords:
            # System.out.println("Remain words: " + word);
            if (word.confidence < 90 and not self.mOcr.isValidTextUsingBoundaryCheck(word)) :
                continue
            
            line = OCRTextWrapper.OCRTextWrapper(word)
            words = []
            words.append(word)
            line.words = words
            validLines.append(line)
            
        validLines.sort(key=cmp_to_key(RectUtil.getTopBottomComparator))
#        self.log("ValidLines", validLines, CColor.Red)

        for ocrLineWrapper in validLines:
            rect = ocrLineWrapper.reCalculateBoundBaseOnWordList()
            if (rect == None) :
                print("Error with line, there is no more text: "+ ocrLineWrapper.text)
                #System.out.println("Error with line, there is no more text: "+ ocrLineWrapper.getText());
            else :
                text = self.mOcr.getText(rect)
                ocrLineWrapper.text = text
                ocrLineWrapper.rect = rect
        
        # word is sort from left to right
            
        for ocrLineWrapper in validLines:
            blocks = [[]]
            words = ocrLineWrapper.words
            currentBlock = []
            if len(words) > 0 :
                currentBlock.append(words[0])
                for i in range(len(words)-1) :
                    nextWord = words[i + 1]
                    currentWord = words[i]
                    xDistance = nextWord.x - (currentWord.x+currentWord.width)
                    xDistanceThreshold = int (Constants.WORD_SPACE_THRESHOLD_BASE_ON_HEIGHT * float(min(currentWord.bound().height,nextWord.bound().height)))
                    fontDiff = abs(currentWord.fontSize - nextWord.fontSize)
#                    if (xDistance <= xDistanceThreshold and fontDiff <= 1) :
                    if (xDistance <= xDistanceThreshold ):
                        currentBlock.append(nextWord);
                    else :
                        blocks.append(currentBlock)
                        currentBlock = []
                        currentBlock.append(nextWord)
                    
                if currentBlock not in blocks:
                    blocks.append(currentBlock);
                
            ocrLineWrapper.blocks= blocks

        
#        logImageWithValidTextBox = copy.deepcopy(self.mRgbaImage)
#        ImageUtil.fillRect(logImageWithValidTextBox, Rect(0, 0, width,height), ColorUtil.toInt(255, 255, 255, 255))

        blocksInline = []

        for lineOCR in validLines:
            blocks = lineOCR.blocks
            for listWord in blocks:
                if len(listWord) > 0 :
                    firstWord = listWord[0]
                    rect = RectUtil.findBoundRectangle(listWord)
#                    cv2.rectangle(logImageWithValidTextBox, rect.tl(),
#							rect.br(), CColor.Red, 2);
                    block = OCRTextWrapper.OCRTextWrapper(firstWord)
                    block.words =  listWord
                    block.width = rect.width
                    block.height = rect.height
                    block.rect =  rect
                    lineText = ""
#                    rect = Rect(rect.x -2, rect.y-2, rect.width +2, rect.height +2)
#                    if len(listWord) == 1 :
#                        lineText = listWord[0].text
#                    else :
#                        # override text
                    lineText = self.mOcr.getLineText(rect)
                    block.text = lineText
                    # will ignore this block if it contains only invisible
                    # chars
#                    blocksInline.append(block)
                    if ( RuleAllSpace.containAllSpacesOrInvalidChars(lineText)) :
                       blocksInline.append(block)
        colListmap =  {}
        for blocks in blocksInline: 
            colListmap[ColorWrapper(ColorUtil.cColortoInt(CColor.Red), 1)] =  blocks
                     
                        
        
#        ImageUtil.logDrawMap(colListmap, "Text Block", self.mRgbaImage)

        textInfo = TextInfo();
        textInfo.lines = validLines
        textInfo.blocksInALine = blocksInline
        textInfo.blocksInALine.sort(key=cmp_to_key(RectUtil.getTopBottomComparator))
        
        #mSreenshotProcessor.getTimerManager().log(Constants.TIMER_ID_SPLIT_LINE_INTO_TEXT_BOXES);
        return textInfo
    

    def getNotHorizontalAlignmentWords(self, words) :
        if len(words) <= 1 :
            return []

        invalidWords = []
        textWrappers = []
        textWrappers.extend(words)
        first = textWrappers[0].bound()
        for i in range(1,len(words)):
            # Assume that the first item is correct
            current = textWrappers[i].bound();
            if (first.y + first.height <= current.y) :
                invalidWords.append(textWrappers[i])

        return invalidWords
    
    def validateWordWithAllViews(self, tv, ocrTextWrapper) :
        ocrBound = ocrTextWrapper.bound();
        for view in self.mViews :
            # woa this word is big and have a lot of children, not good
            # this may okay with url or special texts
            if (RectUtil.contains(ocrBound, view.bound())and len(view.getChildren()) > 0) :
                tv.scalar = ColorUtil.getScalar(CColor.Cyan)
                tv.valid = False
                tv.log = "This word is big and have a lot of children";
                return

            # the box may has the word is too small compare with the word
            # itself.
            # If the word a children view which only have on child, we need
            # to verify if:
            # (1) This child view did not intersect with any other views
            # (2) This child view really small compare to the word bound
            if RectUtil.contains(ocrBound, view.bound()) and len(view.getChildren()) == 0 :
                # make sure this view did not intersect with other view,
                # include is accepted in this case
                hasIntersection = False
                for otherView in self.mViews:
                    if otherView != view and RectUtil.intersectsNotInclude(ocrBound,otherView.bound()) :
                        hasIntersection = True
                        break                    
                
                if (not hasIntersection) :
                    if (RectUtil.dimesionSmallerThan(view, ocrTextWrapper, 0.8)) :
                        # this is wrong, ignore this word
                        tv.scalar = CColor.Black
                        tv.valid = False
                        tv.log = "The box may has the word is too small compare with the word itself"
                        return
                 

            # same here: the box may has the word is too big compare to the
            # word itself we also make sure that this view may also have
            # other view but it so tiny will be ignore when layout
            # itself and there is only one word in here
            if (self.areChildrenIsTooSmall(self.mDipCalculator, view) and RectUtil.contains(view.bound(), ocrBound)) :
                if (RectUtil.dimesionSmallerThan(ocrTextWrapper, view, 0.8)) :
                    # this is wrong, ignore this word
                    tv.scalar = CColor.Pink
                    tv.valid = False
                    tv.log = "The box may has the word is too big compare to the word, and there is only one word in here. This view may also have other view but it so tiny"
                    return
                

    

    def log(self,id, ocrTextWrappers, color):
        
        width = 0
        height = 0
        copyImage = copy.deepcopy(self.mRgbaImage)
        
        if len(copyImage.shape) == 2 :
            height, width = copyImage.shape
        else:
            height, width,channels = copyImage.shape
        
        for ocrTextWrapper in ocrTextWrappers :
            cv2.rectangle(copyImage, ocrTextWrapper.bound().tl(),ocrTextWrapper.bound().br(), color, 2)
        ImageUtil.drawWindow(id, copyImage)

#        ImageUtil.log(mOutLogFolder, self.mFileName, suffix, copyImage, self.mSreenshotProcessor.getImageChangeListener());
    
    # private void addTextToView(RectView rectView) :
    # List<RectView> children = rectView.getChildren();
    # for (RectView rawView : children) :
    # addTextToView(rawView);
    # }
    # List<OCRTextWrapper> texts =
    # mOcr.getTextWithLocationAndRemove(rectView.getBound(),
    # TesseractOCR.DEFAULT_CONFIDENT_THRESHOLD);
    # rectView.setTextWithLocations(texts);
    # }

