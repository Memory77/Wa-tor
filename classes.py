import pygame
import random
import time


class Monde:
    def __init__(self, largeur, hauteur, case_size):
        self.largeur = largeur
        self.hauteur = hauteur
        self.case_size = case_size
        self.fenetre = pygame.display.set_mode((self.largeur, self.hauteur))
        self.grille_poissons = [[False] * (largeur // case_size) for _ in range(hauteur // case_size)]
        self.poissons_tab = pygame.sprite.Group()
        self.requins_tab = pygame.sprite.Group()
        # attributs pour les bonus
        self.grille_algues = [[False] * (largeur // case_size) for _ in range(hauteur // case_size)]
        self.algues_tab = pygame.sprite.Group()
        self.chronon = 0  # compteur de chronon pour le monde
        self.cycle_jour_nuit = 5  #durée d'un jour ou d'une nuit en termes de chronons
        self.est_jour = True

    def ajout_algue(self, x, y):
        nouvelle_algue = Algue(x, y, self)
        self.algues_tab.add(nouvelle_algue)
        index_x = x // self.case_size
        index_y = y // self.case_size
        self.grille_algues[index_y][index_x] = True

    def ajout_poisson(self, x, y):
        nouveau_poisson = Poisson(x, y, self)
        self.poissons_tab.add(nouveau_poisson)

    def ajout_requin(self, x, y):
        nouveau_requin = Requin(x, y, self)
        self.requins_tab.add(nouveau_requin)

    def afficher(self):
        pygame.display.set_caption("Déplacement et reproduction d'animaux")

        image_jour = pygame.image.load('img/wator-background.png')
        image_nuit = pygame.image.load('img/wator-background-night.png')

        if self.est_jour:
            self.fenetre.blit(image_jour, (0, 0))
        else:
            self.fenetre.blit(image_nuit, (0, 0))

        self.algues_tab.draw(self.fenetre)
        self.poissons_tab.draw(self.fenetre)
        self.requins_tab.draw(self.fenetre)
        pygame.display.update()


class Algue(pygame.sprite.Sprite):
    def __init__(self, x, y, monde):
        super().__init__()
        self.image = pygame.image.load('img/algue (1).png')
        self.rect = self.image.get_rect(topleft=(x, y))
        self.monde = monde


class Poisson(pygame.sprite.Sprite):
    def __init__(self, x, y, monde):
        super().__init__()
        self.image = pygame.image.load('img/poisson5 (1).png')
        self.rect = self.image.get_rect(topleft=(x, y))
        self.chronon = 0
        self.temps_reproduction_poisson = 2
        self.monde = monde

    def deplacer(self):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                      (0, 1), (1, -1), (1, 0), (1, 1)]

        random.shuffle(directions)

        for dx, dy in directions:
            nouvelle_position_x = self.rect.x + (dx * self.monde.case_size)
            nouvelle_position_y = self.rect.y + (dy * self.monde.case_size)

            # gestion du tp
            if nouvelle_position_x < 0:
                nouvelle_position_x = self.monde.largeur - self.monde.case_size
            elif nouvelle_position_x >= self.monde.largeur:
                nouvelle_position_x = 0

            if nouvelle_position_y < 0:
                nouvelle_position_y = self.monde.hauteur - self.monde.case_size
            elif nouvelle_position_y >= self.monde.hauteur:
                nouvelle_position_y = 0

            # conversion des coordonnées pixels en indices de la grille
            index_x = nouvelle_position_x // self.monde.case_size
            index_y = nouvelle_position_y // self.monde.case_size

            # Vérifier si la nouvelle position est libre
            if not self.monde.grille_poissons[index_y][index_x] and not self.monde.grille_algues[index_y][index_x]:
                # Libération de l'ancienne case
                index_x_ancien = self.rect.x // self.monde.case_size
                index_y_ancien = self.rect.y // self.monde.case_size
                self.monde.grille_poissons[index_y_ancien][index_x_ancien] = False

                # Mise à jour de la grille pour la nouvelle position
                self.monde.grille_poissons[index_y][index_x] = True

                # Mise à jour de la position de l'objet
                self.rect.x = nouvelle_position_x
                self.rect.y = nouvelle_position_y
                break

    def update(self):
        # recuperation des anciennes positions avant de se déplacer
        ancienne_position_x = self.rect.x
        ancienne_position_y = self.rect.y

        self.deplacer()

        self.chronon += 1
        if self.chronon >= self.temps_reproduction_poisson:
            self.reproduire(ancienne_position_x, ancienne_position_y)

    def reproduire(self, ancienne_x, ancienne_y):
        index_x = ancienne_x // self.monde.case_size
        index_y = ancienne_y // self.monde.case_size

        # verification si l'ancienne position est libre
        if not self.monde.grille_poissons[index_y][index_x]:
            if self.__class__ == Poisson:
                self.monde.ajout_poisson(ancienne_x, ancienne_y)
            elif self.__class__ == Requin:
                self.monde.ajout_requin(ancienne_x, ancienne_y)
                # print('requin reproduit')
            # marquer la case comme occupée et réinitialiser le temps de reproduction
            self.monde.grille_poissons[index_y][index_x] = True
        self.chronon = 0


class Requin(Poisson):
    def __init__(self, x, y, monde):
        super().__init__(x, y, monde)
        self.image = pygame.image.load('img/req (2).png')
        self.rect = self.image.get_rect(topleft=(x, y))
        self.temps_survie_requin = 3
        self.temps_reproduction_requin = 6
        self.energie = 6
        self.cpt_sans_mange = 0

    def update(self):
        self.gestion_energie()
        # recuperation des anciennes positions avant de se déplacer
        ancienne_position_x = self.rect.x
        ancienne_position_y = self.rect.y
        self.deplacer()

        self.chronon += 1  # temps de reproduction en chronon voir time.sleep()
        if self.chronon >= self.temps_reproduction_requin:
            super().reproduire(ancienne_position_x, ancienne_position_y)

    def gestion_energie(self):
        if self.monde.est_jour == False:
            # print('les requins chassent')
            a_mange = False
            directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                          (0, 1), (1, -1), (1, 0), (1, 1)]

            for dx, dy in directions:
                nouvelle_position_x = self.rect.x + dx * self.monde.case_size
                nouvelle_position_y = self.rect.y + dy * self.monde.case_size

                if 0 <= nouvelle_position_x < self.monde.largeur and 0 <= nouvelle_position_y < self.monde.hauteur:
                    for fish in self.monde.poissons_tab:
                        if isinstance(fish, Poisson) and not isinstance(fish, Requin):
                            if fish.rect.x == nouvelle_position_x and fish.rect.y == nouvelle_position_y:
                                fish.kill()  # enlève le poisson du groupe de sprites
                                # print("poisson mangé")
                                index_x = nouvelle_position_x // self.monde.case_size
                                index_y = nouvelle_position_y // self.monde.case_size
                                # libère la grille
                                self.monde.grille_poissons[index_y][index_x] = False
                                self.energie += 1
                                a_mange = True
                                break

            if not a_mange:
                self.energie -= 1
                self.cpt_sans_mange += 1
            else:
                self.cpt_sans_mange = 0

            if self.energie <= 0 or self.cpt_sans_mange >= self.temps_survie_requin:
                self.kill()
                # print(self.energie)
                # print(self.cpt_sans_mange)
                # print('requin mort')
