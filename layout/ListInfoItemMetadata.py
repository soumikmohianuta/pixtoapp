from layout import ListInfoData
from layout import FieldMetadata

class ListInfoItemMetadata:

#	private final ListInfoData infoData
#	private String variableName
#
    def __init__(self, infoData,  _type,  value):
        self.infoData = infoData
        self.type = _type
        self.value = value
        self.variableName = ""


    def getIsText(self):
        return self.type.type == FieldMetadata.TEXT
    

    def getIsLast(self):
        return self.infoData.isLast(self)