import pygame
from random import randint

pygame.init()

info = pygame.display.Info() # You have to call this before pygame.display.set_mode()
screen_width,screen_height = info.current_w,info.current_h

screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

grid = {}

ant_pos = [0, 0]

screen.fill((255, 255, 255))

pygame.display.update()

def check_ant():
    #check position
    #return a value to determine movement
    return

def move_ant():
    #move the ant
    return

def update_grid():
    #update the grid history
    return

while True:
    screen.fill((255, 255, 255))
    pygame.display.update()
