from Utils import TextUtils

class FieldMetadata:
    IMAGE = 0
    TEXT = 1
    VIEW = 2

    def __init__(self, listViewData, _type, layoutId=None):
        self._type = _type
        self.listViewData = listViewData
        self.layoutId = layoutId
		
		


    def getVariableName(self) :
        return self.listViewData.getVariableName(self)
		

    def getIsLast(self) :
        return self.listViewData.isLast(self)
		

    def getIsText(self) :
        return self.type == FieldMetadata.TEXT
		

    def getLayoutId(self) :
        if (TextUtils.isEmpty(self.layoutId)) :
                return self.getVariableName()
			
        return self.layoutId
		

		

