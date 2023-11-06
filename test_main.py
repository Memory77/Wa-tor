import pygame
import random
import time

from classes import *


# Initialisation de Pygame
pygame.init()


# Creation de l'instance monde
monde = Monde(1000, 1000, 50)

# # recuperation des variables input
# nombre_poisson = int(input("Combien de poisson souhaitez-vous pour commencer ?"))
# nombre_requins = int(input("Combien de poisson souhaitez-vous pour commencer ?"))


# positions_deja_prises = []

# # fonction pour générer une position aléatoire non prise
# def generer_position_aleatoire():
#     while True:
#         x = random.randint(monde.case_size, monde.largeur - monde.case_size)  # Assurez-vous que cela correspond à votre taille de case
#         y = random.randint(monde.case_size, monde.hauteur - monde.case_size)
#         if (x, y) not in positions_deja_prises:
#             positions_deja_prises.append((x, y))
#             return x, y

# for _ in range(nombre_poisson):
#     x, y = generer_position_aleatoire()
#     monde.ajout_poisson(x, y)

# for _ in range(nombre_requins):
#     x, y = generer_position_aleatoire()
#     monde.ajout_requin(x, y)

# Ajout de poissons et requins dans le monde
monde.ajout_poisson(100, 900)
monde.ajout_poisson(300, 300)
monde.ajout_poisson(500, 400)
monde.ajout_poisson(800, 800)
monde.ajout_requin(100, 500)
monde.ajout_requin(800, 100)
monde.ajout_requin(200, 500)
monde.ajout_requin(500, 500)
monde.ajout_algue(500, 750)
monde.ajout_algue(200, 200)
monde.ajout_algue(800, 200)

# boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # gérer le cycle jour/nuit
    monde.chronon += 1
    if monde.chronon % monde.cycle_jour_nuit == 0:
        monde.est_jour = not monde.est_jour

    monde.afficher()
    monde.poissons_tab.update()
    monde.requins_tab.update()
    time.sleep(0.5)
    print(monde.chronon)

# Quitter Pygame
pygame.quit()
