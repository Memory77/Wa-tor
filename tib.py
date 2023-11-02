import random
import time
import pygame


class Monde:
    def __init__(self, largeur, hauteur):
        self.largeur = largeur
        self.hauteur = hauteur


class Poisson(Monde):
    def __init__(self, monde, fish="🐠"):
        self.monde = monde
        self.x = random.randint(0, monde.largeur - 1) % monde.largeur
        self.y = random.randint(0, monde.hauteur - 1) % monde.hauteur
        self.fish = fish

    def deplacements_poissons(self, grille):
        indices_adjacents = []
        haut = (self.y - 1) % self.monde.hauteur
        bas = (self.y + 1) % self.monde.hauteur
        gauche = (self.x - 1) % self.monde.largeur
        droite = (self.x + 1) % self.monde.largeur
        directions = [(self.x, haut), (self.x, bas), (gauche, self.y), (droite, self.y)]
        indices_adjacents = []

        for x, y in directions:
            nouvel_x = x % self.monde.largeur
            nouvel_y = y % self.monde.hauteur
            if grille[nouvel_y][nouvel_x] == "💧":
                indices_adjacents.append((nouvel_x, nouvel_y))

        if indices_adjacents:
            nouvel_x, nouvel_y = random.choice(indices_adjacents)
            grille[self.y][self.x] = "💧"
            self.x, self.y = nouvel_x, nouvel_y
            grille[self.y][self.x] = self.fish

        return grille


class Requin(Poisson):
    def __init__(self, monde, shark="🦈"):
        super().__init__(monde, shark)
        self.shark = shark
        self.energie = 5

    def energie_vitale(self, grille, liste_de_requins):
        if self.energie == 0:
            grille[self.y][self.x] = "💧"
            liste_de_requins.remove(self)

    def deplacements_requins(self, grille, poissons):
        poissons_adjacents = []

        for poisson in poissons:
            if abs(self.x - poisson.x) <= 1 and abs(self.y - poisson.y) <= 1:
                poissons_adjacents.append(poisson)

        if poissons_adjacents:
            poisson_adjacent = random.choice(poissons_adjacents)
            grille[self.y][self.x] = "💧"
            self.x, self.y = poisson_adjacent.x, poisson_adjacent.y
            grille[self.y][self.x] = self.shark
            poissons.remove(poisson_adjacent)
            self.energie += 1
        else:
            haut = (self.y - 1) % self.monde.hauteur
            bas = (self.y + 1) % self.monde.hauteur
            gauche = (self.x - 1) % self.monde.largeur
            droite = (self.x + 1) % self.monde.largeur
            directions = [(self.x, haut), (self.x, bas), (gauche, self.y), (droite, self.y)]

            indices_adjacents = []
            for x, y in directions:
                nouvel_x = x % self.monde.largeur
                nouvel_y = y % self.monde.hauteur
                if grille[nouvel_y][nouvel_x] == "💧":
                    indices_adjacents.append((nouvel_x, nouvel_y))

            if indices_adjacents:
                nouvel_x, nouvel_y = random.choice(indices_adjacents)
                grille[self.y][self.x] = "💧"
                self.x, self.y = nouvel_x, nouvel_y
                grille[self.y][self.x] = self.shark

        return grille


# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
largeur_fenetre = 800
hauteur_fenetre = 400
taille_case = 40  # Taille d'une case en pixels

fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Monde sous-marin")

# Couleurs
COULEUR_EAU = (0, 105, 148)
COULEUR_POISSON = (255, 255, 0)
COULEUR_REQUIN = (255, 0, 0)


def dessiner_grille():
    for y in range(monde.hauteur):
        for x in range(monde.largeur):
            rect = pygame.Rect(x * taille_case, y * taille_case, taille_case, taille_case)
            if grille[y][x] == "💧":
                pygame.draw.rect(fenetre, COULEUR_EAU, rect)
            elif grille[y][x] == "🐠":
                pygame.draw.rect(fenetre, COULEUR_POISSON, rect)
            elif grille[y][x] == "🦈":
                pygame.draw.rect(fenetre, COULEUR_REQUIN, rect)


# Création d'une instance de Monde
monde = Monde(20, 10)  # Largeur et hauteur du monde

# Initialisation de la grille
grille = [["💧" for _ in range(monde.largeur)] for _ in range(monde.hauteur)]

# Demande à l'utilisateur combien de poissons et de requins il souhaite
nombre_de_poissons = int(input("Combien de poissons voulez-vous créer ? "))
nombre_de_requins = int(input("Combien de requins voulez-vous créer ? "))

# Création des poissons et des requins
liste_de_poissons = [Poisson(monde) for _ in range(nombre_de_poissons)]
liste_de_requins = [Requin(monde) for _ in range(nombre_de_requins)]

chronon = 0
chronon_reproduction_poisson = 0
chronon_reproduction_requin = 0

# Boucle principale de Pygame
en_cours = True
while en_cours:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False

    # Logique de jeu
    for poisson in liste_de_poissons:
        poisson.deplacements_poissons(grille)
    for requin in liste_de_requins:
        requin.energie -= 1
        requin.deplacements_requins(grille, liste_de_poissons)
        requin.energie_vitale(grille, liste_de_requins)

    if chronon % 50 == 0:
        for poisson in liste_de_poissons:
            liste_de_poissons.append(Poisson(monde))
            poisson.deplacements_poissons(grille)
        for requin in liste_de_requins:
            liste_de_requins.append(Requin(monde))
            requin.deplacements_requins(grille, liste_de_poissons)

    # Mise à jour de l'affichage
    dessiner_grille()
    pygame.display.flip()
    time.sleep(1)

    chronon += 1

pygame.quit()
