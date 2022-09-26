from curses import COLOR_GREEN, COLOR_WHITE
import pygame
from client import Client

class Gui():

    
    def __init__(self):
        
        pygame.init()
        pygame.display.set_caption("Messanger")
        win = pygame.display.set_mode((800, 600))

        background = pygame.Surface((800, 600))
        background.fill('#000000')
    
        self.connected = True

        self.client = Client()

        self.client.connect_client()
        self.client.start_client()


        while self.connected:
            
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.CONNECTED = False
                    break

                if event.type == pygame.K_SPACE:
                    self.send_msg()

            pygame.display.flip()

    
    def send_msg(self):
        self.client.send_msg("TEST MESSAGE")


Gui()