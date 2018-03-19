import os
import shutil
from Utils import Constants
from xml.etree.ElementTree import Element
from Utils import TextUtils
from os.path import basename
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

PACKAGE_NAME_PREFIX = "edu.uta.cse.screenshot."
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
SDK_FOLDER = os.path.join(APP_ROOT, 'android-sdk/')
def copyFile(src, dst):
    shutil.copyfile(src,dst)

def copyFolder(src,dst):
    
    if(os.path.isdir(src)):
        if(not os.path.exists(dst)):
            os.makedirs(dst)
        files = os.listdir(src)        
        

        for file in files:
#				// construct the src and dest file structure
            srcFile = os.path.join(src, file)
            destFile = os.path.join(dst, file)
#				// recursive copy
            copyFolder(srcFile, destFile)
    else:
#			// if file, then copy it
        copyFile(src,dst)


def readFile(fileName):
    fOpen = open(fileName,"r") #opens file with name of "test.txt"
    content = fOpen.read()
    fOpen.close()
    return content


def readFileEncoded(path, encoding):
    fOpen = open(path, encoding=encoding)
    content = fOpen.read()
    fOpen.close()
    return content

#	public static String readFileFileInputSteam(String path, Charset encoding)
#			throws IOException {
#		FileInputStream fileInputStream = new FileInputStream(new File(path))
#		byte[] bytes = new byte[fileInputStream.available()]
#		fileInputStream.read(bytes)
#		String content = new String(bytes, StandardCharsets.UTF_8)
#		fileInputStream.close()
#		return content
#	}

def readByte(fileName):
    fOpen = open(fileName,"rb") #opens file with name of "test.txt"
    content = fOpen.read()
    fOpen.close()
    return content


def isValidUTF8(_input):
   valid_utf8 = True
   try:
       _input.decode('utf-8')
   except UnicodeDecodeError:
       valid_utf8 = False
   
   return valid_utf8
        
def writeFile(content, fileName):
    fOpen = open(fileName,"w") #opens file with name of "test.txt"
    content = fOpen.write(content)
    fOpen.close()
    
def writeFileEncoded(content, fileName,encoding):
    fOpen = open(fileName,"w",encoding=encoding) #opens file with name of "test.txt"
    content = fOpen.write(content)
    fOpen.close()
       


def run(command):
#    sudoPassword = "1234"
#    sudoCommand = 'echo %s|sudo -S %s' % (sudoPassword,command)
#    print(sudoCommand)
    os.system(command)

def runWithOutput(command):
    sudoPassword = "1234"
    out = os.popen('echo %s|sudo -S %s' % (sudoPassword,command)).read()
    print(out)
    return out


def chmodFilePath(filePath) :
    run("chmod 777 " + filePath)


def chmodFile(file):     
    run("chmod 777 " + os.path.abspath(file))

def writeFileAndChmod(data, filepath, encoding=None):
    if encoding == None:
        writeFile(data, filepath)
    else:
        writeFile(data, filepath, encoding)
    
    chmodFilePath(filepath)

def writeFileAndChmodFilePath(data, filePath, encoding=None):
		writeFileAndChmod(data, filePath,encoding)

def writeFileAndChmodFile(data, file, encoding=None):
		writeFileAndChmod(data, os.path.abspath(file), encoding)


def writeFileAndRunFilePath(data, filePath):
		writeFileAndChmod(data, filePath)
		runWithOutput(data)
        
def writeFileAndRunFile(data,filePath):
		writeFileAndRunFilePath(data, os.path.abspath(filePath))



def getAllFilesRecusively(folder, files, filenameFilter):
    if (folder == None or os.path.isfile(folder)):
        return files
    listFiles = []
    for file in os.listdir(folder):
            if file.endswith(filenameFilter):
                listFiles.append( os.path.join(folder, file))
    
    if (len(listFiles) == 0):
        return files

    files.extend(listFiles)
    subFolders = [x for x in listFiles if os.path.isdir(x)]

    for subFolder in subFolders:
        getAllFilesRecusively(subFolder, files, filenameFilter)
		
    return files


def getAndroidSDKPath():
    UPLOAD_FOLDER = os.path.join(APP_ROOT, r"android-sdk/")
    return UPLOAD_FOLDER

def getAndroidProjectCreatePath():
    return r"/home/soumik/Research/upload_And_Download/REMAUI_AWS/android-sdk/tools/android"


def readLine(filePath):
    lines = []
    with open(filePath) as f:
         lines = f.readlines()
		
    return lines


import re

def createValidAndroidProjectName(mFileName):
    valideName = mFileName.replace("-", "_")
    valideName = valideName.replace(".", "_")
    valideName = valideName.replace("-", "_")
    valideName = valideName.replace("#", "_")
    valideName = valideName.replace("*", "_")
    m = re.search('[a-z|A-Z]', valideName)  
    valideName = valideName[m.start():]
    return valideName
	

def getBaseNameRemoveInvalidChars(fileName):
		return TextUtils.removeInvalidProjectNameChars(basename(fileName))

def getProjectName(fileName):
		baseName = createValidAndroidProjectName(fileName)
		return baseName.upper()

def getPackageName(fileName):
    baseName = createValidAndroidProjectName(fileName)
#TODO    return Constants.PACKAGE_NAME_PREFIX + baseName.lower()
    return  baseName.lower()+".com.remaui"


def sanitizeFilename(name):
    repCharacterList = "[:\\\\/*?|<>]"
    outResult = name
    for c in repCharacterList:
        outResult = outResult.replace(c,'_')
    return outResult
	


def convertPageToFolderPath(packageName):
    return packageName.replace("\\.", "/")



def getHeightofView(root):
    maxVal= 0
    for childNode in root.mChildren:
        height = childNode.height
        if (height > maxVal):
            maxVal = height
    return maxVal + 1


def getHeightofElement(root):
    maxVal = 0
    elements = root.iter()
    for childNode in elements:
        if type(childNode) == Element:
            height = getHeightofElement(childNode)
            if (height > maxVal):
                maxVal = height
    return maxVal + 1
    
    


def copyFileFromClassPath(classPathFilePath, absolutePath):
    name = basename(classPathFilePath)
    destFile = os.path.join(absolutePath, name)
    run("cp "+ classPathFilePath + " " + destFile)
#    shutil.copyfile(classPathFilePath,destFile)

def readFileFromClassPath(classPathFilePath):
    fOpen = open(classPathFilePath,"r") #opens file with name of "test.txt"
    content = fOpen.read()
    fOpen.close()
    return content
