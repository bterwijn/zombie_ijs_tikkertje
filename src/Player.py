import random
import pygame

class Player:
    line_width=1
    
    def __init__(self,pos):
        self.pos=pos
        self.speed=pygame.Vector2(0,0)
        self.angle=0
        self.radius=20
        self.color=pygame.Color(random.randint(100,255),random.randint(100,255),random.randint(100,255))
        
    def update(self,action_list):
        thrust_sum=0
        rotation_sum=0
        if len(action_list)>0:
            for a in action_list:
                thrust_sum+=a.thrust
                rotation_sum+=a.rotation
            thrust_sum/=len(action_list)
            rotation_sum/=len(action_list)
            self.angle+=rotation_sum
            accel=pygame.Vector2(0,0)
            accel.from_polar((thrust_sum, self.angle))
            self.speed+=accel
        self.pos+=self.speed
        self.speed*=0.98

    def draw(self,screen):
        pygame.draw.circle(screen, self.color, self.pos, self.radius, self.line_width)
        line=pygame.Vector2(0,0)
        line.from_polar((self.radius*2, self.angle))
        pygame.draw.line(screen, self.color, self.pos, self.pos+line ,self.line_width )
