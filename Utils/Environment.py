# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 18:40:24 2017

@author: soumi
"""

from enum import IntEnum


KEY_WITH_TITLE_BAR = "with_title_bar"
KEY_SCALE_TYPE = "scale_type"
KEY_TEXT_WIDTH_WRAP_CONTENT = "text_width_wrap_content"
KEY_GENERATE_WITH_RANDOM_BACKGROUND_COLOR = "generate_with_random_color"
KEY_GENERATE_WITH_BACKGROUND_COLOR_DETECTION = "generate_with_background_color_detection"
KEY_REMOVE_DATA_FOLDER_WHEN_UNINSTALL = "remove_data_folder_when_uninstall"
KEY_FOLDER_OUTPUT = "output_folder"
KEY_INPUT_FOLDER = "input_folder"
KEY_LIST_SUPPORT = "list_support"
KEY_RULE_FILTER_INDEX = "rule_filter_index"
KEY_RULE_FILTER_INDEX_ENABLE = "rule_filter_index_enable"
KEY_CURRENT_PROJECT_NAME = "current_project_name"
KEY_SCREENSHOT_HAS_TITLEBAR = "screen_shot_has_title_bar"
    # {@link #KEY_SCALE_TYPE}
#    public enum ScaleType {
#        FIT_START,
#        FIT_XY,
#        KEEP_RATIO
#    }
     
class ScaleType(IntEnum):
    FIT_START = 1
    FIT_XY = 2
    KEEP_RATIO =3
    
    #private static Environment sEnviroment
    #private Map<String, Object> mValues
mValues = {}

def getValue(key):
    if key not in mValues:
        return None
    return mValues[key]

def putValue(key,value):
    mValues[key] =  value
