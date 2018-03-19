# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 20:37:43 2018

@author: soumi
"""
from functools import cmp_to_key
from layout import AlignGroupFunction
from RectUtils import RectUtil
class AlignLeftGroup(AlignGroupFunction.AlignGroupFunction):

#        @Override
    def __init__(self, defaultAlignThreshold,groupDistanceVerticalTheshold ):
#            super().__init()
            self.mDefaultAlignThreshold = defaultAlignThreshold
            self.mGroupDistanceVerticalTheshold= groupDistanceVerticalTheshold
            
    def sameGroup(self, r1, r2) :
            return RectUtil.alignLeft(r1, r2, self.mDefaultAlignThreshold)
        

#        @Override
#        def closestDistance() :
#            return new Function<ClosestDistanceInfo<RectView>, Boolean>() :

#                @Override
    def apply(self,info) :
            if (not (info.mSecond.bound().tl_Pt().y - info.mFirst.bound().br_Pt().y <= self.mGroupDistanceVerticalTheshold)) :
                return False
                    
            for neighbour in info.mNeighbours :
                if (neighbour != info.mFirst and neighbour != info.mSecond and RectUtil.above(info.mSecond,neighbour) and RectUtil.below(info.mFirst,neighbour)) :
                    return False
            return True    
   
    def sort(self,elements) :
            elements.sort(key=cmp_to_key(RectUtil.getTopBottomComparator))   

#        @Override
    def sortComparator(self) :
          return cmp_to_key(RectUtil.getTopBottomComparator)
        
    
class AlignRightGroup(AlignGroupFunction.AlignGroupFunction):
    def __init__(self, defaultAlignThreshold,groupDistanceVerticalTheshold ):
#            super().__init()
            self.mDefaultAlignThreshold = defaultAlignThreshold
            self.mGroupDistanceVerticalTheshold= groupDistanceVerticalTheshold
            
    def sameGroup(self, r1, r2) :
            return RectUtil.alignRight(r1, r2, self.mDefaultAlignThreshold)

#        @Override
#         Function<ClosestDistanceInfo<RectView>, Boolean> closestDistance() :
#
#            return new Function<ClosestDistanceInfo<RectView>, Boolean>() :

#                @Override
    def apply(self,info) :
            if not (info.mSecond.bound().tl_Pt().y - info.mFirst.bound().br_Pt().y <= self.mGroupDistanceVerticalTheshold):
                return False
                    
            for neighbour in info.mNeighbours() :
                if (neighbour != info.mFirst()and neighbour != info.mSecond and RectUtil.above(info.mSecond.bound(),neighbour.bound())and RectUtil.below(info.mFirst().bound(),neighbour.bound())) :
                    return False
           
            return True
                        
    def sort(self,elements) :
            elements.sort(key=cmp_to_key(RectUtil.getTopBottomComparator))    
   
    def sortComparator(self) :
          return cmp_to_key(RectUtil.getTopBottomComparator)

class AlignTopGroup(AlignGroupFunction.AlignGroupFunction):

    def __init__(self, defaultAlignThreshold,groupDistanceVerticalTheshold ):
#            super().__init()
            self.mDefaultAlignThreshold = defaultAlignThreshold
            self.mGroupDistanceVerticalTheshold= groupDistanceVerticalTheshold

    def sameGroup(self, r1, r2) :
            return RectUtil.alignTop(r1, r2, self.mDefaultAlignThreshold)

#        @Override
#         Function<ClosestDistanceInfo<RectView>, Boolean> closestDistance() :
#
#            return new Function<ClosestDistanceInfo<RectView>, Boolean>() :

#                @Override
    def apply(self,info) :
            if (not(info.mSecond.bound().tl_Pt().x- info.mFirst.bound().br_Pt().x <= self.mGroupDistanceVerticalTheshold)) :                
                 return False
            for neighbour in info.mNeighbours() :
                if (neighbour != info.mFirst and neighbour != info.mSecond and RectUtil.left(info.mSecond.bound(),neighbour.bound()) and RectUtil.right(info.mFirst.bound(),neighbour.bound())) :
                    return False
           
            return True
                        
    def sort(self,elements) :
            elements.sort(key=cmp_to_key(RectUtil.getLeftRightComparator))    

    def sortComparator(self) :
            return cmp_to_key(RectUtil.getLeftRightComparator)



class AlignBottomGroup(AlignGroupFunction.AlignGroupFunction):

        def __init__(self, DefaultAlignThreshold):
#            super().__init()
            self.mDefaultAlignThreshold = DefaultAlignThreshold
            
        def sameGroup(self, r1, r2) :
            return RectUtil.alignBottom(r1, r2, self.mDefaultAlignThreshold)

#        @Override
#         Function<ClosestDistanceInfo<RectView>, Boolean> closestDistance() :
#
#            return new Function<ClosestDistanceInfo<RectView>, Boolean>() :

#                @Override
        def apply(self,info) :
            if (not(info.mSecond.bound().tl_Pt().x- info.mFirst.bound().br_Pt().x <= self.mGroupDistanceVerticalTheshold)) :                
                 return False
            for neighbour in info.mNeighbours() :
                if (neighbour != info.mFirst and neighbour != info.mSecond and RectUtil.left(info.mSecond.bound(),neighbour.bound()) and RectUtil.right(info.mFirst.bound(),neighbour.bound())) :
                    return False
           
            return True
                        
        def sort(self,elements) :
            elements.sort(key=cmp_to_key(RectUtil.getLeftRightComparator))    
        
        
        def sortComparator(self) :
            return cmp_to_key(RectUtil.getLeftRightComparator)