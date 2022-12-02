import pygame, random
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
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
button_random = pygame.Rect(posmain[0] + 30, posmain[1] + 320, 90, 30)
button_cree = pygame.Rect(posmain[0] + 60 + 90, posmain[1] + 320, 90, 30)

#sliders - il faut en faire 8 - site python-widgets
bgcolor = (65, 63, 70)
tcolor = couleur_rect

slidertaille = Slider(displaysurf,
                      posmain[0] + 30,
                      posmain[1] + 25 + 18 * 1 + 15 * 1,
                      posmain[2] // 2,
                      40,
                      min=1,
                      max=10,
                      step=1)
label_slider_taille = TextBox(displaysurf,
                              posmain[0] + 30,
                              posmain[1] + 30,
                              10,
                              10,
                              fontSize=10,
                              borderThickness=1)
label_slider_taille.disable()
labeltaille = TextBox(
    displaysurf,
    posmain[0] + 20,
    posmain[1] + 25 + 18 * 1 + 15 * 1,
    #position du rectangle gris + décalage + taille texte + taille padding
    0,
    0,
    fontSize=23,
    borderThickness=0)
labeltaille.disable()
labeltaille.setText("Taille : ")

labeluniv = TextBox(displaysurf,
                    posmain[0] + 40,
                    posmain[1] + 35,
                    0,
                    0,
                    fontSize=25,
                    textColour=bgcolor,
                    borderThickness=0)
labeluniv.disable()
labeluniv.setText("Crée ton univers !")

slidermasse = Slider(displaysurf,
                     100,
                     100,
                     800,
                     40,
                     min=1,
                     max=10,
                     step=1,
                     curved=False)
labelmasse = TextBox(displaysurf,
                     posmain[0] + 30,
                     200,
                     50,
                     50,
                     fontSize=30,
                     radius=10,
                     borderThickness=0)
labelmasse.disable()
labelmasse.setText("Masse : ")

tempinput = TextBox(displaysurf,
                    posmain[0] + 30,
                    200,
                    50,
                    50,
                    fontSize=30,
                    radius=10,
                    borderThickness=0)
templabel = TextBox(displaysurf,
                    posmain[0] + 30,
                    200,
                    50,
                    50,
                    fontSize=30,
                    radius=10,
                    borderThickness=0)
templabel.disable()
templabel.setText("Température : ")

typelabel = TextBox(displaysurf,
                    posmain[0] + 30,
                    200,
                    50,
                    50,
                    fontSize=30,
                    radius=10,
                    borderThickness=0)
typelabel.disable()
typelabel.setText("Type : ")
typeinput = TextBox(displaysurf,
                    posmain[0] + 30,
                    200,
                    50,
                    50,
                    fontSize=30,
                    radius=10)  #séléction de type

slidernbplant = Slider(displaysurf, 100, 100, 800, 40, min=1, max=10, step=1)
labelnbplant = TextBox(displaysurf,
                       posmain[0] + 30,
                       200,
                       50,
                       50,
                       fontSize=30,
                       radius=10,
                       borderThickness=0,
                       textColour=bgcolor)
labelnbplant.disable()
labelnbplant.setText("Nombre de planètes : ")

aleatoire = TextBox(displaysurf,
                    posmain[0] + 28,
                    posmain[1] + 350,
                    0,
                    0,
                    fontSize=27,
                    borderThickness=0,
                    textColour=tcolor)
aleatoire.disable()
aleatoire.setText("Aléatoire")

cree = TextBox(displaysurf,
               posmain[0] + 65 + 90,
               posmain[1] + 350,
               0,
               0,
               fontSize=27,
               borderThickness=0,
               textColour=tcolor)
cree.disable()
cree.setText("Crée")

# main loop
run = True
while run:
    events = pygame.event.get()
    displaysurf.blit(starbackground, (0, 0))

    pygame.draw.rect(displaysurf, couleur_rect, grey,
                     border_radius=5)  # draw rectangle containing buttons
    pygame.draw.rect(displaysurf, [65, 63, 70], button_random,
                     border_radius=5)  #draw randomizer button
    pygame.draw.rect(displaysurf, [65, 63, 70], button_cree,
                     border_radius=5)  #draw create button

    label_slider_taille.setText(slidertaille.getValue())
    labelmasse.setText(slidermasse.getValue())
    labelnbplant.setText(slidernbplant.getValue())

    for event in events:
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

    pygame_widgets.update(events)
    pygame.display.update()

pygame.quit()
