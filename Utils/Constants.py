# -*- coding: utf-8 -*-
'''
Created on Wed Oct  4 16:19:04 2017

@author: soumi
'''

ANDROID_SDK_LOCATION = '${HOME}/tools/android-sdk'
OUT_PUT_PROJECT_FOLDER = 'projects'
OUT_PUT_VIEW_DUMP_FOLDER = 'viewDump'
OUT_PUT_LOG_FOLDER = 'logs'
OUT_PUT_APK_FOLDER = 'apks'
OUT_PUT_SCREENSHOT_FOLDER = 'screenshots'
ARGS_IMAGE_FOLDER = 'd'
ARGS_OUTPUT_FOLDER = 'o'

TIMER_ID_TOTAL = 'TIMER_ID_TOTAL'
TIMER_ID_ADD_TEXTBOX_TO_VIEW_HIERARCHY = 'TIMER_ID_ADD_TEXTBOX_TO_VIEW_HIERARCHY'
TIMER_ID_COMPUTER_VISION_STEP = 'TIMER_ID_COMPUTER_VISION_STEP'
TIMER_ID_CREATE_ANDROID_PROJECT_AND_RESOURCE = 'TIMER_ID_CREATE_ANDROID_PROJECT_AND_RESOURCE'
TIMER_ID_CREATE_ANDROID_VIEW_HIERARCHY = 'TIMER_ID_CREATE_ANDROID_VIEW_HIERARCHY'
TIMER_ID_IDENTIFY_REPEATED_ITEMS = 'TIMER_ID_IDENTIFY_REPEATED_ITEMS'
TIMER_ID_MATCH_OCR_WORDS_TO_VISION_BOXES = 'TIMER_ID_MATCH_OCR_WORDS_TO_VISION_BOXES'
TIMER_ID_OCR = 'TIMER_ID_OCR'
TIMER_ID_SPLIT_LINE_INTO_TEXT_BOXES = 'TIMER_ID_SPLIT_LINE_INTO_TEXT_BOXES'


INPUT_FOLDER_VALUE = ''
OUTPUT_FOLDER_VALUE = ''
    #Nexus 5 screens: 1080*1920
DEFAULT_OUTPUT_SCREEN_WIDTH_PIXEL = 1080.0
DEFAULT_OUTPUT_SCREEN_HEIGHT_PIXEL = 1920.0
	#1080 px
DEFAULT_SCREEN_WIDTH_DP = 360.0
   #1557 px
DEFAULT_SCREEN_CONTENT_VIEW_HEIGHT_DP = 519.0
    # 144 px
DEFAULT_SCREEN_TITLE_BAR_HEIGHT_DP = 48.0
    #OCR constants
    
    # the standard ratio between a textbox and its boundary
TEXT_BOX_AND_TEXT_HEIGHT_RATIO = 1.257
TEXT_CONFIDENT_THRESHOLD = 40.0
TEXT_CONFIDENT_THRESHOLD_SECONDARY_RANGE = 30.0
TEXT_CONFIDENT_ACCEPTANCE_DIMENSION_RATIO_DIFFERENCE_THRESHOLD = 0.5
TEXT_AREA_ACCEPTANCE_DIFFERENCE_THRESHOLD = 0.0164
WORD_SPACE_THRESHOLD_BASE_ON_HEIGHT = 0.75
SPACE_BETWEEN_WORD_RATIO = 1.7

    
     #Layout constants
    
GROUP_DISTANCE_VERTICAL_THRESHOLD = 12.975
DEFAULT_EQUAL_THRESHOLD = 5.625
DEFAULT_ALIGN_THRESHOLD = 11.25
MIN_SINGLE_LIST_AREA = 54.0*54.0 #54D
    
     #Never set this value < 3, a list with two items with get false positive
    
LAYOUT_MIN_ACCEPTABLE_LIST_SIZE = 3

MIN_AREA_TO_IGNORE_RATIO_WIDTH_DP = 4.325
MIN_AREA_TO_IGNORE_RATIO_HEIGHT_DP = 4.325
    
    #Open CV
    
    # HISTOGRAM comparison
