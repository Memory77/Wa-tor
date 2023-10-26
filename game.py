import pygame
import sys
import numpy as np

# class Timer(Animaux):

#     def __init__(self, chronon, chronon_count, chronon_count_reproduction):
#         Animaux.init(self, chronon, chronon_count, chronon_count_reproduction)

#     def timer(self, chronon):

#         while self.chronon_count < 2:
#             for seconds in range(1, self.chronon+1):
#                 print(seconds)
#                 time.sleep(1)

#             self.chronon_count += 1
#             self.chronon_count_reproduction += 1
#             # self.energie -= 1 (pour les requins uniquement)
#             print(f"Un nouveau jour vient de passer, ({self.chronon_count} chronon(s))")
#             time.sleep(2) #temps d'attente entre chaque chronon/jour


# temps = Timer(5,0)
# temps.timer(5)

class Animaux(pygame.sprite.Sprite):

    def __init__(self, chronon, chronon_count, chronon_count_reproduction, x, y):
        super().__init__()
        self.chronon = chronon
        self.chronon_count = chronon_count
        self.chronon_count_reproduction = chronon_count_reproduction
        self.rect.x = x
        self.rect.y = y

    def reproduction(self, chronon_count_reproduction): #seuil de reproduction identiques pour poissons et requins
        if self.chronon_count_reproduction >= 3:
            self.old_poisson = pygame.Rect.copy(self.poisson.rect)
            self.old_requin = pygame.Rect.copy(self.requin.rect)
            self.chronon_count_reproduction = 0

    #def radar cases voisines

class Poissons(Animaux):
    pass

    def __init__(self, chronon, chronon_count, poisson):
        Animaux.init(self, chronon, chronon_count)
        self.poisson = poisson

    # def reproduction(self, chronon_count_reproduction):
    #     if self.chronon_count_reproduction >= 3:
    #         self.old_poisson = pygame.Rect.copy(self.poisson.rect)
    #         self.chronon_count_reproduction = 0


    def deplacements_poissons(self, poisson):
        #cases vides uniquement
        

class Poisson(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('img/poisson (1).png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# class Requin(Poisson):
#     def __init__(self, x, y):
#         super().__init__(x, y)  # Assurez-vous de passer x et y au constructeur de la classe mère
#         self.image = pygame.image.load('img/poisson.png')
#         self.rect = self.image.get_rect()

# Initialisation de Pygame
pygame.init()

# Taille de la fenêtre
largeur, hauteur = 1500, 1000
taille_case = largeur // 15

# Création de la fenêtre
fenetre = pygame.display.set_mode((largeur, hauteur))


grille_poissons = [[False] * (largeur // taille_case) for _ in range(hauteur // taille_case)]


# Couleurs
blanc = (255, 255, 255)
noir = (0, 0, 0)

# Groupes de sprite
tous_sprites = pygame.sprite.Group()


# Position de la case pour les poissons
positions_poissons = [(0, 1), (3, 5), (6, 8)]  # Exemple : positionnez 3 poissons à différentes positions
new_poisson = [(0, 1), (5, 5), (8, 8)]


for x_case, y_case in positions_poissons:
    if not grille_poissons[y_case][x_case]:
        grille_poissons[y_case][x_case] = True  # Marquez la case comme occupée par un poisson
        poisson = Poisson(x_case * taille_case, y_case * taille_case)
        tous_sprites.add(poisson)

for x_case, y_case in new_poisson:
    if not grille_poissons[y_case][x_case]:
        grille_poissons[y_case][x_case] = True  # Marquez la case comme occupée par un poisson
        poisson = Poisson(x_case * taille_case, y_case * taille_case)
        tous_sprites.add(poisson)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    fenetre.fill(blanc)

    for x in range(0, largeur, taille_case):
        pygame.draw.line(fenetre, noir, (x, 0), (x, hauteur))
    for y in range(0, hauteur, taille_case):
        pygame.draw.line(fenetre, noir, (0, y), (largeur, y))

    
    tous_sprites.update()
    tous_sprites.draw(fenetre)

    pygame.display.update()


# Quitter Pygame
pygame.quit()
sys.exit()

