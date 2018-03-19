
from ocr import OCRTextWrapper
from RectUtils import RectUtil
from RectUtils.Rect import Rect
from RectUtils.Point import Point
from PIL import Image
from Utils import Constants
from Utils import TextUtils
import os

from tesserocr import PyTessBaseAPI, RIL, OEM, PSM
from PIL import ImageFont

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
FONT_FOLDER = os.path.join(APP_ROOT, 'fonts/')
def increaseHeight(height):
        return Constants.TEXT_BOX_AND_TEXT_HEIGHT_RATIO * height * Constants.TEXT_BOX_AND_TEXT_HEIGHT_RATIO 
	

class TesseractOCR :

	#private static   TESSERACT_ENGINE_MODE = TessAPI1.TessOcrEngineMode.OEM_DEFAULT

	#
	 # bpp - bits per pixel, represents the bit depth of the image, with 1 for
	 # binary bitmap, 8 for gray, and 24 for color RGB.
	 #
    BBP = 8
    DEFAULT_CONFIDENT_THRESHOLD = 60.0
    MINIMUM_DESKEW_THRESHOLD = 0.05

    def __init__(self,rgbaImage, dipCalculator,language):
         self.mRgbaImage = rgbaImage
         self.mDipCalculator = dipCalculator
         self.mHandle = PyTessBaseAPI()

         self.mOcrTextWrappers = []
         self.mOcrBlockWrappers = []
         self.mOcrLineWrappers = []
         self.raWrappers = []
#         self.mLanguage = language

         self.mBufferedImageRgbaImage = Image.fromarray(self.mRgbaImage)
         self.initOCR()
    def baseInit( self,iteratorLevel):
        width = 0
        height = 0
        channels= 1
        
        if len(self.mRgbaImage.shape) == 2 :
            height, width = self.mRgbaImage.shape
        else:
            height, width,channels = self.mRgbaImage.shape
            
        return self.baseInitIter( self.mRgbaImage,Rect(0, 0, width, height),channels, iteratorLevel)
	

    def baseInitIter(self,imageMat, rect,channels, iteratorLevel):
        listdata = []
        parentX = rect.x
        parentY = rect.y
#        subMat = imageMat[rect.y:rect.y+rect.height, rect.x:rect.width+rect.x]
#
#        if(channels != 1):  
#            subMat = imageMat[rect.y:rect.y+rect.height, rect.x:rect.width+rect.x, 0:channels]
            
        #tessAPI = PyTessBaseAPI()
        #Convert to PIL image 
        imgPIL = Image.fromarray(imageMat)
        self.mHandle.SetImage(imgPIL)
        boxes = self.mHandle.GetComponentImages(iteratorLevel, True)

        
        for i, (im, box, _, _) in enumerate(boxes):
            
            wrapper = OCRTextWrapper.OCRTextWrapper()
            self.mHandle.SetRectangle(box['x'], box['y'], box['w'], box['h'])
            ocrResult = self.mHandle.GetUTF8Text()
            wrapper.text= ocrResult
            conf = self.mHandle.MeanTextConf()
            wrapper.confidence= conf
            self.mHandle.Recognize()
            iterator = self.mHandle.GetIterator()
            fontAttribute = iterator.WordFontAttributes()
            wrapper.x = box['x'] + parentX
            wrapper.y = box['y'] + parentY
            wrapper.width = box['w']
            wrapper.height = box['h']
            wrapper.rect = Rect(wrapper.x, wrapper.y, wrapper.width, wrapper.height)
