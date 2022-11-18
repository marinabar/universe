import pygame, random
from pygame.locals import *
import pygame.freetype

#defining screen parameters
LARGEUR_ECRAN = 1080
HAUTEUR_ECRAN = 720


# Sprite base for planets
class Planet(pygame.sprite.Sprite):
    pass


# Star Sprite
class Star(pygame.sprite.Sprite):
    pass


# load images
starbackground = pygame.image.load("night.jpg")
starbackground = pygame.transform.scale(starbackground,
                                        (LARGEUR_ECRAN, HAUTEUR_ECRAN))

# start pygame
pygame.init()
pygame.display.set_caption('Universe')
displaysurf = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))

#initializing background music
pygame.mixer.init()
pygame.mixer.music.load("space.ogg")
pygame.mixer.music.play()


#init font
font = pygame.freetype.SysFont('Times New Roman', 30)

#buttons
couleur_rect = [230, 219, 255]
posmain = [
    LARGEUR_ECRAN - LARGEUR_ECRAN // 4 - 50, 30, LARGEUR_ECRAN // 4,
    HAUTEUR_ECRAN * 0.6 - 60
]  #coordinates main rectangle
grey = pygame.Rect(posmain)
button_random = pygame.Rect(posmain[0] + 30, posmain[1] + 300, 90, 50)
button_cree = pygame.Rect(posmain[0] + 60 + 90, posmain[1] + 300, 90, 50)

# main loop
run = True
while run:
    displaysurf.blit(starbackground, (0, 0))

    mouse = pygame.mouse.get_pos()
    pygame.draw.rect(displaysurf, couleur_rect, grey,
                     border_radius=5)  # draw rectangle containing buttons
    pygame.draw.rect(displaysurf, [65, 63, 70], button_random,
                     border_radius=5)  #draw randomizer button
    pygame.draw.rect(displaysurf, [65, 63, 70], button_cree,
                     border_radius=5)  #draw create button

    for event in pygame.event.get():
        #check if quit event
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # stores the (x,y) coordinates into the variable as a tuple
            # checks if mouse position is over the button
            if button_cree.collidepoint(mouse_pos):
                # prints current location of mouse
                print('CREATE was pressed at {0}'.format(mouse_pos))
            if button_random.collidepoint(mouse_pos):
                # prints current location of mouse
                print('RANDOM was pressed at {0}'.format(mouse_pos))

    pygame.display.update()

pygame.quit()
