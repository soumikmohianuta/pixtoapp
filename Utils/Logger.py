# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 18:40:57 2017

@author: soumi
"""

CROPPING_INFO_LOG = "cropping_command_log"; 
RULE_INFO_LOG = "rule_info_log";
REE_HEIGHT_LOG = "tree_height_log";
     
logDataMaps = {}
    

def append(logDataName, row):
    if logDataName not in logDataMaps:
        logDataMaps[logDataName] = []
    logDataMaps[logDataName].append(row);
    

def store(outputFolder):
    for entry in logDataMaps:
        rows = logDataMaps[entry]
        buffer = ""
        for row in rows:
            buffer += row
            buffer += "\n"                
        #Util.writeFile(buffer.toString(), outputFolder + "/" + entry.getKey() + ".log");    

def clear():
    logDataMaps = {}

