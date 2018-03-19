# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 21:11:26 2017

@author: soumi
"""


def isEmpty(text):
    return text == None or len(text) == 0
    
def formatText(text):
    if (isEmpty(text)):
        return text
    buffer = ""
		# remove no ASCII character
    for c in text:
        if (c < ' ' or c > '~'):
            buffer+= ' '
        elif (c == 63):
            buffer+="\\?"
        elif (c == 64):
            buffer += '\\@'
        elif (c == 39):
            buffer += '\\'
        else:
            buffer+=c
    return buffer.strip().replace("\\n", " ")
    
def removeInvalidProjectNameChars(projectName):
    newName= projectName.replace("-", "_")
    newName= projectName.replace(".", "_")
    return newName.replace("\\", "_")

#	/**
#	 * Returns true if a and b are equal, including if they are both null.
#	 * <p>
#	 * <i>Note: In platform versions 1.1 and earlier, this method only worked
#	 * well if both the arguments were instances of String.</i>
#	 * </p>
#	 * 
#	 * @param a
#	 *            first CharSequence to check
#	 * @param b
#	 *            second CharSequence to check
#	 * @return true if a and b are equal
#	 */
#    def equals(a, b):
#        if (a == b):
#            return True
#        length = 0 
#        if a != None and b != None and len(a) == len(b):
#            if type(a) == str and type(b) ==  str:
#                return a.equals(b)
#        else:
#				for (int i = 0; i < length; i++) {
#					if a[i] != b[i]
#						return False
#				return True
#		return False
#	public static String getFirstMatch(String link, String regex) {
#		Pattern pattern = Pattern.compile(regex);
#		Matcher matcher = pattern.matcher(link);
#		if (matcher.find()) {
#			return matcher.group(1);
#		}
#		return null;
#	}
#}
