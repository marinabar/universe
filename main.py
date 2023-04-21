# on importe les bibliothèques nécessaires

from cgitb import text
import pygame, random, math
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.dropdown import Dropdown, DropdownChoice
import pygame.freetype

#taille de la fenêtre
LARGEUR_ECRAN = 1080
HAUTEUR_ECRAN = 720

#fonction permettant de créer un dégradé de couleur entre start et end avec n couleurs intermédiaires
def generate_gradient(start_color, end_color, n):
    r1, g1, b1 = start_color
    r2, g2, b2 = end_color
    delta_r = (r2 - r1) / (n - 1)
    delta_g = (g2 - g1) / (n - 1)
    delta_b = (b2 - b1) / (n - 1)
    gradient = [start_color]
    for i in range(n):
        r = int(r1 + i * delta_r)
        g = int(g1 + i * delta_g)
        b = int(b1 + i * delta_b)
        gradient.append((r, g, b))
    return gradient+[end_color]

color_list1 = generate_gradient((255,0,0),(255,255,102),18)
color_list2 = generate_gradient((255,255,102),(61,118,224),18)
color_list = color_list1+color_list2[1:-1]

# classe pour créer la planète animée
class animatedCircle:
    def __init__(self,
                 center: tuple,
                 distanceTo0,
                 display,
                 size=2,
                 masse=1,
                 type=1,
                 temp=60,
                 width=0,
                 animationDegree=0,
                 color=(255, 255, 255)):
        self.center = center  # centre de rotation de la sphère, centre de l'orbite
        self.distanceTo0 = distanceTo0  # rayon du cercle correspondant à l'orbite de la sphère
        self.display = display  # surface sur laquelle afficher la sphère
        self.color = color  # couleur de la sphère
        self.size = int(size) # rayon de la sphère
        self.masse = int(masse)
        # si température spécifiée
        if temp:
            self.temp=int(temp)
        else:
            self.temp=60
        #si type spécifié
        if type:
            self.type=int(type)
        else:
            self.type=1
        self.width = int(width)  # épaisseur de la sphère, si =0 sphère pleine
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
                            self.animationDegree), float(self.size), self.width)
    
    def setcouleur(self):
        i = int((self.temp+100)*38/200)
        print(i)
        print(self.temp)
        self.color = color_list[i]

# création d'un fond d'écran avec une image
starbackground = pygame.image.load("night.jpg")
starbackground = pygame.transform.scale(starbackground,
                                        (LARGEUR_ECRAN, HAUTEUR_ECRAN))

# initialisation de pygame
pygame.init()
pygame.display.set_caption('Universe') # nom de la fenêtre
displaysurf = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
font = pygame.font.Font(None, 13)


# paramètres de planètes
MAX = 320 # distance maximale entre le centre du système solaire et la planète
CENTRE=((LARGEUR_ECRAN *3/4)/2-25, 360)
NBPLANMAX=11

# flag mouvement des planètes ou pas
animation = True

# liste des planètes
listeplan=[]

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
cadreinfo=pygame.Rect(posmain[0]+20, posmain[1] + 420, posmain[2]-40, 20)

#palette de couleurs
bgcolor = (65, 63, 70) #couleur foncée
tcolor = couleur_rect #couleur du text
slidercolor = (200, 200, 200) # couleur des sliders
darkgrey=(104,104,104)

# définition de tous les éléments texte + sliders en utilisant la bibliothèque pygame-widgets
slidertaille = Slider(displaysurf,
                      posmain[0] + 100,
                      posmain[1] + 9 + 18 * 1 + 15 * 1 + 20,
                      width=130,
                      height=5,
                      min=1,
                      max=10,
                      step=1,
                      initial=2,
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
                    borderThickness=1, placeholderText='nombre')

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
                       curved=False, initial=1)
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
    posmain[0] + 100 + 140, 
    posmain[1] + 18 * 6 + 15 * 6 + 90,
    0,
    0,
    fontSize=18,
    borderThickness=0)
labelslidernb.disable()

#texte "aléatoire"
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

#texte "créer"
cree = TextBox(displaysurf,
               posmain[0] + 65 + 97,
               posmain[1] + 353,
               0,
               0,
               fontSize=27,
               borderThickness=0,
               textColour=tcolor)
cree.disable()
cree.setText("Créer")



# fonction créer qui prend en entrée tous les états des paramètres visuels et crée une planète
def create():
  print(f"température : {tempinput.getText()}")
  print(f"taille : {slidertaille.getValue()}")
  print(f"nombre de planètes : {slidernbplant.getValue()}")
  print(f"masse : {slidermasse.getValue()}")
  print(f'type sélectionné {typedropdown.getSelected()}')
  for i in range(slidernbplant.getValue()):
    distance=MAX/11 * (len(listeplan)+1)
    planet = animatedCircle(CENTRE, distance, displaysurf, slidertaille.getValue()+5, slidermasse.getValue(),
                            tempinput.getText(), typedropdown.getSelected())
    planet.setcouleur()
    if len(listeplan)<NBPLANMAX:
        listeplan.append(planet)

# génère une planète avec des paramètres aléatoires
def rdm():
    print(f"température : {random.randint(-130,130)}")
    print(f"taille : {random.randint(1,10)}")
    print(f"nombre de planètes : {slidernbplant.getValue()}")
    print(f"masse : {random.randint(1,10)}")
    print(f'type sélectionné {random.randint(0,1)}')
    distance=MAX/11 * (len(listeplan)+1)
    planet = animatedCircle(CENTRE, distance, displaysurf, random.randint(1,15), random.randint(1,10),
                            random.randint(0,1), random.randint(-100,100))
    planet.setcouleur()
    if len(listeplan)<11:
        listeplan.append(planet)

#compteur
i=0
transparence=255

#texte d'information
notice = "Faire K pour détruire l'univers et P pour annihiler une planète"

# boucle principale
run = True
while run:
    events = pygame.event.get() # on récupère les évènement ayant lieu dans cette itération
    displaysurf.blit(starbackground, (0, 0)) # fond d'écran
    

    pygame.draw.rect(displaysurf, couleur_rect, grey,
                     border_radius=5)  # dessine le rectangle contenant les boutons

    # vérifie si le nombre de planètes max n'est pas atteint
    if len(listeplan)==NBPLANMAX:
        couleur_bouton=(120,120,120)
    else:
        couleur_bouton=[65, 63, 70]
    
    pygame.draw.rect(displaysurf, couleur_bouton, button_cree,
                     border_radius=5)  # dessine bouton aléatoire
    
    pygame.draw.rect(displaysurf, couleur_bouton, button_random,
                     border_radius=5)  # dessine bouton random

    #texte du cadre avec les info
    transparence-=0.25
    if transparence>=0:
        pygame.draw.rect(displaysurf, (104,104,104, transparence), cadreinfo, border_radius=0)  # dessine cadre avec informations
        text_surf = font.render(notice, True, (200,200,200))
        text_surf.set_alpha(transparence)
        displaysurf.blit(text_surf, (posmain[0] + 22 , posmain[1] + 425))

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
            if event.key == pygame.K_p and len(listeplan)!=0:
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
            listeplan[i].incremente_degree(listeplan[i].masse*0.02*(11-i)) # fait tourner chaque planète

    #on affiche chaque planète
    for i in listeplan:
        i.affiche()


    pygame_widgets.update(events)
    pygame.display.update()

pygame.quit()