HISTOGRAM_BHATTACHARYYA_THRESHOLD = 0.1

    # CANNY algorithm
CANNY_KERRY_WONG_LOW_THRESHOLD_RATIO = 0.66
    # we want to low threshold value of candy always below 0.1 #255, some
    # image the contrast between button and background not must different
CANNY_RATIO_CONTROL_THRESHOLD = 0.1 / CANNY_KERRY_WONG_LOW_THRESHOLD_RATIO
    # bilateralFilter
    
    #Diameter of each pixel neighborhood that is used during filtering. If it
    #is non-positive, it is computed from sigmaSpace .
CANNY_PARAM_VALUE_D = 3
    
    #Filter sigma in the color space. A larger value of the parameter means
    #that farther colors within the pixel neighborhood (see sigmaSpace ) will
    #be mixed together, resulting in larger areas of semi-equal color.
    
CANNY_PARAM_VALUE_SIGMA_COLOR = 50
    
         #Filter sigma in the coordinate space. A larger value of the parameter
         #means that farther pixels will influence each other as long as their
         #colors are close enough (see sigmaColor ). When d>0 , it specifies the
         #neighborhood size regardless of sigmaSpace . Otherwise, d is proportional
         #to sigmaSpace .
         
CANNY_PARAM_VALUE_SIGMA_SPACE = 50

    # texts in list items become images
TEXT_TO_BECOME_IMAGE_MIN_ACCEPTABLE_LIST_SIZE = 3
TEXT_TO_BECOME_IMAGE_IN_LIST_THRESHOLD = 90.0


    # 75 px
DEFAULT_SCREEN_STATUS_BAR_HEIGHT_DP = 25.0
	# 144 px
DEFAULT_SCREEN_NAVIGATION_BAR_HEIGHT_DP = 48.0
    
EXTRA_WORD_SPACE_RATIO = 0.3
DEFAULT_DRAWABLE_PATH = '/app/src/main/res/drawable/'
DEFAULT_LAYOUT_PATH = '/app/src/main/res/layout/'
DEFAULT_LAYOUT_LIST_PREFIX = 'list_layout'
    
ELEMENT_TEXT_VIEW = 'TextView'
ATTRIBUTE_TEXT = 'android:text'
ATTRIBUTE_TEXT_COLOR = ' android:textColor'

ATTRIBUTE_TEXT_SIZE = 'android:textSize'
ATTRIBUTE_FONT_FAMILY = 'android:fontFamily'
ATTRIBUTE_TEXT_STYLE = 'android:textStyle'
ATTRIBUTE_TEXT_ALL_CAPS = 'android:textAllCaps'
ATTRIBUTE_TYPEFACE = 'android:typeface'
ATTRIBUTE_WRAP_CONTENT = 'wrap_content'
ATTRIBUTE_MATCH_PARENT = 'match_parent'
UNIT_DIP = 'dip'
ATTRIBUTE_ID = 'android:id'
ATTRIBUTE_LAYOUT_MARGIN_TOP = 'android:layout_marginTop'
ATTRIBUTE_LAYOUT_MARGIN_LEFT = 'android:layout_marginLeft'
ATTRIBUTE_LAYOUT_HEIGHT = 'android:layout_height'
ATTRIBUTE_LAYOUT_WIDTH = 'android:layout_width'
ATTRIBUTE_SCALE_TYPE = 'android:scaleType'
ATTRIBUTE_BACKGROUND = 'android:background'
    
ATTRIBUTE_PADDING_LEFT = 'android:paddingLeft'
ATTRIBUTE_PADDING_RIGHT = 'android:paddingRight'
ATTRIBUTE_PADDING_TOP = 'android:paddingTop'
ATTRIBUTE_PADDING_BOTTOM = 'android:paddingBottom'
ATTRIBUTE_MIN_SDK_VERSION = 'android:minSdkVersion'
ATTRIBUTE_TARGET_SDK_VERSION = 'android:targetSdkVersion'

	# for Linear Layout and Frame Layout
