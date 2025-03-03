import sys
import speech_recognition as sr
import time
import json
import RPi.GPIO as GPIO
import os
import sys 
from time import sleep
import pygame
import pygame,pigame
from pygame.locals import *
import RPi.GPIO as GPIO
from gpiozero import AngularServo
from gpiozero import LED 
from gpiozero.pins.pigpio import PiGPIOFactory

WIT_AI_KEY = ""

GREEN_LED = LED(5)
RED_LED = LED(6)

# bail out button 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.IN)

def GPIO17_callback(channel): 
    pygame.quit()
    sys.exit(0)

GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)

# display on pi

# os.putenv('SDL_VIDEODRV','fbcon')
# os.putenv('SDL_FBDEV', '/dev/fb1')
# os.putenv('SDL_MOUSEDRV','dummy')
# os.putenv('SDL_MOUSEDEV','/dev/null')
# os.putenv('DISPLAY','')


# Initialize Pygame
pygame.init()
# pygame.mouse.set_visible(False)   
pitft = pigame.PiTft()

# Screen dimensions and settings
SCREEN_WIDTH, SCREEN_HEIGHT = 320, 240
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("State Machine Example")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.Font(None, 30)

# Button class
class Button:
    def __init__(self, text, x, y, width, height, color, text_color=BLACK):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text_color = text_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Type_Button:
    def __init__(self, text, x, y, width, height, color, text_color=BLACK, count=0):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text_color = text_color
        self.count = count

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        self.count += 1
        return self.rect.collidepoint(pos)

    def count_reset(self):
        self.count = 0
    
key_mappings = {
    0: "ABC", 1: "DEF", 2: "GHI", 3: "JKL",
    4: "MNO", 5: "PQR", 6: "STU", 7: "VWX", 8: "YZ"
}

button_width, button_height = 80, 40

button_0 = Type_Button("A B C", 25, 40, button_width, button_height, GRAY)
button_1 = Type_Button("D E F", 115, 40, button_width, button_height, GRAY)
button_2 = Type_Button("G H I", 205, 40, button_width, button_height, GRAY)
button_3 = Type_Button("J K L", 25, 90, button_width, button_height, GRAY)
button_4 = Type_Button("M N O", 115, 90, button_width, button_height, GRAY)
button_5 = Type_Button("P Q R", 205, 90, button_width, button_height, GRAY)
button_6 = Type_Button("S T U", 25, 140, button_width, button_height, GRAY)
button_7 = Type_Button("V W X", 115, 140, button_width, button_height, GRAY)
button_8 = Type_Button(" Y Z ", 205, 140, button_width, button_height, GRAY)
button_save = Type_Button("Save", 115, 190, button_width, button_height, GREEN)









    

# State management
current_state = "start"

def draw_state():
    screen.fill(WHITE)
    if current_state == "start":
        register_button.draw(screen)
        open_button.draw(screen)
        quit_button.draw(screen)
    elif current_state == "register":
        record_button.draw(screen)
    elif current_state == "record":
        return_button.draw(screen)
    elif current_state == "open":
        listen_button.draw(screen)

