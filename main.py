# on importe les bibliothèques nécessaires
import pygame, random, math
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.dropdown import Dropdown, DropdownChoice
import pygame.freetype

#taille de la fenêtre
LARGEUR_ECRAN = 1080
HAUTEUR_ECRAN = 720

# classe pour créer la planète animée
class animatedCircle:
    def __init__(self,
                 center: tuple,
                 distanceTo0,
                 display,
                 color=(255, 255, 255),
                 size=10,
                 width=0,
                 animationDegree=0):
        self.center = center  # centre de rotation de la sphère, centre de l'orbite
        self.distanceTo0 = distanceTo0  # rayon du cercle correspondant à l'orbite de la sphère
        self.display = display  # surface sur laquelle afficher la sphère
        self.color = color  # couleur de la sphère
        self.size = size  # rayon de la sphère
        self.width = width  # épaisseur de la sphère, si =0 sphère pleine
        self.animationDegree = animationDegree  # mesure de l'angle par rapport à l'axe des abscisses

    def coordinate(self, w: tuple, r: int, teta: int):
        # fonction qui retourne les coordonnées (x,y) en fonction de paramètres de coordonnées polaires
        # w    = centre du repère
        # r    = la distance au centre w
        # teta = mesure de l'angle par rapport à l'axe des abscisses
        rad_teta = math.radians(teta) % (2 * math.pi)
        return (int(r * math.cos(rad_teta) + w[0]),
                int(r * math.sin(rad_teta) + w[1]))

    def incremente_degree(self, val):
        # fonction qui permet d'incrémenter la mesure de l'angle par rapport à l'axe des abscisses
        # autrement dit qui permet d'animer la sphère et de la faire bouger
        self.animationDegree = (self.animationDegree + val) % 360

    def affiche(self):
        # fonction qui permet d'afficher avec le modul pygame la sphère
        pygame.draw.circle(
            self.display, self.color,
            self.coordinate(self.center, self.distanceTo0,
                            self.animationDegree), self.size, self.width)


# création d'un fond d'écran avec une image
starbackground = pygame.image.load("night.jpg")
starbackground = pygame.transform.scale(starbackground,
                                        (LARGEUR_ECRAN, HAUTEUR_ECRAN))

# initialisation de pygame
pygame.init()
pygame.display.set_caption('Universe') # nom de la fenêtre
displaysurf = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))


# couleurs et paramètres de planètes
blue = (0, 0, 255)
red =(255, 0, 0)
MAX = 320 # distance maximale entre le centre du système solaire et la planète
CENTRE=((LARGEUR_ECRAN *3/4)/2-25, 360)
animation = True

# liste des planètes
planet1=animatedCircle(CENTRE,100, displaysurf, red, 15)
planet = animatedCircle(CENTRE, 320, displaysurf, blue, 25) # A CHANGER
listeplan=[planet1, planet]

# rectangle principal contenant la palette de commande
couleur_rect = [230, 219, 255]
posmain = [
    LARGEUR_ECRAN - LARGEUR_ECRAN // 4 - 50, 120, LARGEUR_ECRAN // 4,
    HAUTEUR_ECRAN * 0.6 - 60
]  #coordonnées 

#création des rectangles servant de fond aux boutons random et crée
grey = pygame.Rect(posmain)
button_random = pygame.Rect(posmain[0] + 30, posmain[1] + 320, 90, 30)
button_cree = pygame.Rect(posmain[0] + 60 + 90, posmain[1] + 320, 90, 30)

#palette de couleurs
bgcolor = (65, 63, 70) #couleur foncée
tcolor = couleur_rect #couleur du text
slidercolor = (200, 200, 200) # couleur des sliders

# définition de tous les éléments en utilisant la bibliothèque pygame-widgets
slidertaille = Slider(displaysurf,
                      posmain[0] + 100,
                      posmain[1] + 9 + 18 * 1 + 15 * 1 + 20,
                      width=130,
                      height=5,
                      min=1,
                      max=10,
                      step=1,
                      curved=False)
label_slider_taille = TextBox(
    displaysurf,
    posmain[0] + 100 + 140,  #largeur slider,
    posmain[1] + 23 + 18 * 1 + 15 * 1 + 20,
    0,
    0,
    fontSize=18,
    borderThickness=0)
label_slider_taille.disable() # on le définit comme texte constant qui ne bouge pas
labeltaille = TextBox(
    displaysurf,
    posmain[0] + 30,
    posmain[1] + 25 + 18 * 1 + 15 * 1 + 20,
    #position du rectangle gris + décalage + taille texte + taille padding
    0,
    0,
    fontSize=23,
    borderThickness=0)
labeltaille.disable()
labeltaille.setText("Taille : ")

labeluniv = TextBox(displaysurf,
                    posmain[0] + 53,
                    posmain[1] + 35,
                    0,
                    0,
                    fontSize=25,
                    textColour=bgcolor,
                    borderThickness=0)
labeluniv.disable()
labeluniv.setText("Crée ton univers !")

slidermasse = Slider(displaysurf,
                     posmain[0] + 100,
                     posmain[1] + 9 + 18 * 2 + 15 * 2 + 32,
                     width=130,
                     height=5,
                     min=1,
                     max=10,
                     step=1,
                     curved=False)
labelslidermasse = TextBox(
    displaysurf,
    posmain[0] + 100 + 140,  #width slider,
    posmain[1] + 23 + 18 * 2 + 15 * 2 + 32,
    0,
    0,
    fontSize=18,
    borderThickness=0)
labelslidermasse.disable()
labelmasse = TextBox(displaysurf,
                     posmain[0] + 30,
                     posmain[1] + 25 + 18 * 2 + 15 * 2 + 32,
                     0,
                     0,
                     fontSize=23,
                     borderThickness=0)
