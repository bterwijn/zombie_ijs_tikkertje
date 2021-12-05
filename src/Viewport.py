
import pygame

import Polygon

class Viewport:

    def __init__(self,world_center,world_angle,view_center,view_angle,zoom):
        self.world_center=world_center
        self.world_angle=world_angle
        self.view_center=view_center
        self.view_angle=view_angle
        self.zoom=zoom

    def transform(self,value):
        return value/self.zoom
        
    def tranform_vec(self,v):
        v=v-self.world_center
        v/=self.zoom
        r,phi=v.as_polar()
        phi-=self.world_angle+self.view_angle
        v.from_polar((r,phi))
        v+=self.view_center
        return v
