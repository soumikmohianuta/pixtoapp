from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from Utils import Constants
import xml.etree.ElementTree as ET
from Utils import ColorUtil 
from Utils.ColorUtil import CColor
from Utils import TextUtils

USING_RANDOM = False


#def createDocument() :
#    document = dom.
#    return document
	

def createRoot(dipCalculator,   name, rectView, colorWriter) :
    ET.register_namespace('android', "http://schemas.android.com/apk/res/android")
    element = Element(name)
    colorId = colorWriter.addResource(selectColorMode(rectView.mColor))
    element.set('xmlns:android', "http://schemas.android.com/apk/res/android")
    width = dipCalculator.pxToWidthDip(rectView.width) 
    height =  dipCalculator.pxToWidthDip(rectView.height)
    print("Just checking")
    print(width)
    print(height)
    print(rectView.width)
    print(rectView.height)
#    
    element.set( Constants.ATTRIBUTE_LAYOUT_WIDTH, str(dipCalculator.pxToWidthDip(rectView.width))+ Constants.UNIT_DIP)
    element.set(Constants.ATTRIBUTE_LAYOUT_HEIGHT, str(dipCalculator.pxToHeightDip(rectView.height))+ Constants.UNIT_DIP)
    element.set(Constants.ATTRIBUTE_BACKGROUND, getReferenceColorId(colorId))
    return element
	

def selectColorMode(color) :
    if(USING_RANDOM):
        return getRandomColor()
    else: 
        return toHtmlColor(color)
	

def getRandomColor():
    color = ColorUtil.alphaColortoInt( ColorUtil.randomColor())
    return toHtmlColor(color)
	

def	 toHtmlColor( color) :
		return '#%08X' %  int(0xFFFFFFFF & color)
    


def addMargin(dipCalculator, element, left,top) :
    element.set(Constants.ATTRIBUTE_LAYOUT_MARGIN_LEFT,  str(dipCalculator.pxToWidthDip(left)) + Constants.UNIT_DIP)
    element.set(Constants.ATTRIBUTE_LAYOUT_MARGIN_TOP, str(dipCalculator.pxToHeightDip(top)) + Constants.UNIT_DIP)
    
def addSize(dipCalculator, element, width, height) :
    if(type(width) == str ):
        element.set(Constants.ATTRIBUTE_LAYOUT_WIDTH, width)
    else:
        element.set(Constants.ATTRIBUTE_LAYOUT_WIDTH, str(dipCalculator.pxToWidthDip(width)) + Constants.UNIT_DIP)
    
    if(type(height) == str ):
        element.set(Constants.ATTRIBUTE_LAYOUT_HEIGHT, height)
    else:
        element.set(Constants.ATTRIBUTE_LAYOUT_HEIGHT, str(dipCalculator.pxToHeightDip(height)) + Constants.UNIT_DIP)

        
        
def addId(element, _id) :
    element.set(Constants.ATTRIBUTE_ID, "@+id/" + _id)
    
def addScaleType(element, scaleType) :
    element.set(Constants.ATTRIBUTE_SCALE_TYPE, str(scaleType))
	
def addBackgroundColor(element, color, colorWriter) :
    colorId = colorWriter.addResource(selectColorMode(color))
    element.set(Constants.ATTRIBUTE_BACKGROUND, getReferenceColorId(colorId))
	
def addTextColor(element, color, colorWriter) :
#    color = ColorUtil.cColortoInt(CColor.Black)
    colorId = colorWriter.addResource(selectColorMode(color))
    element.set(Constants.ATTRIBUTE_TEXT_COLOR, getReferenceColorId(colorId))
	
def	addBackroundImage(element, _id) :
    element.set(Constants.ATTRIBUTE_BACKGROUND, getReferenceDrawableId(_id))
	
	
def addGravity(element,  gravity) :
    element.set(Constants.ATTRIBUTE_GRAVITY, gravity)
	
	
def addLayoutGravity(element,  layoutGravity) :
    element.set(Constants.ATTRIBUTE_LAYOUT_GRAVITY, layoutGravity)

#def addElement(dipCalculator, parent,   name, rectView, marginLeft, marginTop,  _id, color):
#    child = SubElement(parent, name)
#    addMargin(dipCalculator, child, marginLeft, marginTop)
#    addSize(dipCalculator, child, rectView.widht, rectView.height)
#    addId(child, _id)
#    return child
    
    
#def addElement(dipCalculator, parent,   name,  rectView, marginLeft, marginTop,   _id, colorWriter) :
#		return addElement(dipCalculator, parent, name, rectView, marginLeft,
#				marginTop, id, colorWriter, rectView.getColor())
#	

def addElement(dipCalculator, parent, name, rectView, marginLeft, marginTop,   _id, colorWriter=None,  color = None) :
    
    element = SubElement(parent,name)
    addMargin(dipCalculator, element, marginLeft, marginTop)
    addSize(dipCalculator, element, rectView.width, rectView.height)
    if(colorWriter != None):
        if(color == None):
            color = rectView.mColor
        addBackgroundColor(element, color, colorWriter)
    addId(element, _id)
    return element
	


def writeDocumet(document, path):
    fh = open(path, "w")
    fh.write(document)
    fh.close()
	

def writeDocumentxml(document, path):
    tree = ET.ElementTree(document)
    tree.write(path)


#	
#
#	  writeDocument( Document document,   path)
#			throws IOException :
#		// lets write to a file
#		 XMLWriter writer = new XMLWriter(new FileWriter(path),
#				OutputFormat.createPrettyPr())
#		writer.write(document)
#		writer.close()
#	

def	 getReferenceResourceId(_id) :
		return "@" + Constants.VALUE_STRING_FILE_NAME + "/" + str(_id)
	

def	 getReferenceStyleId(_id) :
		return "@" + Constants.VALUE_STYLE_FILE_NAME + "/" + str(_id)
	

def	  getReferenceColorId(  _id) :
		return "@" + Constants.VALUE_COLOR_FILE_NAME + "/" + str(_id)
	

def	 getReferenceDrawableId( _id) :
    return "@" + Constants.VALUE_DRAWABLE_FILE_NAME + "/" + str(_id)
	

def	  addImageDrawable(element,  _id) :
    element.set("android:src", getReferenceDrawableId(_id))
	

def	  removeAttribute(element,  name) :
    if name in element.attrib:
        del element.attrib[name]
	
def getDipValue(element,  attributeName) :
    if attributeName in element.attrib:
        value = element.get(attributeName)
        if (not TextUtils.isEmpty(value) and value.endswith(Constants.UNIT_DIP)) :
            dValue = float(value[0:len(value) - 3])
            return dValue
    return 0
		
def getDipValueOr0(element,  attributeName) :
    try :
        return getDipValue(element, attributeName)
    except Exception as error:
             print('Caught this error: ' + repr(error))
    return 0
		
	
def hasDipValue(element,  attributeName) :
    value = element.get(attributeName)
    if (not TextUtils.isEmpty(value) and value.endswith(Constants.UNIT_DIP)) :
        return True
    return False
	
def parse(file):
    tree = ET.parse('country_data.xml')
    return tree
	