#            print(box)
#        
            if(fontAttribute != None):
                wrapper.fontName = fontAttribute['font_name']
                wrapper.bold = fontAttribute['bold']
                wrapper.italic = fontAttribute['italic'] 
                wrapper.underlined = fontAttribute['underlined']
                wrapper.monospace = fontAttribute['monospace']
                wrapper.serif = fontAttribute['serif']
                wrapper.smallcaps = fontAttribute['smallcaps']
                wrapper.fontSize = fontAttribute['pointsize']
                wrapper.fontId = fontAttribute['font_id']
            
            listdata.append(wrapper)
            
            
        return listdata
	
    def getBlockWithLocation(self, rect) :
        wrappers = []
        for ocrTextWrapper in self.mOcrBlockWrappers :
            bound = ocrTextWrapper.rect
            if (RectUtil.contains(rect, bound)) :
                wrappers.append(OCRTextWrapper.OCRTextWrapper(ocrTextWrapper))
            
        return wrappers
        
    def getImage(self, rect):
        x2 = rect.x + rect.width
        y2 = rect.y + rect.height
        mat = self.mRgbaImage[rect.y:y2, rect.x:x2]
        return Image.fromarray(mat)
        
        
    def getText(self,rect):
        try :
            self.mHandle.SetImage(self.mBufferedImageRgbaImage)
            self.mHandle.SetRectangle(rect.x, rect.y, rect.width, rect.height)
            text = self.mHandle.GetUTF8Text()
            return text
        except Exception as error:
             print('Caught this error: ' + repr(error))
             
        return ""
    
    def getLineText(self,rect):
        try :
            self.mHandle.SetImage(self.mBufferedImageRgbaImage)
            self.mHandle.SetRectangle(rect.x, rect.y, rect.width, rect.height)
            text = self.mHandle.GetUTF8Text()
            if (TextUtils.isEmpty(text)) :
                self.mHandle = PyTessBaseAPI(psm=PSM.SINGLE_LINE)
                self.mHandle.SetImage(self.mBufferedImageRgbaImage)
                self.mHandle.SetRectangle(rect.x, rect.y, rect.width, rect.height)
                text = self.mHandle.GetUTF8Text()
                if (TextUtils.isEmpty(text)) :
                    self.mHandle.SetImage(self.getImage(rect))
                    text = self.mHandle.GetUTF8Text()
                    
                self.mHandle = PyTessBaseAPI(psm=PSM.AUTO)
            return text
        except Exception as error:
             print('Caught this error: ' + repr(error))
             
        return ""
    
    def getRectWordForLowConfidence(self,ocr):
        try :
            rect = ocr.bound()
            self.mHandle = PyTessBaseAPI(psm=PSM.SINGLE_WORD)
            self.mHandle.SetImage(self.mBufferedImageRgbaImage)
            self.mHandle.SetRectangle(rect.x, rect.y, rect.width, rect.height)
            ocr.text = self.mHandle.GetUTF8Text()
            ocr.confidence = self.mHandle.MeanTextConf()
            if(ocr.confidence <= Constants.TEXT_CONFIDENT_THRESHOLD):
                self.mHandle.SetImage(self.getImage(rect))
                ocr.text = self.mHandle.GetUTF8Text()
                ocr.confidence = self.mHandle.MeanTextConf()
            if(ocr.confidence <= Constants.TEXT_CONFIDENT_THRESHOLD):
                return False
            self.mHandle.Recognize()
            iterator = self.mHandle.GetIterator()    
            fontAttribute = iterator.WordFontAttributes()      
            if(fontAttribute != None):
                ocr.fontName = fontAttribute['font_name']
                ocr.bold = fontAttribute['bold']
                ocr.italic = fontAttribute['italic'] 
                ocr.underlined = fontAttribute['underlined']
                ocr.monospace = fontAttribute['monospace']
                ocr.serif = fontAttribute['serif']
                ocr.smallcaps = fontAttribute['smallcaps']
                ocr.fontSize = fontAttribute['pointsize']
                ocr.fontId = fontAttribute['font_id']
#                ocr.fontsize = self.getPreferenceFontSize(ocr)

            self.mHandle = PyTessBaseAPI(psm=PSM.AUTO)
            return True
        except Exception as error:
             print('Caught this error: ' + repr(error))
             
        return False        

    def getWordsIn(self, rect) :
        wrappers = []
        for ocrTextWrapper in self.mOcrTextWrappers:
            bound = ocrTextWrapper.bound()
            if (RectUtil.contains(rect, bound)) :
                wrappers.append(OCRTextWrapper.OCRTextWrapper(ocrTextWrapper))
        
        return wrappers
	
    def initOCR(self):

#
        self.initText()

        
        self.initBlock()
#        self.initPara()
        self.initLine()
