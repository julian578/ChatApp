import pygame
import client

WIDTH, HEIGHT = 800, 600
pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.Font(None, 16)



class Gui():

    
    def __init__(self):
        
        
        self.connected = True


        self.message_input_box = InputBox(WIDTH / 2 - 150, HEIGHT-50, 300, 20, "Type your message", "Send")
        self.conversation_field = ConversationField(WIDTH, HEIGHT-200)

        
        while self.connected:

            clock.tick(60)
            events = pygame.event.get()
            if client.new_messages:
                for msg in client.new_messages:
                    self.conversation_field.add_message(Message(msg[0], msg[1], WIDTH))
                client.new_messages.clear()
            for event in events:
                if event.type == pygame.QUIT:
                    self.connected = False
                    self.disconnect_user()
                    break

                if event.type == pygame.K_SPACE:
                    pass

                
                self.message_input_box.handle_event(event)
                self.conversation_field.handle_scrolling(event)

            screen.fill((255,255,255))
            self.message_input_box.draw(screen)
            self.conversation_field.draw(screen)

            

            pygame.display.flip()
        pygame.quit()
        
    def disconnect_user(self):
        client.send_msg("!disconnect")
    

class InputBox():
    def __init__(self, x, y, w, h, title, button_title):
        self.rect = pygame.Rect(x,y,w,h)
        self.text = ""
        self.COLOR_INACTIVE = (100, 100, 100)
        self.COLOR_ACTIVE = (66, 135, 245)
        self.color = self.COLOR_INACTIVE
        self.txt_surface = FONT.render(self.text, True, self.COLOR_INACTIVE)
        self.title_surface = FONT.render(title, True, self.COLOR_INACTIVE)
        self.active = False
        self.submit_button = Button(x+w+10, y,40, 20, button_title)

    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = self.COLOR_ACTIVE
            elif self.submit_button.rect.collidepoint(event.pos):
                self.submit_button.handle_button_press(self.text)
                self.text = ""
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
        self.submit_button.draw(screen)

    def submit_text(self):
        return self.text


#window with messages
class ConversationField():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.box = pygame.Rect(10, 10, width-20, height+10)
        self.surface1 = pygame.Surface((width, height), flags=pygame.SRCALPHA)
        self.messages = []

        #visible part of the scrolling field
        self.start = 0
        self.end = len(self.messages)

    def add_message(self, message):
        self.messages.append(message)
        self.end += 1
        if self.end > self.height / 21:
            self.start += 1

    def render_conversation(self):
        y = 20
        delta_y = 20


        empty = (0,0,0,0)
        self.surface1.fill(empty)
        for i in range(self.start, self.end):

            self.surface1.blit(self.messages[i].get_text_surface(), (20, y))
            
            y += delta_y
    
    def handle_scrolling(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            #scrolling up
            if event.button == 4 and self.start > 0:
                self.start -= 1
                self.end -= 1
            elif event.button == 5 and self.end < len(self.messages):
                #scrolling down
                self.start += 1
                self.end += 1
    
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

            x = int(x)

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

    def __init__(self, x, y, width, height, title):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        self.color = (0,0,0)
        self.rect = pygame.Rect(x,y,width,height)
        self.txt_surface = FONT.render(self.title, True, self.color)
    
    def handle_button_press(self, message_input):
        msg = message_input

        client.send_msg(msg)

    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))

if __name__ == "__main__":

    print("type in your username")
    client.USERNAME = input()
    pygame.display.set_caption(f"{client.USERNAME}'s Messanger")
    client.connect_client()
    Gui()