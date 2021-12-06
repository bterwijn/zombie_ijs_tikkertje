import pygame

class Frame:

    def __init__(self,pos,angle):
        self.pos=pos
        self.angle=angle
        
    def __repr__(self):
        return f"{self.pos}:{self.angle}"

    def zero():
        return Frame(pygame.Vector2(0,0),0)
