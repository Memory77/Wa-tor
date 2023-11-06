import pygame
import random
import time
from Animaux import Requin
from Animaux import Poisson

# Classe pour le tableau de jeu
class Tableau:
    def __init__(self, largeur, hauteur, taille_case):
        self.largeur = largeur
        self.hauteur = hauteur
        self.taille_case = taille_case
        self.fenetre = pygame.display.set_mode((largeur, hauteur))
        pygame.display.set_caption("Wa-Tor")
        self.animaux = []  # Liste pour stocker tous les animaux
        self.deplacement = self.deplacement_aleatoire()  # Générateur pour les déplacements aléatoires
        self.delai = 800  # Délai entre les rafraîchissements de l'écran

        # Ajoutez des limites à la population maximale
        self.population_max_poissons = 200
        self.population_max_requins = 50


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
            if isinstance(animal, Poisson) and animal.age >= 5 and time.time() - animal.derniere_reproduction >= animal.delai_reproduction:
                x, y = animal.x, animal.y
                nouvel_animal = type(animal)(self, animal.image, x, y)  # Crée un nouvel animal du même type
                nouveaux_animaux.append(nouvel_animal)
                animal.derniere_reproduction = time.time()  # Met à jour le temps de la dernière reproduction
            elif isinstance(animal, Requin) and animal.age >= 5 and time.time() - animal.derniere_reproduction >= animal.delai_reproduction:
            # Fait de même pour les requins avec leur délai spécifique
                x, y = animal.x, animal.y
                nouvel_animal = type(animal)(self, animal.image, x, y)
                nouveaux_animaux.append(nouvel_animal)
                animal.derniere_reproduction = time.time()
        self.animaux.extend(nouveaux_animaux)  # Ajoute les nouveaux animaux à la liste d'animaux




        

    def manger_poisson(self, requin):
        poissons_a_manger = [poisson for poisson in self.animaux if isinstance(poisson, Poisson) and poisson.x == requin.x and poisson.y == requin.y]
        for poisson in poissons_a_manger:
            self.animaux.remove(poisson)
            requin.compteur_energie += 1  # Augmente le compteur d'énergie du requin
            print(poissons_a_manger)





         # Vérifie le temps écoulé depuis la dernière fois que le requin a mangé
        temps_actuel = time.time()
        temps_ecoule = temps_actuel - requin.derniere_mangee

        # Si plus d'une seconde s'est écoulée depuis la dernière fois que le requin a mangé, réduire le compteur d'énergie
        if temps_ecoule >= 5:
            requin.derniere_mangee = temps_actuel
            requin.compteur_energie -= 1    
           
        # blocage du compteur à 8
            if requin.compteur_energie > 8:
                requin.compteur_energie = 8
                


    def afficher(self):
        self.fenetre.fill((0, 0, 255))  # Remplit la fenêtre avec une couleur de fond (blanc)
        for i in range(0, self.largeur, self.taille_case):
            for j in range(0, self.hauteur, self.taille_case):
                pygame.draw.rect(self.fenetre, (0, 0, 255), (i, j, self.taille_case, self.taille_case), 1)
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