#	
    
    def initBlock(self):
        self.mOcrBlockWrappers = self.baseInit(RIL.BLOCK)
        
    
    def initLine(self):
        self.mOcrLineWrappers = self.baseInit(RIL.TEXTLINE)
        invalidLineWrappers = []
		# a line cannot contain another lines
        for ocrLine in self.mOcrLineWrappers:
            for otherOcrLine in self.mOcrLineWrappers:
                if (ocrLine != otherOcrLine and RectUtil.contains(ocrLine.bound(),
								otherOcrLine.bound())):
                    invalidLineWrappers.append(ocrLine)
        self.mOcrLineWrappers = [x for x in self.mOcrLineWrappers if x not in invalidLineWrappers]
	
    
    def initPara(self):
        self.mOcrParaWrappers = self.baseInit(RIL.PARA)
	
    
    def initText(self):
        self.mOcrTextWrappers = self.baseInit(RIL.WORD)
	
    def isOverlapText(self, rect,confident) :
        for ocrTextWrapper in self.mOcrTextWrappers:
            bound = ocrTextWrapper.bound()
            if (ocrTextWrapper.getConfidence() >= confident and RectUtil.intersects(rect, bound)) :
                return True
        return False
	
    
    def reset(self):
        self.mOcrTextWrappers = []
        self.mOcrLineWrappers = []
        self.initOCR()
	

#    def rotateImage(bi) :
#        iden = ImageDeskew(bi)
#        imageSkewAngle = iden.getSkewAngle() # determine skew angle
#        if imageSkewAngle > MINIMUM_DESKEW_THRESHOLD or imageSkewAngle < -MINIMUM_DESKEW_THRESHOLD :
#            bi = ImageHelper.rotateImage(bi, -imageSkewAngle) # deskew
#        return bi
	
    def  getPreferenceFontSize(self, ocrTextWrapper,parentHeight) :
        
#        TODO TODO
        fontName = ocrTextWrapper.fontName
        fontSize = ocrTextWrapper.fontSize

        height = ocrTextWrapper.height * Constants.TEXT_BOX_AND_TEXT_HEIGHT_RATIO

#        height = ocrTextWrapper.height
        textHeight = int(self.mDipCalculator.pxToHeightDip(min(parentHeight, height)))
#        font = QFont(fontName, fontSize)
        newFontSize = fontSize
        if (self.getTextHeightUsingFontMetrics(ocrTextWrapper, fontName, fontSize) == textHeight) :
            newFontSize = fontSize
        
        elif (self.getTextHeightUsingFontMetrics(ocrTextWrapper, fontName, fontSize) < textHeight) :
            while (self.getTextHeightUsingFontMetrics(ocrTextWrapper, fontName, fontSize) < textHeight):
                fontSize = fontSize + 1
            newFontSize = fontSize
        
        else :
            while (self.getTextHeightUsingFontMetrics(ocrTextWrapper, fontName, fontSize) > textHeight):
                fontSize = fontSize - 1
            
            newFontSize = fontSize
		
        return newFontSize
	

    def getTextHeightUsingFontMetrics(self, ocrTextWrapper, fontName, fontSize) :
#        class SIZE(ctypes.Structure):
#            _fields_ = [("cx", ctypes.c_long), ("cy", ctypes.c_long)]
#        hdc = ctypes.windll.user32.GetDC(0)
#        hfont = ctypes.windll.gdi32.CreateFontA(-fontSize, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, fontName)
#        hfont_old = ctypes.windll.gdi32.SelectObject(hdc, hfont)
#        size = SIZE(0, 0)
#        ctypes.windll.gdi32.GetTextExtentPoint32A(hdc, text, len(text), ctypes.byref(size))
#        ctypes.windll.gdi32.SelectObject(hdc, hfont_old)
#        ctypes.windll.gdi32.DeleteObject(hfont)
#        return size.cy 
        file = "fonts//"+fontName + ".ttf"

        font = ImageFont.truetype(file, fontSize)
        fontSize= font.getsize(ocrTextWrapper.text)
        return fontSize[1]
    
    def validCharacter(self,word) :
        return self.mHandle.IsValidCharacter(word)
        
        #Don't have this method return TessAPI1.TessBaseAPIIsValidWord(mHandle, word) != 0
#        return True
	
#TODO
#    def getTextHeightUsingTextLayout(self,ocrTextWrapper, font) :
#        frc = self.mGraphics.getFontRenderContext()
#        loc = Point(0, 0)
#        layout = TextLayout(ocrTextWrapper.text, font, frc)
#        layout.draw(self.mGraphics, float(loc.x, loc.y))
#        bounds = layout.getBounds()
#        height = bounds.getHeight()
#        return height
	

