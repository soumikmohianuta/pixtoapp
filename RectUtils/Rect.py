# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 20:26:16 2017

@author: soumi
"""
from RectUtils import Point

class Rect:
    
    def __init__(self, x=0 ,y=0 , width=0, height=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height 
    
    
    def tl(self):
        return (int(self.x) , int(self.y))
    
    def tl_Pt(self):
        return Point.Point(int(self.x) , int(self.y))
    
    def br_Pt(self):
        return Point.Point(int(self.x + self.width) ,  int(self.y + self.height))
    
    def br(self):
        return (int(self.x + self.width) ,  int(self.y + self.height))

    
    def reshape(self,  x ,y , width, height):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        return self
    
    def area(self):
        return self.height*self.width
    
    def __hash__(self):
        return hash((self.x, self.y, self.width, self.height))

    def __eq__(self, other):
        
        if other is None:
            return self.area() == 0
        else:
            return (self.x, self.y, self.width, self.height) == (other.x, other.y, other.width, other.height)

    def __ne__(self, other):
        return not(self.__eq__(other))