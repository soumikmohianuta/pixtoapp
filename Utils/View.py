from Utils import Attribute

class View:

    def View(self,name):
        self.mName = name
        self.attributes = []
        self.mChildren = []
        
        
    @classmethod
    def fromELement(cls,element):
        mName = element.tag
        viewCls = cls(mName)
        attributeslist = []
        mChildren = []
        attributes = element.attributes.values()
        for obj in attributes:
            attributeslist.append(Attribute(obj.name, obj.value))

        elements = [elem for elem in element.iter()]
        for obj in elements:
            mChildren.add(View.fromELement(obj))
            
        viewCls.mChildren =mChildren
        viewCls.attributes = attributeslist
        return cls(mName)
        
    def addAtribute(self,attribute):
        self.attributes.append(attribute)
