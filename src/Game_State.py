import pygame

import Player
import Polygon
import Viewport
import Frame

class Game_State:

    def __init__(self):
        self.players={}
        self.polygons=[]
        self.add_polygons()
        
    def add_polygons(self):
        p=Polygon.Polygon([pygame.Vector2(10,10),pygame.Vector2(300,10),pygame.Vector2(100,300)])
        self.polygons.append(p)
        p=Polygon.Polygon([pygame.Vector2(400,300),pygame.Vector2(500,360),pygame.Vector2(450,500)])
        self.polygons.append(p)

    def get_player(self,name):
        return self.players.get(name,None)
        
    def update(self,elapsed_time,actions):
        for name,action_list in actions.get_actions().items():
            if name not in self.players:
                print("new player:",name)
                self.players[name]=Player.Player(pygame.Vector2(400,400))
            self.players[name].update(action_list)
            
    def draw(self,screen,frame_history):
        viewport=self.get_viewport(screen,frame_history)
        screen.fill((0,0,0))
        for polygon in self.polygons:
            polygon.draw(screen,viewport)
        for name,player in self.players.items():
            player.draw(screen,viewport)
        pygame.display.flip()

    def get_viewport(self,screen,frame_history):
        if len(frame_history)>0:
            player_frame=frame_history[0]
        else:
            player_frame=Frame.Frame(pygame.Vector2(0,0),0)
        size=pygame.Vector2(screen.get_size())
        screen_frame=Frame.Frame(pygame.Vector2(size[0]/2,2*size[1]/3),90)
        return Viewport.Viewport(player_frame,screen_frame,2)
        
        
