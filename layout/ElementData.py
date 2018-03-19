
from RectUtils.Rect import Rect

class ElementData:
    def __init__(self, top, left, width, height):
        self.x = top
        self.y = left
        self.width = width
        self.height = height
        self.rect = Rect(top,left,width,height)
    
#    @Override
    def bound(self):
        return self.rect

#    @Override
    def toString(self):
        return "(" + self.x + ", " + self.y + ", " + self.width + ", " + self.height + ")"
    
    
    def __eq__(self, other):
        
        if other is None:
            return self.rect.area() == 0
        elif type(other) != type(self):
                return False
        else:
            return (self.rect == other.rect) 

    def __ne__(self, other):
        return not(self.__eq__(other))
