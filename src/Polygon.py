import pygame

class Polygon:
    color=pygame.Color(255,255,255)
    
    def __init__(self,points=[]):
        self.points=points

    def add_point(self,point):
        self.points.append(point)

    def draw(self,screen,viewport):
        for i in range(-1,len(self.points)-1):
            p1=self.points[i]
            p2=self.points[i+1]
            pygame.draw.line(screen, Polygon.color, viewport.tranform_vec(p1), viewport.tranform_vec(p2))
