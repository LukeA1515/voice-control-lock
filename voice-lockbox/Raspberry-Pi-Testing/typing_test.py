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

os.putenv('SDL_VIDEODRV','fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV','dummy')
os.putenv('SDL_MOUSEDEV','/dev/null')
os.putenv('DISPLAY','')

# bail out button 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.IN)

def GPIO17_callback(channel): 
    pygame.quit()
    sys.exit(0)

GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)

# Initialize Pygame
pygame.init()
pitft = pigame.PiTft()
# Screen dimensions
WIDTH, HEIGHT = 320, 240
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)

# Font
font = pygame.font.Font(None, 36)

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

# State variables
typed_word = ""
current_input = ""
current_index = 0
current_key = None
green_button_count = 0
keyboard_visible = True

# Helper to draw text on a button
def draw_button(x, y, width, height, text, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    label = font.render(text, True, BLACK)
    label_rect = label.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(label, label_rect)

def is_clicked(obj):
    return obj.rect.collidepoint(pos)
# Main loop
running = True
while running:
    pitft.update()
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and keyboard_visible:
            x, y = event.pos

            # Check for button presses
            for i, (bx, by, label, chars) in enumerate(buttons):
                if bx <= x <= bx + button_width and by <= y <= by + button_height:
                    if current_key == i:
                        current_index = (current_index + 1) % len(chars)
                    else:
                        current_key = i
                        current_index = 0
                    current_input = chars[current_index]

            # Check for green button
            gx, gy, gtext = green_button
            if gx <= x <= gx + button_width and gy <= y <= gy + button_height:
                if current_input:
                    typed_word += current_input
                    current_input = ""
                    current_key = None
                    green_button_count += 1
                else :
                    keyboard_visible = False

    # Render typed word
    word_label = font.render(typed_word, True, BLACK)
    word_rect = word_label.get_rect(center=(156, 15))
    screen.blit(word_label, word_rect)

    if keyboard_visible:
        # Draw buttons
        for bx, by, label, chars in buttons:
            draw_button(bx, by, button_width, button_height, label, GRAY)

        # Draw green button
        gx, gy, gtext = green_button
        draw_button(gx, gy, button_width, button_height, gtext, GREEN)

    else:
        # Show final word in the center
        screen.fill(WHITE)
        final_label = font.render(typed_word, True, BLACK)
        final_rect = final_label.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(final_label, final_rect)
        time.sleep(3)
        running = False


    pygame.display.flip()


pygame.quit()
sys.exit()
