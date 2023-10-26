import pygame
import sys


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

# Couleurs
blanc = (255, 255, 255)
noir = (0, 0, 0)

# Groupes de sprite
tous_sprites = pygame.sprite.Group()


# Position de la case pour les poissons
positions_poissons = [(0, 1), (3, 5), (6, 8)]  # Exemple : positionnez 3 poissons à différentes positions

for x_case, y_case in positions_poissons:
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

