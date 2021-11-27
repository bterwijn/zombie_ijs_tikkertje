import sys
import zmq
import time

import pygame

import Action
import Actions
import Game_State

def main():
    game_server=Game_Server(*sys.argv[1:])
    game_server.run()

class Game_Server:
    game_fps=55
    
    def __init__(self,port="2222",host="0.0.0.0"):
         context = zmq.Context()
         self.socket = context.socket(zmq.REP)
         self.socket.bind("tcp://"+host+":"+port)
         print("waiting for clients on server",host,"on port",port)
         
    def run(self):
        game_state = Game_State.Game_State( pygame.Vector2(800, 600) )
        start_time = time.time()
        actions = Actions.Actions()
        while True:
            action = self.socket.recv_pyobj()            # receive action
            actions.add_action(action)                   # store action
            self.socket.send_pyobj(game_state)           # send game_state asap

            now = time.time()
            elapsed_time = now - start_time
            if elapsed_time > 1/self.game_fps:           # check for frame rate 
                game_state.update(elapsed_time,actions)  # update game_state
                actions.clear()                          # forget earlier actions
                start_time = now                         # update start time 
                
if __name__ == "__main__":
    main()
    