ATTRIBUTE_GRAVITY = 'android:gravity'
ATTRIBUTE_LAYOUT_GRAVITY = 'android:layout_gravity'
ATTRIBUTE_LAYOUT_GRAVITY_TOP = 'top'
ATTRIBUTE_LAYOUT_GRAVITY_BOTTOM = 'bottom'
ATTRIBUTE_LAYOUT_GRAVITY_LEFT = 'left'
ATTRIBUTE_LAYOUT_GRAVITY_RIGHT = 'right'
ATTRIBUTE_LAYOUT_GRAVITY_CENTER_VERTICAL = 'center_vertical'
ATTRIBUTE_LAYOUT_GRAVITY_CENTER_HORIZONTAL = 'center_horizontal'
ATTRIBUTE_LAYOUT_GRAVITY_FILL_PARRENT = 'fill_vertical'
ATTRIBUTE_LAYOUT_GRAVITY_FILL_HORIZONTAL = 'fill_horizontal'
ATTRIBUTE_LAYOUT_GRAVITY_CENTER = 'center'
ATTRIBUTE_LAYOUT_GRAVITY_FILL = 'fill'

ATTRIBUTE_LAYOUT_GRAVITY_CLIP_VERTICAL = 'clip_vertical'
ATTRIBUTE_LAYOUT_GRAVITY_CLIP_HORIZONTAL = 'clip_horizontal'
ATTRIBUTE_LAYOUT_GRAVITY_START = 'start'
ATTRIBUTE_LAYOUT_GRAVITY_END = 'end'
	
	# for Relative Layout
ATTRIBUTE_LAYOUT_ABOVE = 'android:layout_above'
ATTRIBUTE_LAYOUT_ALIGN_BASELINE = 'android:layout_alignBaseline'
ATTRIBUTE_LAYOUT_ALIGN_BOTTOM = 'android:layout_alignBottom'
ATTRIBUTE_LAYOUT_ALIGN_END = 'android:layout_alignEnd'
ATTRIBUTE_LAYOUT_ALIGN_LEFT = 'android:layout_alignLeft'
ATTRIBUTE_LAYOUT_ALIGN_PARENT_BOTTOM = 'android:layout_alignParentBottom'
ATTRIBUTE_LAYOUT_ALIGN_PARENT_END = 'android:layout_alignParentEnd'
ATTRIBUTE_LAYOUT_ALIGN_PARENT_LEFT = 'android:layout_alignParentLeft'
ATTRIBUTE_LAYOUT_ALIGN_PARENT_RIGHT = 'android:layout_alignParentRight'
ATTRIBUTE_LAYOUT_ALIGN_PARENT_START = 'android:layout_alignParentStart'
ATTRIBUTE_LAYOUT_ALIGN_PARENT_TOP = 'android:layout_alignParentTop'
ATTRIBUTE_LAYOUT_ALIGN_RIGHT = 'android:layout_alignRight'
ATTRIBUTE_LAYOUT_ALIGN_START = 'android:layout_alignStart'
ATTRIBUTE_LAYOUT_ALIGN_TOP = 'android:layout_alignTop'
ATTRIBUTE_LAYOUT_BELOW = 'android:layout_below'
ATTRIBUTE_LAYOUT_CENTER_HORIZONTAL = 'android:layout_centerHorizontal'
ATTRIBUTE_LAYOUT_CENTER_IN_PARENT = 'android:layout_centerInParent'
ATTRIBUTE_LAYOUT_CENTER_VERTICAL = 'android:layout_centerVertical'
ATTRIBUTE_LAYOUT_END_OF = 'android:layout_toEndOf'
ATTRIBUTE_LAYOUT_LEFT_OF = 'android:layout_toLeftOf'
ATTRIBUTE_LAYOUT_RIGHT_OF = 'android:layout_toRightOf'
	 
ATTRIBUTE_LAYOUT_START_OF = 'android:layout_toStartOf'
ATTRIBUTE_STYLE = 'style'
    
