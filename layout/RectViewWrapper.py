from RectUtils import Rect
from RectUtils import RectView

class RectViewWrapper:
#	public RectView view;
#	public Rect relativeBound;
#	public boolean overlapFlag;
#	public List<RectViewWrapper> relativeViews;

	def __init__(self,view, relativeBound):
		self.view = view
		self.relativeBound = relativeBound
		self.relativeViews = []
		self.overlapFlag = False

	def getType(self):
		return self.view.getType()
	

#	@Override
	def bound(self):
		return self.relativeBound

#	@Override
	def toString(self):
		return self.view + ", " + self.relativeBound + "," + self.overlapFlag;
