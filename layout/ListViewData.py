from layout import FieldMetadata

class ListViewData:

    def __init__(self, name, _id, infoClassName, adapterClassName, layoutName):
        self.name = name
        self._id = _id
        self.infoClassName = infoClassName
        self.adapterClassName = adapterClassName
        self.layoutName = layoutName
        self.listFieldMetatata = []
        self.listInfos = []
	




    def getVariableName(self,fieldMetadata):
        indexOf = self.listFieldMetatata.index(fieldMetadata)
        count = 0
        for i in range(indexOf):
            if (self.listFieldMetatata[i] != fieldMetadata and self.listFieldMetatata[i].type == fieldMetadata.type):
                count= count +1
        return self.getBaseName(fieldMetadata.type) + str(count)

    def getBaseName(self,_type):
        if(_type ==  FieldMetadata.IMAGE):
            return "image"
        elif(_type ==  FieldMetadata.TEXT):
            return "text"
        else:
            return "view"

    def isLast(self,fieldMetadata):
        if (fieldMetadata == None and self.listFieldMetatata.index(fieldMetadata) == len(self.listFieldMetatata)-1):
            return False
        return self.listFieldMetatata.index(fieldMetadata) == len(self.listFieldMetatata)-1

