import sys
import zmq
import time

import pygame

import Action
import Game_State

class Game_Client:
    game_fps=55
    
    def __init__(self,name,host="127.0.0.1",port="2222"):
        self.name=name
        context = zmq.Context()
        print("Connecting as '",name,"' to server",host,"on port",port)
        self.socket = context.socket(zmq.REQ)
        self.socket.connect ("tcp://"+host+":"+port)
        print("Connected")
        
    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        game_state=None
        clock = pygame.time.Clock()
        self.running = True        
        while self.running:
            self.socket.send_pyobj(self.get_action())  # send action
            if game_state is not None:
                game_state.draw(screen)                # draw game state
            clock.tick(self.game_fps)                  # sleep to limit frame rate
            game_state = self.socket.recv_pyobj()      # receive game state
        pygame.quit()
            
    def get_action(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event)
            if event.type == pygame.MOUSEBUTTONUP:
                print(event)
        keys=pygame.key.get_pressed()
        accel=pygame.Vector2( -1 if keys[pygame.K_LEFT] else 0 + +1 if keys[pygame.K_RIGHT] else 0, \
                              +1 if keys[pygame.K_DOWN] else 0 + -1 if keys[pygame.K_UP]    else 0 )
        return Action.Action(self.name,accel)
            
if __name__ == "__main__":
    if len(sys.argv)>1:
        game_client=Game_Client(*sys.argv[1:])
        game_client.run()
    else:
        print("usage: ",sys.argv[0],"<name> [host] [port] ")
    
