import pygame
import sys
import random


chronon = 0

#definition de la classe poisson
class Poisson(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('img/poisson-rouge.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.temps_reproduction_poisson = 0  # age du poisson en chronons

    def update(self):
        self.temps_reproduction_poisson += 1
        if self.temps_reproduction_poisson >= 30:
            self.reproduire()
            temps_temps_reproduction_poisson = 0

    def reproduire(self):
        # directions possibles pour la reproduction, ce sera jamais 0 0 car c'est le parent
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        random.shuffle(directions)  # Mélanger les directions pour choisir au hasard

        for dx, dy in directions:
            nouvelle_position_x = self.rect.x + dx * taille_case
            nouvelle_position_y = self.rect.y + dy * taille_case

            
            #on va verifier si :la nouvelle position x et y est entre 0 et la largeur, et que la case est libre grace au booleen
            #il faudra changer par la suite faire en sorte que ça se delimite 
            if (0 <= nouvelle_position_x < largeur and 0 <= nouvelle_position_y < hauteur and 
                not grille_poissons[nouvelle_position_y // taille_case][nouvelle_position_x // taille_case]):
                grille_poissons[nouvelle_position_y // taille_case][nouvelle_position_x // taille_case] = True
                nouveau_poisson = Poisson(nouvelle_position_x, nouvelle_position_y)
                tous_sprites.add(nouveau_poisson)
                break  # Arrêter après avoir trouvé une position libre

        self.temps_reproduction_poisson = 0  # Réinitialiser l'âge de reproduction

# Initialisation de Pygame
pygame.init()

# taille fenêtre
largeur, hauteur = 1500, 1000
taille_case = largeur // 50

# creation fenetre
fenetre = pygame.display.set_mode((largeur, hauteur))

#definition de la grille
#liste comprehension qui créé une grille 2d donc une liste de liste
#largeur//taille_case calcule le nb de cases horizontales dans la grille et item hauteur
grille_poissons = [[False] * (largeur // taille_case) for _ in range(hauteur // taille_case)]


# couleur du background
ocean = (50, 50, 255)

#definition du background
fenetre.fill(ocean)


# Groupes de sprite
tous_sprites = pygame.sprite.Group()

positions_poissons = []

#nombre initial de poissons
nombre_poissons = 5

# Générez aléatoirement les positions de départ pour les poissons
for _ in range(nombre_poissons):
    x_case, y_case = random.randint(0, (largeur // taille_case) - 1), random.randint(0, (hauteur // taille_case) - 1)
    while grille_poissons[y_case][x_case]:
        x_case, y_case = random.randint(0, (largeur // taille_case) - 1), random.randint(0, (hauteur // taille_case) - 1)
    positions_poissons.append((x_case, y_case))

# Créez les poissons à ces positions
for x_case, y_case in positions_poissons:
    grille_poissons[y_case][x_case] = True
    poisson = Poisson(x_case * taille_case, y_case * taille_case)
    tous_sprites.add(poisson)
    
    
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    chronon += 1  # Incrémente le chronon à chaque itération de la boucle

    #code juste pour voir les lignes de la grille definie plus haut
    #for x in range(0, largeur, taille_case):
    #    pygame.draw.line(fenetre, noir, (x, 0), (x, hauteur))
    #for y in range(0, hauteur, taille_case):
    #    pygame.draw.line(fenetre, noir, (0, y), (largeur, y))

    tous_sprites.update()
    tous_sprites.draw(fenetre)

    pygame.display.update()

# Quitter Pygame
pygame.quit()
sys.exit()