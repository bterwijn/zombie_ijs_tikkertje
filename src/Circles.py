import pygame
import Circle

class Circles:
    
    def __init__(self):
        self.circles=[]

    def add_circle(self,circle):
        self.circles.append(circle)

    def random(n,min_pos,max_pos,min_radius,max_radius,min_color,max_color):
        circles=Circles()
        for i in range(n):
            circles.add_circle(Circle.Circle.random(min_pos,max_pos,min_radius,max_radius,min_color,max_color))
        return circles
        
    def draw(self,screen,viewport):
        for c in self.circles:
            c.draw(screen,viewport)
