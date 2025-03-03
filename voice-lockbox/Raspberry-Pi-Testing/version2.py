fimport sys
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

GLED = LED(5)
RLED = LED(6)

name = " "
password_text = " "
password = " "
show_say = False
show_pass = False

# bail out button 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.IN)

def GPIO17_callback(channel): 
    pygame.quit()
    sys.exit(0)

GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)

# display on pi

os.putenv('SDL_VIDEODRV','fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV','dummy')
os.putenv('SDL_MOUSEDEV','/dev/null')
os.putenv('DISPLAY','')

factory = PiGPIOFactory()
servo = AngularServo(26, min_pulse_width=0.0005, max_pulse_width=0.0023, initial_angle=-62, pin_factory=factory)

def open_door():
    final = 0
    i =  -62
    while i < final:
        servo.angle = i
        i+= 2
        time.sleep(0.05)

def close_door():
    final = -64
    i =  0
    while i > final:
        servo.angle = i
        i-= 2
        time.sleep(0.05)

# Initialize Pygame
pygame.init()
pygame.mouse.set_visible(False)   
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
dummy_button = Button("Dummy", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 30, 10, RED)
return_button = Button("Return Home", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50, GRAY)


#Text
say_something_button = Button("Speak your password", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50, WHITE)
# password_button = Button(password_text, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 3 - 50, 200, 50, WHITE)

# Register Task; Adding a User
def register_task():
    say_something_button.draw(screen)
    pygame.display.flip()
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    try:
        password = r.recognize_wit(audio, key=WIT_AI_KEY)
        print("Wit.ai thinks you said/password " + password)
        global password_text
        password_text = "Password: " + password
        screen.fill(WHITE)
        password_button = Button(password_text, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50, WHITE)
        password_button.draw(screen)
        pygame.display.flip()
        time.sleep(3)
        with open("data.json", 'r') as f:
            data = json.load(f)

        data[name] = password
        with open("data.json", 'w') as f:
            json.dump(data,f)
            
    except sr.UnknownValueError:
        print("Wit.ai could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Wit.ai service; {0}".format(e))
        # GPIO17_callback()


# Show that door is opening
def open_task():
    say_something_button.draw(screen)
    pygame.display.flip()
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    try:
        password = r.recognize_wit(audio, key=WIT_AI_KEY)
        global open_val
        with open("data.json", 'r') as f:
            data = json.load(f)
        
        if data[name] == password:
            open_val = True
            screen.fill(WHITE)
            open_button = Button("OPENING DOOR", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50, GREEN)
            open_button.draw(screen)
            pygame.display.flip()
            GLED.on()
            RLED.off()
            open_door()
            time.sleep(3)
            close_door()
            RLED.on()
            GLED.off()


        else:
            open_val = False
            screen.fill(WHITE)
            open_button = Button("PASSWORD REJECTED", SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 25, 300, 50, RED)
            open_button.draw(screen)
            pygame.display.flip()
            time.sleep(3)
            
    except sr.UnknownValueError:
        print("Wit.ai could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Wit.ai service; {0}".format(e))
        # GPIO17_callback()

# Name Intake 
def name_task():
    global name
    screen.fill(WHITE)
    name_button = Button("Type Name", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50, WHITE)
    name_button.draw(screen)
    pygame.display.flip()
    global name
    global val
    name = typing_task()
    display_button = Button("Name: " + name, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50, WHITE)
    inv_button = Button("INVALID ", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50, WHITE)
    with open("data.json", 'r') as f:
        data = json.load(f)

    if name in data:
        screen.fill(WHITE)
        inv_button.draw(screen)
        pygame.display.flip()
        time.sleep(3)
        val = False

    else:
        screen.fill(WHITE)
        display_button.draw(screen)
        pygame.display.flip()
        time.sleep(3)
        val = True

    
# Determing if a user is in the system
def identity_task():
    global name
    screen.fill(WHITE)
    name_button = Button("Type Name", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50, WHITE)
    name_button.draw(screen)
    pygame.display.flip()
    global name
    global val2
    name = typing_task()
    display_button = Button("MATCH: " + name, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50, WHITE)
    inv_button = Button("INVALID NAME", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50, WHITE)
    with open("data.json", 'r') as f:
        data = json.load(f)

    if name in data:
        screen.fill(WHITE)
        display_button.draw(screen)
        pygame.display.flip()
        time.sleep(3)
        val2 = True

    else:
        screen.fill(WHITE)
        inv_button.draw(screen)
        pygame.display.flip()
        time.sleep(3)
        val2 = False

def typing_task():
    helper = ""
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
            # checking if keydown event happened or not
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    helper += "a"
                if event.key == pygame.K_b:
                    helper += "b"
                if event.key == pygame.K_c:
                    helper += "c"
                if event.key == pygame.K_d:
                    helper += "d"
                if event.key == pygame.K_e:
                    helper += "e"
                if event.key == pygame.K_f:
                    helper += "f"
                if event.key == pygame.K_g:
                    helper += "g"
                if event.key == pygame.K_h:
                    helper += "h"
                if event.key == pygame.K_i:
                    helper += "i"
                if event.key == pygame.K_j:
                    helper += "j"
                if event.key == pygame.K_k:
                    helper += "k"
                if event.key == pygame.K_l:
                    helper += "l"
                if event.key == pygame.K_m:
                    helper += "m"
                if event.key == pygame.K_n:
                    helper += "n"
                if event.key == pygame.K_o:
                    helper += "o"
                if event.key == pygame.K_p:
                    helper += "p"
                if event.key == pygame.K_q:
                    helper += "q"
                if event.key == pygame.K_r:
                    helper += "r"
                if event.key == pygame.K_s:
                    helper += "s"
                if event.key == pygame.K_t:
                    helper += "t"
                if event.key == pygame.K_u:
                    helper += "u"
                if event.key == pygame.K_v:
                    helper += "v"
                if event.key == pygame.K_w:
                    helper += "w"
                if event.key == pygame.K_x:
                    helper += "x"
                if event.key == pygame.K_y:
                    helper += "y"
                if event.key == pygame.K_z:
                    helper += "z"
                if event.key == pygame.K_RETURN:
                    run = False
    return helper
    
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



# Helper to draw text on a button
def draw_button(x, y, width, height, text, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    label = font.render(text, True, BLACK)
    label_rect = label.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(label, label_rect)

# Game loop
running = True
while running:
    pitft.update()
    pos = pygame.mouse.get_pos()  # Get the mouse position
    screen.fill(WHITE)  # Clear the screen
    RLED.on()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == "start":
                if register_button.is_clicked(pos):
                    name_task()
                    if not val:
                        current_state = "start"
                    else:
                        current_state = "register"
                elif open_button.is_clicked(pos):
                    identity_task()
                    if not val2:
                        current_state = "start"
                    else:
                        open_task()
                        current_state = "record"
                elif quit_button.is_clicked(pos):
                    running = False
            elif current_state == "name":
                name_task()
                if not val:
                    current_state = "start"
                else: 
                    current_state = "register"

            elif current_state == "register":
                if record_button.is_clicked(pos):
                    current_state = "record"
                    register_task()

            elif current_state == "open":
                if listen_button.is_clicked(pos):
                    current_state = "start"

            elif current_state == "record":
                if return_button.is_clicked(pos):
                    current_state = "start"

    # Draw the appropriate state in the same loop
    draw_state()
    pygame.display.flip()

pygame.quit()
sys.exit()



