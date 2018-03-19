from resource import Resource

class TextResource (Resource.Resource):
    def __init__(self, document= None, root= None):
        super().__init__()
        self.mDocument = document
        self.mRoot = root
