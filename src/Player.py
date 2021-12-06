import random
import pygame

import Frame

class Player:
    line_width=1
    
    def __init__(self,pos):
        self.frame=Frame.Frame(pos,0)
        self.speed=pygame.Vector2(0,0)
        self.radius=20
        self.color=pygame.Color(random.randint(100,255),random.randint(100,255),random.randint(100,255))

    def get_frame(self):
        return self.frame
        
    def update(self,action_list):
        thrust_sum=0
        rotation_sum=0
        if len(action_list)>0:
            for a in action_list:
                thrust_sum+=a.thrust
                rotation_sum+=a.rotation
            thrust_sum/=len(action_list)
            rotation_sum/=len(action_list)
            self.frame.angle+=rotation_sum
            accel=pygame.Vector2(0,0)
            accel.from_polar((thrust_sum, self.frame.angle))
            self.speed+=accel
        self.frame.vector+=self.speed
        self.speed*=0.98
  
    def draw(self,screen,viewport):
        pygame.draw.circle(screen, self.color, viewport.tranform_vec(self.frame.vector), viewport.transform(self.radius), self.line_width)
        line=pygame.Vector2(0,0)
        line.from_polar((self.radius*2, self.frame.angle))
        pygame.draw.line(screen, self.color, viewport.tranform_vec(self.frame.vector), viewport.tranform_vec(self.frame.vector+line), self.line_width )