labelmasse.disable()
labelmasse.setText("Masse : ")

tempinput = TextBox(displaysurf,
                    posmain[0] + 140,
                    posmain[1] + 18 * 3 + 15 * 3 + 44,
                    90,
                    18,
                    fontSize=15,
                    borderThickness=1)
templabel = TextBox(displaysurf,
                    posmain[0] + 30,
                    posmain[1] + 25 + 18 * 3 + 15 * 3 + 44,
                    0,
                    0,
                    fontSize=23,
                    borderThickness=0)
templabel.disable()
templabel.setText("Température : ")

typelabel = TextBox(displaysurf,
                    posmain[0] + 30,
                    posmain[1] + 25 + 18 * 4 + 15 * 4 + 58,
                    0,
                    0,
                    fontSize=23,
                    borderThickness=0)
typelabel.disable()
typelabel.setText("Type : ")
typedropdown = Dropdown(displaysurf,
                        posmain[0] + 100,
                        posmain[1] + 18 * 4 + 15 * 4 + 58,
                        width=133,
                        height=18,
                        name="Quel type ?",
                        choices=["Gazeuse", "Tellurique"],
                        fontSize=23,
                        values=[0, 1],
                        textHalign='left',
                        pressedColour=(255, 255, 255),
                        inactiveColour=slidercolor,
                        textColour=bgcolor)  #séléction de type

slidernbplant = Slider(displaysurf,
                       posmain[0] + 38,
                       posmain[1] + 75 + 18 * 6 + 15 * 6,
                       height=5,
                       width=200,
                       min=1,
                       max=8,
                       step=1,
                       curved=False)
labelnbplant = TextBox(displaysurf,
                       posmain[0] + 38,
                       posmain[1] + 72 + 18 * 5 + 15 * 5,
                       width=200,
                       height=23,
                       fontSize=20,
                       borderThickness=1,
                       coulour=couleur_rect)
labelnbplant.disable()
labelnbplant.setText("       Nombre de planètes : ")
labelslidernb = TextBox(
    displaysurf,
    posmain[0] + 100 + 140,  #width slider,
    posmain[1] + 18 * 6 + 15 * 6 + 90,
    0,
    0,
    fontSize=18,
    borderThickness=0)
labelslidernb.disable()

aleatoire = TextBox(displaysurf,
                    posmain[0] + 28,
                    posmain[1] + 353,
                    0,
                    0,
                    fontSize=27,
                    borderThickness=0,
                    textColour=tcolor)
aleatoire.disable()
aleatoire.setText("Aléatoire")

cree = TextBox(displaysurf,
               posmain[0] + 65 + 100,
               posmain[1] + 353,
               0,
               0,
               fontSize=27,
               borderThickness=0,
               textColour=tcolor)
cree.disable()
cree.setText("Crée")

# fonction créer qui prend en entrée tous les états des paramètres visuels et crée une planète
def create():
  
  couleur = blue
  for i in range(slidernbplant.getValue()):
    distance=MAX/11 * (len(listeplan)+1)
    planet = animatedCircle(CENTRE, distance, displaysurf, couleur, 15)
    listeplan.append(planet)
  print(f"température : {tempinput.getText()}")
  print(f"taille : {slidertaille.getValue()}")
  print(f"nombre de planètes : {slidernbplant.getValue()}")
  print(f"masse : {slidermasse.getValue()}")
  print(f'type sélectionné {typedropdown.getSelected()}')

# génère une planète avec des paramètres aléatoires
def rdm():
    print(f"température : {random.randint(1,10)}")
    print(f"taille : {random.randint(1,10)}")
    print(f"nombre de planètes : {slidernbplant.getValue()}")
    print(f"masse : {random.randint(1,10)}")
    print(f'type sélectionné {random.randint(0,2)}')


# boucle principale
run = True
while run:
    events = pygame.event.get() # on récupère les évènement ayant lieu dans cette itération
    displaysurf.blit(starbackground, (0, 0)) # fond d'écran

    pygame.draw.rect(displaysurf, couleur_rect, grey,
                     border_radius=5)  # dessine le rectangle contenant les boutons
    pygame.draw.rect(displaysurf, [65, 63, 70], button_random,
                     border_radius=5)  # dessine bouton créer
    pygame.draw.rect(displaysurf, [65, 63, 70], button_cree,
                     border_radius=5)  # dessine bouton aléatoire

    #met à jour les étiquettes des sliders
    label_slider_taille.setText(slidertaille.getValue()) 
    labelslidermasse.setText(slidermasse.getValue())
    labelslidernb.setText(slidernbplant.getValue())

    for event in events:
        # vérifie si évènement de sortie du programme
        if event.type == pygame.QUIT:
            run = False
        # pause si la touche espace est appuyée
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
              animation = not animation
            if event.key ==pygame.K_k:
              listeplan=[]
            if event.key == pygame.K_p:
              listeplan.pop()

        # vérifier si boutons aléatoire et créer ont été appuyés
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # enregistre la position de la souris dans un tuple de coordonnées
            # vérifie si est superposé au bouton crée
            if button_cree.collidepoint(mouse_pos):
                create()
                print('CREATE was pressed at {0}'.format(mouse_pos))
              
            # ou superposé au bouton aléatoire
            if button_random.collidepoint(mouse_pos):
                rdm()
                print('RANDOM was pressed at {0}'.format(mouse_pos))

    if animation: # vérifie que l'animation ne soit pas en pause
        for i in range(len(listeplan)):
            listeplan[i].incremente_degree(0.1*(11-i)) # fait tourner chaque planète

    for i in listeplan:
        i.affiche()


    pygame_widgets.update(events)
    pygame.display.update()

pygame.quit()