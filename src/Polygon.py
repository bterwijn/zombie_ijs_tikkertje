import pygame

class Polygon:
    color=pygame.Color(255,255,255)
    
    def __init__(self,points=[]):
        self.points=points

    def add_point(self,point):
        self.points.append(point)

    def draw(self,screen):
        for i in range(-1,len(self.points)-1):
            p1=self.points[i]
            p2=self.points[i+1]
            pygame.draw.line(screen, Polygon.color, p1, p2)
