
import pygame

import Player
import Polygon

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

    def update(self,elapsed_time,actions):
        for name,action_list in actions.get_actions().items():
            if name not in self.players:
                print("new player:",name)
                self.players[name]=Player.Player(pygame.Vector2(400,400))
            self.players[name].update(action_list)
            
    def draw(self,screen):
        screen.fill((0,0,0))
        for polygon in self.polygons:
            polygon.draw(screen)
        for name,player in self.players.items():
            player.draw(screen)
        pygame.display.flip()
