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
            
    def draw(self,screen,name):
        viewport=self.get_viewport(screen,name)
        screen.fill((0,0,0))
        for polygon in self.polygons:
            polygon.draw(screen,viewport)
        for name,player in self.players.items():
            player.draw(screen,viewport)
        pygame.display.flip()

    def get_viewport(self,screen,name):
        if name in self.players:
            player_frame=self.players[name].get_frame()
        else:
            player_frame=Frame.Frame(pygame.Vector2(0,0),0)            
        screen_frame=Frame.Frame(pygame.Vector2(screen.get_size())/2,90)
        return Viewport.Viewport(player_frame,screen_frame,2)
        
        
