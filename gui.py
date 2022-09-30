from curses import COLOR_GREEN, COLOR_WHITE, KEY_DOWN

import pygame
from client import Client

WIDTH, HEIGHT = 800, 600
pygame.init()
pygame.display.set_caption("Messanger")
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.Font(None, 16)

class Gui():

    
    def __init__(self):
        
        
        self.connected = True

        self.client = Client()

        self.message_input_box = InputBox(WIDTH / 2 - 150, HEIGHT-50, 300, 20, "Type your message")
        self.conversation_field = ConversationField(WIDTH, HEIGHT-200)
        #self.client.connect_client()
        self.conversation_field.add_message(Message("Hello hier ist Julatsdfsdfsjdfjskd", True, WIDTH))
        self.conversation_field.add_message(Message("Hello 2", False, WIDTH))
        
        while self.connected:

            clock.tick(60)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.connected = False
                    self.disconnect_user()
                    break

                if event.type == pygame.K_SPACE:
                    pass

                
                self.message_input_box.handle_event(event)

            screen.fill((255,255,255))
            self.message_input_box.draw(screen)
            self.conversation_field.draw(screen)
            

            pygame.display.flip()
        pygame.quit()
        
    def disconnect_user(self):
        self.client.send_msg("!disconnect")
    #def send_msg(self):
       # self.client.send_msg("TEST MESSAGE")

class InputBox():
    def __init__(self, x, y, w, h, title):
        self.rect = pygame.Rect(x,y,w,h)
        self.text = ""
        self.COLOR_INACTIVE = (100, 100, 100)
        self.COLOR_ACTIVE = (66, 135, 245)
        self.color = self.COLOR_INACTIVE
        self.txt_surface = FONT.render(self.text, True, self.COLOR_INACTIVE)
        self.title_surface = FONT.render(title, True, self.COLOR_INACTIVE)
        self.active = False
        
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = self.COLOR_ACTIVE
            else:
                self.active = False
                self.color = self.COLOR_INACTIVE
            
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    pass
                    # send message
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if self.txt_surface.get_width() < self.rect.width-20:
                        self.text += event.unicode
                
                self.txt_surface = FONT.render(self.text, True, self.COLOR_INACTIVE)
    
    
    def draw(self, screen):
        screen.blit(self.title_surface, (self.rect.x + 10, self.rect.y - 20))
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y +5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def submit_text(self):
        return self.text


class ConversationField():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.box = pygame.Rect(10, 10, width-20, height+10)
        self.surface1 = pygame.Surface((width, height), flags=pygame.SRCALPHA)
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)

    def render_conversation(self):
        y = 20
        delta_y = 20
        for message in self.messages:
                

            self.surface1.blit(message.get_text_surface(), (20, y))
            y += delta_y
    
    def draw(self, screen):
        self.render_conversation()
        screen.blit(self.surface1, (0, 0))
        pygame.draw.rect(screen, (100, 100, 100), self.box, 2)

class Message():
    def __init__(self, content, my_message, field_width):
        self.content = content
        self.MY_COLOR = (52, 235, 58)
        self.PARTNER_COLOR = (52, 150, 235)

        self.color = self.MY_COLOR
    
        self.my_message = my_message
        if my_message:
            self.color = self.MY_COLOR 
        else:
            self.color = self.PARTNER_COLOR
        

        self.text_surface = FONT.render(self.content, True, self.color)

        #if it's my own message it should be on the left
        if self.my_message:


            x = (field_width - self.text_surface.get_width())/3.2
            print(self.text_surface.get_width())
            x = int(x)
            print(x)
            s = ""
            for i in range(x):
                s += " "
        
            self.content = s + self.content
            self.text_surface = FONT.render(self.content, True, self.color)

    def get_content(self):
        return self.content
    
    def set_content(self, content):
        self.content = content
        self.text_surface = FONT.render(self.content, True, self.color)
    
    def get_text_surface(self):
        return self.text_surface


    def is_my_message(self):
        return self.my_message


class Button:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

Gui()