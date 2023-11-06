import pygame
import time



# Classe de base pour tous les animaux
class Animal:
    def __init__(self, tableau, image, x, y):
        self.tableau = tableau
        self.image = pygame.transform.scale(image, (40, 40))
        self.x = x
        self.y = y
        self.age = 0
        self.derniere_reproduction = time.time()
    


    def deplacer(self):
        # Méthode pour déplacer un animal dans une direction aléatoire
        dx, dy = next(self.tableau.deplacement)
        # Gestion du rebouclage lorsque l'animal atteint les bords
        self.x = (self.x + dx) % self.tableau.largeur
        self.y = (self.y + dy) % self.tableau.hauteur
        self.age += 1



class Poisson(Animal):
    def __init__(self, tableau, image, x, y):
        super().__init__(tableau, image, x, y)
        self.delai_reproduction = 15  # Délai de reproduction spécifique aux poissons


class Requin(Animal):
    def __init__(self, tableau, image, x, y):
        super().__init__(tableau, image, x, y)
        self.compteur_energie = 10  # Compteur d'énergie du requin
        self.derniere_mangee = time.time()  # Initialise le temps de la dernière fois qu'il a mangé
        self.delai_reproduction = 10  # Délai de reproduction spécifique aux requins
