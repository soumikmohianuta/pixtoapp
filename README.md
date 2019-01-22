# Pix to App
It's a python project. 
# Dependencies-
1. Tesseract OCR
2. OpenCV
3. stringtemplate3
4. ANTLR 

#Set up environment variables (Windows)

#To integrate Tesseract OCR 
Build the latest library of Tesseract in Windows
-    Download and install Git, CMake and put them in PATH. 
-    [Download the latest CPPAN. Add CPPAN client in PATH too.](https://cppan.org/client/)
-    VS2015 redistributable and Windows SDK 8.1 are required. 
-    Put the test data in tessdata folder and add it to the path.
-    Run command "git clone https://github.com/tesseract-ocr/tesseract tesseract"
-    Run command – "mkdir win64 && cd win64"
- Run command    "cppan .."
-    Run command "cppan --generate" 

#Other Dependencies 
- Install OPenCV and set environment variable OPENCV_DIR and add it in path too
- pip install stringtemplate3. (For python3 replace the strintemplate folder in the environment [with this link](https://drive.google.com/open?id=19zdiuefxCrT5z6a_58FrkM2E3qImz_Fd) )
- Clone https://github.com/antlr/antlr3
- Go to directory runtime\Python3 and run python setup.py to install
- Download JDK and set environment variable JAVA_HOME.
- Download Android SDK and set the path in the templateProject which resides in the template folder
- Change the image path in the screenshotProcessor.py and run the project 
