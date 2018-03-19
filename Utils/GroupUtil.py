# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 16:23:41 2017

@author: soumi
"""



#public class GroupUtil {
#    /**
#     * Credit:http://stackoverflow.com/questions/8463543/grouping-elements-of-a-
#     * list-into-sublists-maybe-by-using-guava
#     */
def group(listItem, groupFunction):
    result = []

    for element in listItem:

        groupFound = False
        for group in  result:
            if (groupFunction(element, group[0])):
                group.append(element)
                groupFound = True
                break
                
        if (not groupFound) :
            newGroup = []
            newGroup.append(element)
            result.append(newGroup)
    return result
    
