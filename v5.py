import pygame
import random
import time

class Poisson(pygame.sprite.Sprite):
    def __init__(self, x, y, grille_poisson, case_size):
        super().__init__()
        self.image = pygame.image.load('img/poisson5.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.temps_reproduction_poisson = 0  # age du poisson en chronons
        self.grille_poisson = grille_poisson
        self.case_size = case_size

    def deplacer(self):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        random.shuffle(directions)

        for dx, dy in directions:
            nouvelle_position_x = self.rect.x + dx * self.case_size
            nouvelle_position_y = self.rect.y + dy * self.case_size

            # gestion du tp
            if nouvelle_position_x < 0:
                nouvelle_position_x = WIDTH - self.case_size
            elif nouvelle_position_x >= WIDTH:
                nouvelle_position_x = 0

            if nouvelle_position_y < 0:
                nouvelle_position_y = HEIGHT - self.case_size
            elif nouvelle_position_y >= HEIGHT:
                nouvelle_position_y = 0

            index_x = nouvelle_position_x // self.case_size
            index_y = nouvelle_position_y // self.case_size

            # verification si le point x et y remplissent les conditions pour le deplacement
            if 0 <= index_x < WIDTH // self.case_size and 0 <= index_y < HEIGHT // self.case_size:
                if not self.grille_poisson[index_y][index_x]:
                    self.grille_poisson[self.rect.y // self.case_size][self.rect.x // self.case_size] = False
                    self.grille_poisson[index_y][index_x] = True
                    self.rect.x = nouvelle_position_x
                    self.rect.y = nouvelle_position_y
                    break

    def update(self):
        self.deplacer()
        #stockage de la position pour faire des bébés
        ancienne_position_x = self.rect.x  
        ancienne_position_y = self.rect.y  
        self.temps_reproduction_poisson += 1 #temps de reproduction en chronon (1 chronon = 0.5s voir la boucle de jeu)
        if self.temps_reproduction_poisson >= 3:
            self.reproduire(ancienne_position_x, ancienne_position_y)  
            
    def reproduire(self, ancienne_x, ancienne_y):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        random.shuffle(directions)
        for dx, dy in directions:
            x = ancienne_x + dx * self.case_size
            y = ancienne_y + dy * self.case_size

            if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
                continue

            index_x = x // self.case_size
            index_y = y // self.case_size

            if not self.grille_poisson[index_y][index_x]:
                self.grille_poisson[index_y][index_x] = True
                if self.__class__ == Poisson:
                    nouveau_poisson = Poisson(x, y, self.grille_poisson, self.case_size)
                    poissons.add(nouveau_poisson)
                    self.temps_reproduction_poisson = 0
                    break
                elif self.__class__ == Requin:
                    nouveau_poisson = Requin(x, y, self.grille_poisson, self.case_size)
                    poissons.add(nouveau_poisson)
                    self.temps_reproduction_poisson = 0
                    break

#class requin qui hérite de Poisson
class Requin(Poisson):
    def __init__(self, x, y, grille_poisson, case_size):
        super().__init__(x, y, grille_poisson, case_size)
        self.image = pygame.image.load('img/req.png')
        self.rect = self.image.get_rect()
        self.rect.x = x  
        self.rect.y = y  
        self.temps_reproduction_poisson = 0
        self.energie = 6
        self.grille_poisson = grille_poisson
        self.case_size = case_size
        
    def update(self,):
        super().deplacer()
        #self.gestion_energie()
        #stockage de la position pour faire des bébés
        ancienne_position_x = self.rect.x  
        ancienne_position_y = self.rect.y  
        self.temps_reproduction_poisson += 1 #temps de reproduction en chronon (1 chronon = 0.5s voir la boucle de jeu)
        if self.temps_reproduction_poisson >= 5:
            super().reproduire(ancienne_position_x,ancienne_position_y)
   
    # def gestion_energie(self):
    #     global grille_poissons

    #     directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    #     for dx, dy in directions:
    #         nouvelle_position_x = self.rect.x + dx * CASE_SIZE
    #         nouvelle_position_y = self.rect.y + dy * CASE_SIZE
    #         position = self.grille_poisson[nouvelle_position_x][nouvelle_position_y]
    #         if position.__class__ is Poisson:
    #             grille_poissons.remove(position)
    #             self.rect.x = nouvelle_position_x
    #             self.rect.y = nouvelle_position_y
                
        # if pygame.sprite.spritecollideany(poissons, requins):
    # if poisson and requin dans la même case 
    #   poisson.kill())
    #   self.energie += 1
    #   compteur_sans_bouffe = 0 je reinitialise le compteur de la bouffe
    # else 
    #   self.energie -= 1
    #   comteur_sans_bouffe += 1
    # if compteur_sans_bouffe = 3
    #   self.kill()
    
    # def mort(self, chronon_count, energie):
    #    if energie == 0: #or (self.chronon_count >= 4 and compteur nourriture requin == 0):
                            

    # def nourriture(self, chronon_count, energie, poissons_manges):
    #     if poisson and requin dans la même case
    #         requin mange poisson (poisson.kill())
    #         energie += 1
    #     elif energie == 0 or (self.chronon_count >= 4 and compteur nourriture requin == 0):
    #         self.kill()


# Initialisation de Pygame
pygame.init()

WIDTH, HEIGHT = 1000, 1000
CASE_SIZE = 100

# creation fenetre
fenetre = pygame.display.set_mode((WIDTH, HEIGHT))

# couleur du background
ocean = (255, 255, 255)

#definition du background
fenetre.fill(ocean)

#definition de la grille
#liste comprehension qui créé une grille 2d donc une liste de liste
grille_poissons = [[False] * (WIDTH // CASE_SIZE) for _ in range(HEIGHT // CASE_SIZE)]


# creation des groupes de sprite
poissons = pygame.sprite.Group()
requins = pygame.sprite.Group()  # Pas encore utilisé dans ce code

# exemple d'ajout pour un seul poisson 
poisson = Poisson(100, 100, grille_poissons, CASE_SIZE)
poissons.add(poisson)
poisson_2 = Poisson(300, 300, grille_poissons, CASE_SIZE)
poissons.add(poisson_2)  


requin = Requin(200,200, grille_poissons, CASE_SIZE)
requins.add(requin)
requin_2 = Requin(500,500, grille_poissons, CASE_SIZE)
requins.add(requin_2)

chronon_count = 0  # chronon à 0 avant le lancement du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    fenetre.fill(ocean)  # Réinitialise le fond à chaque itération
    
    poissons.update()
    poissons.draw(fenetre)
    requins.update()  # Pas encore utilisé dans ce code
    requins.draw(fenetre)  # Pas encore utilisé dans ce code
    #definition d'un chronon à un demi seconde.
    time.sleep(0.5) 
    #compteur du chronon
    chronon_count += 1
    print(chronon_count)  # voir la console
    pygame.display.update()

# Quitter Pygame
pygame.quit()
