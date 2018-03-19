from RectUtils.RectUtil import *
class ViewRelation:
    def ViewRelation(self,view):
        self.left = []
        self.top = []
        self.right = []
        self.bottom = []
        self.alignLeft = []
        self.alignTop = []
        self.alignRight = []
        self.alignBottom = []
        self.view =view


    def closestLeft(self,views):
        rb = None
        if (len(views) >= 0):
            rb = views[0]
            for i in range(1,len(views)):
                rectView = views[i]
                if (RectUtil.left(rectView.bound(), self.view.bound()) and self.closerLeft(rectView.bound(), rb.bound())):
                    rb = rectView
        return rb
    
    def closestTop(self,views):
        rb = None
        if (len(views) >= 0):
            rb = views[0]
            for i in range(1,len(views)):
                rectView = views[i]
                if (RectUtil.above(rectView.bound(), self.view.bound()) and self.closestTop(rectView.bound(), rb.bound())):
                    rb = rectView
        return rb
    
    def closestRight(self,views):
        rb = None
        if (len(views) >= 0):
            rb = views[0]
            for i in range(1,len(views)):
                rectView = views[i]
                if (RectUtil.right(rectView.bound(), self.view.bound()) and self.closestRight(rectView.bound(), rb.bound())):
                    rb = rectView
        return rb
    
    def closestBottom(self,views):
        rb = None
        if (len(views) >= 0):
            rb = views[0]
            for i in range(1,len(views)):
                rectView = views[i]
                if (RectUtil.below(rectView.bound(), self.view.bound()) and self.closestBottom(rectView.bound(), rb.bound())):
                    rb = rectView
        return rb

