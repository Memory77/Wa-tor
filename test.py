import pygame
import sys
import random
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

# Classe pour les poissons
class Poisson(Animal):
    pass

# Classe pour les requins
class Requin(Animal):
    def __init__(self, tableau, image, x, y):
        super().__init__(tableau, image, x, y)
        self.compteur_energie = 100  # Compteur d'énergie du requin

# Classe pour le tableau de jeu
class Tableau:
    def __init__(self, largeur, hauteur, taille_case):
        self.largeur = largeur
        self.hauteur = hauteur
        self.taille_case = taille_case
        self.fenetre = pygame.display.set_mode((largeur, hauteur))
        pygame.display.set_caption("Déplacement et reproduction d'animaux")
        self.animaux = []  # Liste pour stocker tous les animaux
        self.deplacement = self.deplacement_aleatoire()  # Générateur pour les déplacements aléatoires
        self.delai = 500  # Délai entre les rafraîchissements de l'écran

    def deplacement_aleatoire(self):
        while True:
            # Quatre directions possibles pour les déplacements
            directions = [(self.taille_case, 0), (-self.taille_case, 0), (0, self.taille_case), (0, -self.taille_case)]
            dx, dy = random.choice(directions)
            yield dx, dy

    def case_est_vide(self, x, y):
        # Vérifie si une case est vide (pas d'autre animal à cette position)
        return all(animal.x != x or animal.y != y for animal in self.animaux)

    def reproduction(self):
        nouveaux_animaux = []  # Liste pour stocker les nouveaux animaux créés
        for animal in self.animaux:
            if isinstance(animal, (Poisson, Requin)):
                # Vérifie si l'animal a un âge suffisant et s'il s'est écoulé suffisamment de temps depuis la dernière reproduction
                if animal.age >= 3 and time.time() - animal.derniere_reproduction >= 3:
                    x, y = animal.x, animal.y
                    nouvel_animal = type(animal)(self, animal.image, x, y)  # Crée un nouvel animal du même type
                    nouveaux_animaux.append(nouvel_animal)
                    animal.derniere_reproduction = time.time()  # Met à jour le temps de la dernière reproduction
        self.animaux.extend(nouveaux_animaux)  # Ajoute les nouveaux animaux à la liste d'animaux

    def manger_poisson(self, requin):
        poissons_a_manger = [poisson for poisson in self.animaux if isinstance(poisson, Poisson) and poisson.x == requin.x and poisson.y == requin.y]
        for poisson in poissons_a_manger:
            self.animaux.remove(poisson)
            requin.compteur_energie += 10  # Augmente le compteur d'énergie du requin

    def afficher(self):
        self.fenetre.fill((255, 255, 255))  # Remplit la fenêtre avec une couleur de fond (blanc)
        for i in range(0, self.largeur, self.taille_case):
            for j in range(0, self.hauteur, self.taille_case):
                pygame.draw.rect(self.fenetre, (0, 0, 0), (i, j, self.taille_case, self.taille_case), 1)
                # Dessine un rectangle (case) avec des contours noirs

        self.reproduction()  # Appelle la méthode de reproduction
        for animal in self.animaux:
            animal.deplacer()  # Appelle la méthode deplacer() de chaque animal pour les déplacer
            if isinstance(animal, Requin):
                self.manger_poisson(animal)  # Vérifie s'il y a des poissons à manger
                if animal.compteur_energie <= 0:
                    self.animaux.remove(animal)  # Le requin disparaît s'il n'a plus d'énergie
            self.fenetre.blit(animal.image, (animal.x, animal.y))  # Affiche l'image de chaque animal à sa position actuelle

        pygame.display.flip()  # Actualise l'affichage
        pygame.time.delay(self.delai)  # Délai entre les rafraîchissements de l'écran

def main():
    pygame.init()  # Initialise Pygame

    largeur, hauteur, taille_case = 400, 400, 50  # Dimensions du tableau et taille des cases
    tableau = Tableau(largeur, hauteur, taille_case)  # Crée le tableau du jeu
    image_poisson = pygame.image.load("img/poisson (1).png")  # Charge l'image du poisson
    image_requin = pygame.image.load("img/12624.png")  # Charge l'image du requin

    x_poisson, y_poisson = 50, 50  # Position initiale du poisson
    poisson = Poisson(tableau, image_poisson, x_poisson, y_poisson)  # Crée un nouveau poisson
    tableau.animaux.append(poisson)  # Ajoute le poisson à la liste d'animaux

    x_requin, y_requin = 50, 50  # Position initiale du requin
    requin = Requin(tableau, image_requin, x_requin, y_requin)  # Crée un nouveau requin
    tableau.animaux.append(requin)  # Ajoute le requin à la liste d'animaux

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        tableau.afficher()  # Affiche le tableau

        # Crée un poisson et un requin toutes les 5 secondes
        if time.time() - tableau.animaux[-1].derniere_reproduction >= 5:

            x, y = 50, 50  # Position initiale du poisson
            poisson = Poisson(tableau, image_poisson, x, y)  # Crée un nouveau poisson
            tableau.animaux.append(poisson)  # Ajoute le poisson à la liste d'animaux

            x, y = 50, 50  # Position initiale du requin
            requin = Requin(tableau, image_requin, x, y)  # Crée un nouveau requin
            tableau.animaux.append(requin)  # Ajoute le requin à la liste d'animaux

if __name__ == "__main__":
    main()
