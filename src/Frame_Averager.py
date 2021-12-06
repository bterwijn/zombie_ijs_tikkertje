import pygame

import Frame

def main():
    frame_averager=Frame_Averager()
    frame=Frame.Frame(pygame.Vector2(0,0),0)
    for i in range(40):
        print(frame,"---",frame_averager.update(frame,0.1), "---",frame_averager)
        frame.pos.x=i
    
class Frame_Averager:

    def __init__(self):
        self.first=True
        self.pos=None
        self.angle=None
        
    def __repr__(self):
        return f"{self.pos} {self.angle}"

    def update(self,frame,weight):
        cartesian=pygame.Vector2(0,0)
        cartesian.from_polar((1.0,frame.angle))
        if self.first:
            self.pos=(frame.pos*1)
            self.angle=cartesian
            self.first=False
        else:
            self.pos+=frame.pos*weight
            self.angle+=cartesian*weight
            self.pos/=(1.0+weight)
            self.angle/=(1.0+weight)
        r,phi=self.angle.as_polar() 
        nf=Frame.Frame(self.pos,phi)
        return nf

if __name__ == "__main__":
    main()
