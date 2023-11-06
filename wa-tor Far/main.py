import pygame
import sys
import time
from tableau import Tableau
from Animaux import Requin
from Animaux import Poisson

def main():
    pygame.init()  # Initialise Pygame

    largeur, hauteur, taille_case = 700,700, 50  # Dimensions du tableau et taille des cases

    tableau = Tableau(largeur, hauteur, taille_case)  # Crée le tableau du jeu
    image_poisson = pygame.image.load("wa-tor /poisson2_far.gif")  # Charge l'image du poisson
    image_requin = pygame.image.load("wa-tor /requin_far.jpeg")  # Charge l'image du requin


    x_poisson, y_poisson = 200, 100  # Position initiale du poisson
    poisson = Poisson(tableau, image_poisson, x_poisson, y_poisson)  # Crée un nouveau poisson
    tableau.animaux.append(poisson)  # Ajoute le poisson à la liste d'animaux

    x_poisson, y_poisson = 100, 200  # Position initiale du poisson
    poisson2 = Poisson(tableau, image_poisson, x_poisson, y_poisson)  # Crée un nouveau poisson
    tableau.animaux.append(poisson2)  # Ajoute le poisson à la liste d'animaux

    x_requin, y_requin = 50, 50  # Position initiale du requin
    requin = Requin(tableau, image_requin, x_requin, y_requin)  # Crée un nouveau requin
    tableau.animaux.append(requin)  # Ajoute le requin à la liste d'animaux


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        tableau.afficher()  # Affiche le tableau

        # Crée un poisson et un requin toutes milli-secondes
        if time.time() - tableau.animaux[-1].derniere_reproduction >= 20000:

            x, y = 50, 50  # Position initiale du poisson
            poisson = Poisson(tableau, image_poisson, x, y)  # Crée un nouveau poisson
            tableau.animaux.append(poisson)  # Ajoute le poisson à la liste d'animaux

            x, y = 50, 50  # Position initiale du requin
            requin = Requin(tableau, image_requin, x, y)  # Crée un nouveau requin
            tableau.animaux.append(requin)  # Ajoute le requin à la liste d'animaux





if __name__ == "__main__":
    main()