ELEMENT_RESOURCE = 'resources'
ELEMENT_STRING = 'string'
ELEMENT_STYPE = 'style'
ELEMENT_COLOR = 'color'
ELEMENT_ITEM = 'item'
ELEMENT_IMAGE_VIEW = 'ImageView'
    
ATTRIBUTE_NAME = 'name'

VALUE_STRING_FILE_NAME = 'string'
VALUE_STYLE_FILE_NAME = 'style'
VALUE_COLOR_FILE_NAME = 'color'
VALUE_DRAWABLE_FILE_NAME = 'drawable'

    # RESOURCE_FOLDER = '/home/ubuntu/remaui-web-1.0/conf'
#RESOURCE_FOLDER = '/Users/siva/Remaui_Workspace/Core/Resources/'
TEMPLATE_FOLDER = 'templates'
EXE_FOLDER = 'exe'
SCRIPT_INSTALL_FILE_NAME = 'install.sh'
SCRIPT_UNINSTALL_FILE_NAME = 'uninstall.sh'
SCRIPT_COMPILE_FILE_NAME = 'compile.sh'
SCRIPT_SCREENSHOT_CAPTURE_FILE_NAME = 'screenshot_capture.sh'
EXE_TEXT_DETECTION_FILE_NAME = 'textdetection'
TEMPLATE_SCRIPT_INSTALL = TEMPLATE_FOLDER + '/'+ SCRIPT_INSTALL_FILE_NAME
TEMPLATE_SCRIPT_COMPILE = TEMPLATE_FOLDER + '/'+ SCRIPT_COMPILE_FILE_NAME
TEMPLATE_SCRIPT_SCREENSHOT_CAPTURE = TEMPLATE_FOLDER + '/' + SCRIPT_SCREENSHOT_CAPTURE_FILE_NAME
EXE_TEXT_DETECTION = EXE_FOLDER + '/' + EXE_TEXT_DETECTION_FILE_NAME
    
OUT_PUT_LOG_FOLDER_FOR_ALL = OUT_PUT_LOG_FOLDER + '/' + 'all'

STRING_PACAKGE_NAME = 'package_name'
STRING_PROJECT_NAME = 'project_name'
STRING_OUTPUT_PATH = 'output_path'
STRING_FOLDER_PATH = 'folder_path'
STRING_ADB_LOCATION = 'adb_location'
STRING_ANT_LOCATION = 'ant_location'
STRING_OUTPUT_APK_FOLDER = 'output_apk_folder'
STRING_OUTPUT_SCREENSHOT_FOLDER = 'output_screenshot_folder'

    # For Core constant (Temp)
CV_8U = 0
CV_8S = 1
CV_16U = 2 
CV_16S = 3
			
CV_32S = 4 
CV_32F = 5 
CV_64F = 6 
CV_USRTYPE1 = 7
DEPTH_MASK_8U = 1 << CV_8U
DEPTH_MASK_8S = 1 << CV_8S
DEPTH_MASK_16U = 1 << CV_16U
DEPTH_MASK_16S = 1 << CV_16S
DEPTH_MASK_32S = 1 << CV_32S
DEPTH_MASK_32F = 1 << CV_32F
DEPTH_MASK_64F = 1 << CV_64F
DEPTH_MASK_ALL = (DEPTH_MASK_64F << 1) - 1
DEPTH_MASK_ALL_BUT_8S = DEPTH_MASK_ALL & ~DEPTH_MASK_8S
DEPTH_MASK_FLT = DEPTH_MASK_32F + DEPTH_MASK_64F
INVISIBLE_CHARACTER_REG = '[\\p{C}\\s]*'
NON_ASCII_CHARACTER_REG = '[^\\x00-\\x7F]*'
MIN_INVALID_LIST_TEXT_THRESHOLD = 70
MIN_ACCEPTABLE_LIST_SIZE_FOR_INVALID_LIST_TEXT = 5
IS_DEBUG_MODE = True