#    def isValidTextUsingConfidentAndBoundaryCheck(self, ocrTextWrapper) :
#        if (ocrTextWrapper.getConfidence() > Constants.TEXT_CONFIDENT_THRESHOLD + Constants.TEXT_CONFIDENT_THRESHOLD_SECONDARY_RANGE) :
#            return True
#        
#        elif (ocrTextWrapper.getConfidence() <= Constants.TEXT_CONFIDENT_THRESHOLD) :
#            return False
#        
#        return self.isValidTextUsingBoundaryCheck(ocrTextWrapper)
#	
#
        
    def getTextDimensions(self, text, fontName, fontSize):
        file = "fonts//"+fontName + ".ttf"
        font = ImageFont.truetype(file, fontSize)
        fontSize= font.getsize(text)
        return fontSize

    def isValidTextUsingBoundaryCheck(self,ocrTextWrapper) :
		# confident between TextProcessor.TEXT_CONFIDENT_THRESHOLD and
		# TextProcessor.TEXT_CONFIDENT_THRESHOLD +
		# TextProcessor.TEXT_CONFIDENT_THRESHOLD_SECONDARY_RANGE
        if (TextUtils.isEmpty(ocrTextWrapper.text)) :
			# We cannot calculate width of empty text
            return True
#        return True

		
#        frc = mGraphics.getFontRenderContext()
#        font = QFont(ocrTextWrapper.fontName,ocrTextWrapper.fontSize)
#        loc = Point(0, 0)
#        layout = TextLayout(ocrTextWrapper.text,font, frc)
#        layout.draw(mGraphics,  loc.getX(), loc.getY())
#        bound = layout.getBounds()
        width, height = self.getTextDimensions(ocrTextWrapper.text,ocrTextWrapper.fontName,ocrTextWrapper.fontSize )
        
        fontRatio = float(height / width)
        boundRatio = float (ocrTextWrapper.height/ ocrTextWrapper.width)
        fontArea = self.mDipCalculator.dipToHeightPx(height)* self.mDipCalculator.dipToWidthPx(width)
        boundArea = float( ocrTextWrapper.width* ocrTextWrapper.height)
#
		# the different between dimensions of the text should be smaller than
		# 10% of the max dimension.
		# System.out.prln(" Ratio: " + fontRatio + ", " + boundRatio + ", "
		# + Math.abs(boundRatio - fontRatio)
		# / Math.max(boundRatio, fontRatio) + "," + fontArea + ", "
		# + boundArea + ", " + Math.min(fontArea, boundArea)
		# / Math.max(fontArea, boundArea))

		# It the bound is square, it less likely that this text is correct
		# TODO: This rule may not need it
#        if (float(min(ocrTextWrapper.getWidth(),ocrTextWrapper.getHeight()) / max( ocrTextWrapper.getWidth(),
#						ocrTextWrapper.getHeight())) > 0.95) :
#			# if drawing text cannot create square, sorry -> invalid
#            if (float(min(width, height) / max(width, height)) <= 0.95 and not validWord(ocrTextWrapper.text)) :
#                return False
#			
#		
#
        
#        print(self.mDipCalculator.dipToWidthPx(width), self.mDipCalculator.dipToHeightPx(height))
#        print( ocrTextWrapper.width, ocrTextWrapper.height)
        dimension = abs(boundRatio - fontRatio)/max(boundRatio, fontRatio)
#        print(dimension)

        dimensionCheck = abs(boundRatio - fontRatio)/max(boundRatio, fontRatio) <= Constants.TEXT_CONFIDENT_ACCEPTANCE_DIMENSION_RATIO_DIFFERENCE_THRESHOLD

        areaCheckVal = min(fontArea, boundArea)/ max(fontArea, boundArea) 
#        print(areaCheckVal)
#        print(ocrTextWrapper.text)
        areaCheck = min(fontArea, boundArea)/ max(fontArea, boundArea) >= Constants.TEXT_AREA_ACCEPTANCE_DIFFERENCE_THRESHOLD


        return dimensionCheck and areaCheck
	



    def destroy(self) :
        self.mHandle.End
#        TessAPI1.TessBaseAPIDelete(mHandle)
	



	