# Buttons
register_button = Button("Register", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 3 - 50, 200, 50, GRAY)
open_button = Button("Open", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50, GRAY)
quit_button = Button("Quit", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT * 2 // 3, 200, 50, GRAY)
record_button = Button("Record", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50, RED)
listen_button = Button("Listen", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50, RED)
dummy_button = Button("FUCK FUCK", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 3-50, 200, 50, RED)
return_button = Button("Return Home", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50, GRAY)


#Text
say_something_button = Button("Speak your password", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50, WHITE)
# password_button = Button(password_text, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 3 - 50, 200, 50, WHITE)



    
# Button configuration
button_width, button_height = 80, 40
button_margin = 10

# Mappings
key_mappings = {
    0: "ABC", 1: "DEF", 2: "GHI", 3: "JKL",
    4: "MNO", 5: "PQR", 6: "STU", 7: "VWX", 8: "YZ"
}

# Buttons and positions
buttons = []
buttons.append ((25, 40, "A B C", key_mappings[0]))
buttons.append ((115, 40, "D E F", key_mappings[1]))
buttons.append ((205, 40, "G H I", key_mappings[2]))
buttons.append ((25, 90, "J K L", key_mappings[3]))
buttons.append ((115, 90, "M N O", key_mappings[4]))
buttons.append ((205, 90, "P Q R", key_mappings[5]))
buttons.append ((25, 140, "S T U", key_mappings[3]))
buttons.append ((115, 140, "V W X", key_mappings[4]))
buttons.append ((205, 140, "Y Z", key_mappings[5]))
green_button = (115, 190, "Save")

keyboard_visible = False

def onscreen_type():
    # Main loop
    running_type = True
    print("b")
    current_key = None
    typed_word = ""
    while running_type:
        # print("BOB")
        screen.fill(WHITE)
        pos = pygame.mouse.get_pos() 
        button_0.draw(screen)
        button_1.draw(screen)
        button_2.draw(screen)
        button_3.draw(screen)
        button_4.draw(screen)
        button_5.draw(screen)
        button_6.draw(screen)
        button_7.draw(screen)
        button_8.draw(screen)
        button_save.draw(screen)


        pitft.update()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_0.is_clicked(pos):
                    current_key = 1
                    current_index = (button_1.count - 1) % 3
                    current_input = key_mappings[current_key][current_index]
                    print(current_input)
                if button_1.is_clicked(pos):
                    current_key = 1
                    current_index = (button_1.count - 1) % 3
                    current_input = key_mappings[current_key][current_index]
                    print(current_input)
                if button_2.is_clicked(pos):
                    current_key = 2
                    current_index = (button_1.count - 1) % 3
                    current_input = key_mappings[current_key][current_index]
                    print(current_input)
                if button_3.is_clicked(pos):
                    current_key = 3
                    current_index = (button_1.count - 1) % 3
                    current_input = key_mappings[current_key][current_index]
                    print(current_input)
                if button_4.is_clicked(pos):
                    current_key = 4
                    current_index = (button_1.count - 1) % 3
                    current_input = key_mappings[current_key][current_index]
                    print(current_input)
                if button_5.is_clicked(pos):
                    current_key = 5
                    current_index = (button_1.count - 1) % 3
                    current_input = key_mappings[current_key][current_index]
                    print(current_input)
                if button_6.is_clicked(pos):
                    current_key = 6
                    current_index = (button_1.count - 1) % 3
                    current_input = key_mappings[current_key][current_index]
                    print(current_input)
                if button_7.is_clicked(pos):
                    current_key = 7
                    current_index = (button_1.count - 1) % 3
                    current_input = key_mappings[current_key][current_index]
                    print(current_input)
                if button_8.is_clicked(pos):
                    current_key = 8
                    current_index = (button_1.count - 1) % 3
                    current_input = key_mappings[current_key][current_index]
                    print(current_input)

                if button_save.is_clicked(pos):
                    button_1.count_reset()
                    button_2.count_reset()
                    button_3.count_reset()
                    button_4.count_reset()
                    button_5.count_reset()
                    button_6.count_reset()
                    button_7.count_reset()
                    button_8.count_reset()
                    button_save.count_reset()
                    typed_word += current_input
                    print("saved")
                    print(typed_word)

                if button_save.count == 2:
                    running_type = False

        screen.fill(WHITE) 
        return typed_word
         

        # else:
        #     # Show final word in the center
        #     screen.fill(WHITE)
        #     final_label = font.render(typed_word, True, BLACK)
        #     final_rect = final_label.get_rect(center=(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25))
        #     screen.blit(final_label, final_rect)
        #     pygame.display.flip()
        #     time.sleep(3)
        #     running_type = False
    screen.fill(WHITE)  
    word_button = Button(typed_word, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50, WHITE)
    word_button.draw(screen)    
    pygame.display.flip()
    time.sleep(3)
    return "typed_word"

# Helper to draw text on a button
def draw_button(x, y, width, height, text, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    label = font.render(text, True, BLACK)
    label_rect = label.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(label, label_rect)

# Game loop
running = True
while running:
    print(current_state)
    pitft.update()
    pos = pygame.mouse.get_pos()  # Get the mouse position
    screen.fill(WHITE)  # Clear the screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == "start":
                if register_button.is_clicked(pos):
                    # name_task()
                    # if not val:
                    #     current_state = "start"
                    # else:
                    current_state = "start"
                elif open_button.is_clicked(pos):
                    name = onscreen_type()

                elif quit_button.is_clicked(pos):
                    running = False
            # elif current_state == "name":
            #     name_task()
            #     if not val:
            #         current_state = "start"
            #     else: 
            #         current_state = "register"

            # elif current_state == "register":
            #     if record_button.is_clicked(pos):
            #         current_state = "record"
            #         register_task()

            # elif current_state == "open":
            #     if listen_button.is_clicked(pos):
            #         current_state = "start"

            # elif current_state == "record":
            #     if return_button.is_clicked(pos):
            #         current_state = "start"

    # Draw the appropriate state in the same loop
    draw_state()
    pygame.display.flip()

pygame.quit()
sys.exit()


