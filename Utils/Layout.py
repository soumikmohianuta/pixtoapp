import xml.etree.ElementTree as ET
import ntpath
#import View
class Layout:
    def __init__(self, _id, root):
        self.mId = _id
        self.mRoot = root

    @classmethod
    def fromFile(cls,layoutFile):
        _Id = ntpath.basename(layoutFile)[0: len(ntpath.basename(layoutFile)) - 4]
        try:
            tree = ET.parse(layoutFile)
            root = tree.getroot()
            return cls(_Id, root)

        except ValueError:
            print("Can't find the or read the xml File")


    def getAllView(self):
        views = []
        views.append(self.mRoot)
        children = self.mRoot.mChildren
        for view in children:
            views.append(view)
 
        return views


