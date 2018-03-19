from Utils import Constants, ImageUtil
from resource import Resource
from RectUtils import RectView
import cv2
import copy
from RectUtils import RectUtil
from RectUtils import Rect
from xml.etree.ElementTree import Element, SubElement, Comment, tostring

class DrawableWriter(Resource.Resource):
    
#	private final String mProjectPath;
#	private final String mExtention;
#	private final Map<String, DrawableInfo> drawableInfos;
    

    def __init__(self, extention, projectPath):
        super().__init__()
        self.mExtention = extention
        self.mProjectPath = projectPath
        self.drawableInfos = {}
        self.mId = 0
	

#	// public String addResource(final Mat originalImage, final MatOfPoint
#	// contour) {
#	// final Rect rect = Imgproc.boundingRect(contour);
#	// return addResource(originalImage, rect);
#	// }

    def addResource(self,originalImage,rect):
       		image = ImageUtil.getImage(originalImage, rect.bound())
	       	return self.addResourceDirectly(image, rect)

    def addResourceDirectly(self,image,rect):
        _id = "img_" + str(self.mId )
        drawableInfo = DrawableInfo()
        drawableInfo.path = self.mProjectPath + Constants.DEFAULT_DRAWABLE_PATH + _id + self.mExtention
        print(drawableInfo.path )
        drawableInfo.mat = image;
        drawableInfo.rectView = rect
        self.drawableInfos[_id] = drawableInfo
        self.mId = self.mId +1 
        return _id
    
    def save(self):
        for key in self.drawableInfos:
            contour = self.drawableInfos[key].rectView.contour
            if (contour != None and not RectView.isContanerView(self.drawableInfos[key].rectView)):
                contour = RectUtil.convertToParentCorrdinate(self.drawableInfos[key].rectView, contour)
                overlay = ImageUtil.createTransparentBackground(self.drawableInfos[key].mat, contour)
                cv2.writePng(self.drawableInfos[key].path, overlay)
            else:
                cv2.imwrite(self.drawableInfos[key].path, self.drawableInfos[key].mat)



#	public void unRegister(final String drawableId) {
#		// drawableInfos.remove(drawableId);
#	}

class DrawableInfo:
    
    def __init__(self, image = None, view = None, path= ""):
        self.rectView = view
        self.path = path
        self.mat = image

    def __hash__(self):
        prime = 31
        result = 1
        result = prime * result + (self.mat.shape)[0]
        result = prime * result + (self.mat.shape)[1]
        return result

    def __eq__(self, other):
        
        if type(other) != type(self):
            return False
        elif self.mat.shape != other.mat.shape :
            return False
        else:
            subtractMat = copy.deepcopy(self.mat)
            cv2.subtract(self.mat, other.mat,subtractMat)
            countNonZero = cv2.countNonZero(subtractMat)
            return countNonZero == 0

#		@Override
#		public boolean equals(final Object obj) {
#			if (!(obj instanceof DrawableInfo)) {
#				return false;
#			}
#			final DrawableInfo oD = (DrawableInfo) obj;
#
#			if (mat.rows() != oD.mat.rows() || mat.cols() != oD.mat.cols()) {
#				return false;
#			}
#			final Mat substractMat = new Mat();
#			Core.subtract(this.mat, oD.mat, substractMat);
#			final int countNonZero = Core.countNonZero(substractMat);
#			return countNonZero == 0;
#		}

#		@Override
#		public int hashCode() {
#			final int prime = 31;
#			int result = 1;
#			result = prime * result + mat.cols();
#			result = prime * result + mat.rows();
#			return result;
#		}
#	}

