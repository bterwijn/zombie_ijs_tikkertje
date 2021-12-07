import pygame
import random

class Circle:
    
    def __init__(self,pos,radius,color):
        self.pos=pos
        self.radius=radius
        self.color=color

    def random(min_pos,max_pos,min_radius,max_radius,min_color,max_color):
        pos=pygame.Vector2(min_pos.x+(max_pos.x-min_pos.x)*random.random(),
                           min_pos.y+(max_pos.y-min_pos.y)*random.random())
        radius=min_radius+(max_radius-min_radius)*random.random()
        c=round(min_color+(max_color-min_color)*random.random())
        color=pygame.Color(c,c,c)
        return Circle(pos,radius,color)
        
    def draw(self,screen,viewport):
        pygame.draw.circle(screen, self.color, viewport.tranform_vec(self.pos), viewport.transform(self.radius), 1)
