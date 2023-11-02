import pygame
import random
import time

class Poisson(pygame.sprite.Sprite):
    def __init__(self, x, y, monde):
        super().__init__()
        self.image = pygame.image.load('img/poisson-clown.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.chronon = 0
        self.temps_reproduction_poisson = 5
        self.monde = monde

    def deplacer(self):
        directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nouvelle_position_x = self.rect.x + (dx * self.monde.taille_case)
            nouvelle_position_y = self.rect.y + (dy * self.monde.taille_case)
            
            # Gestion du TP
            if nouvelle_position_x < 0:
                nouvelle_position_x = self.monde.largeur - self.monde.taille_case
            elif nouvelle_position_x >= self.monde.largeur:
                nouvelle_position_x = 0

            if nouvelle_position_y < 0:
                nouvelle_position_y = self.monde.hauteur - self.monde.taille_case
            elif nouvelle_position_y >= self.monde.hauteur:
                nouvelle_position_y = 0

            if 0 <= nouvelle_position_x < self.monde.largeur and 0 <= nouvelle_position_y < self.monde.hauteur:
                index_x = nouvelle_position_x // self.monde.taille_case
                index_y = nouvelle_position_y // self.monde.taille_case
                
                if not self.monde.grille_poissons[index_y][index_x]:
                    # Libération de l'ancienne case
                    ancienne_index_x = self.rect.x // self.monde.taille_case
                    ancienne_index_y = self.rect.y // self.monde.taille_case
                    self.monde.grille_poissons[ancienne_index_y][ancienne_index_x] = False
                    
                    # L'objet est dans sa nouvelle position
                    self.monde.grille_poissons[index_y][index_x] = True
                    self.rect.x = nouvelle_position_x
                    self.rect.y = nouvelle_position_y
                    break

    def update(self):
        ancienne_position_x = self.rect.x
        ancienne_position_y = self.rect.y

        self.deplacer()

        self.chronon += 1
        if self.chronon >= self.temps_reproduction_poisson:
            self.reproduire(ancienne_position_x, ancienne_position_y)

    def reproduire(self, ancienne_x, ancienne_y):
        index_x = ancienne_x // self.monde.taille_case
        index_y = ancienne_y // self.monde.taille_case

        if not self.monde.grille_poissons[index_y][index_x]:
            if self.__class__ == Requin:
                print('requin reproduit')
                self.monde.ajout_requin(ancienne_x, ancienne_y)
            elif self.__class__ == Poisson:
                self.monde.ajout_poisson(ancienne_x, ancienne_y)
            self.monde.grille_poissons[index_y][index_x] = True
            self.chronon = 0

class Requin(Poisson):
    def __init__(self, x, y, monde):
        super().__init__(x, y, monde)
        self.image = pygame.image.load('img/requin.png')
        self.rect = self.image.get_rect()
        self.temps_starvation_requin = 30
        self.temps_reproduction_requin = 2
        self.energie = 10
        self.cpt_sans_mange = 0

    def update(self):
        self.gestion_energie()
        ancienne_position_x = self.rect.x
        ancienne_position_y = self.rect.y
        super().deplacer()

        self.chronon += 1
        if self.chronon >= self.temps_reproduction_requin:
            self.reproduire(ancienne_position_x, ancienne_position_y)
            self.chronon = 0

    def gestion_energie(self):
        a_mange = False
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for dx, dy in directions:
            nouvelle_position_x = self.rect.x + dx * self.monde.taille_case
            nouvelle_position_y = self.rect.y + dy * self.monde.taille_case

            if 0 <= nouvelle_position_x < self.monde.largeur and 0 <= nouvelle_position_y < self.monde.hauteur:
                for fish in self.monde.poissons_tab:
                    if isinstance(fish, Poisson) and not isinstance(fish, Requin):
                        if fish.rect.x == nouvelle_position_x and fish.rect.y == nouvelle_position_y:
                            fish.kill()
                            print("poisson mangé")
                            index_x = nouvelle_position_x // self.monde.taille_case
                            index_y = nouvelle_position_y // self.monde.taille_case
                            self.monde.grille_poissons[index_y][index_x] = False
                            self.energie += 2
                            print(self.energie)
                            a_mange = True
                            self.cpt_sans_mange = 0
                            break

        if not a_mange:
            self.energie -= 1
            self.cpt_sans_mange += 1

        if self.energie <= 0 or self.cpt_sans_mange == self.temps_starvation_requin:
            self.kill()
            print("je suis mort")

    def reproduire(self, ancienne_x, ancienne_y):
        if self.energie > 5:  # condition d'énergie pour la reproduction
            positions_voisines = [(ancienne_x + dx, ancienne_y + dy) for dx in range(-1, 2) for dy in range(-1, 2)]
            positions_voisines.remove((ancienne_x, ancienne_y))

            for pos in positions_voisines:
                if self.monde.est_dans_grille(*pos) and self.monde.est_vide(*pos):
                    # Création du nouveau requin
                    nouveau_requin = Requin(*pos, self.monde)
                    self.monde.ajouter_entite(nouveau_requin)
                    print("Nouveau requin né en position", pos)
                    break

class Monde:
    def __init__(self, largeur, hauteur, taille_case):
        self.largeur = largeur  # Ajouté ici
        self.hauteur = hauteur  # Ajouté ici
        self.taille_case = taille_case
        self.grille_poissons = [[False for _ in range(largeur // taille_case)] for _ in range(hauteur // taille_case)]
        self.poissons_tab = pygame.sprite.Group()

    def ajout_poisson(self, x, y):
        poisson = Poisson(x, y, self)
        self.poissons_tab.add(poisson)
        index_x = x // self.taille_case
        index_y = y // self.taille_case
        self.grille_poissons[index_y][index_x] = True

    def ajout_requin(self, x, y):
        requin = Requin(x, y, self)
        self.poissons_tab.add(requin)
        index_x = x // self.taille_case
        index_y = y // self.taille_case
        self.grille_poissons[index_y][index_x] = True

def main():
    pygame.init()
    largeur_ecran = 1000
    hauteur_ecran = 1000
    taille_case = 50
    ecran = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
    pygame.display.set_caption("Simulation Poisson")

    monde = Monde(largeur_ecran, hauteur_ecran, taille_case)

    for _ in range(50):
        x = random.randint(0, (largeur_ecran // taille_case) - 1) * taille_case
        y = random.randint(0, (hauteur_ecran // taille_case) - 1) * taille_case
        monde.ajout_poisson(x, y)

    for _ in range(5):
        x = random.randint(0, (largeur_ecran // taille_case) - 1) * taille_case
        y = random.randint(0, (hauteur_ecran // taille_case) - 1) * taille_case
        monde.ajout_requin(x, y)

    clock = pygame.time.Clock()
    continuer = True

    while continuer:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False

        ecran.fill((255, 255, 255))
        monde.poissons_tab.update()
        monde.poissons_tab.draw(ecran)
        pygame.display.flip()
        clock.tick(1)

    pygame.quit()

if __name__ == "__main__":
    main()
