
class ListInfoData:
    def __init__(self):
        self.metadatas = []

    def isLast(self, listInfoItemMetadata):
        if (listInfoItemMetadata == None or listInfoItemMetadata not in self.metadatas):
            return False
        
        return self.metadatas[listInfoItemMetadata] == self.metadatas[len(self.metadatas)-1]
