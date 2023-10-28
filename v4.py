import pygame
import random
import time



#definition de la classe animaux
class Animaux(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
#definition de la classe poisson qui herite de animaux
class Poisson(Animaux):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('img/poisson-rouge.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.temps_reproduction_poisson = 0  # age du poisson en chronons

    def deplacer(self):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        random.shuffle(directions)

        for dx, dy in directions:
            nouvelle_position_x = self.rect.x + dx * CASE_SIZE
            nouvelle_position_y = self.rect.y + dy * CASE_SIZE

            # gestion du tp
            if nouvelle_position_x < 0:
                nouvelle_position_x = WIDTH - CASE_SIZE
            elif nouvelle_position_x >= WIDTH:
                nouvelle_position_x = 0

            if nouvelle_position_y < 0:
                nouvelle_position_y = HEIGHT - CASE_SIZE
            elif nouvelle_position_y >= HEIGHT:
                nouvelle_position_y = 0

            index_x = nouvelle_position_x // CASE_SIZE
            index_y = nouvelle_position_y // CASE_SIZE

            # verification si le point x et y remplissent les conditions pour le deplacement
            if 0 <= index_x < WIDTH // CASE_SIZE and 0 <= index_y < HEIGHT // CASE_SIZE:
                if not grille_poissons[index_y][index_x]:
                    grille_poissons[self.rect.y // CASE_SIZE][self.rect.x // CASE_SIZE] = False
                    grille_poissons[index_y][index_x] = True
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
        index_x = ancienne_x // CASE_SIZE
        index_y = ancienne_y // CASE_SIZE
        if not grille_poissons[index_y][index_x]:
            grille_poissons[index_y][index_x] = True
            nouveau_poisson = Poisson(ancienne_x, ancienne_y)
            poissons.add(nouveau_poisson)
            self.temps_reproduction_poisson = 0
        
        
# class requin qui hérite de Poisson
class Requin(Poisson):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.temps_reproduction_poisson = 0
        self.energie = 6
        
    def update(self):
        super().__init__()
        self.gestion_energie()
        
    def reproduction(self):
        super().__init__()

    def gestion_energie(self):
        pass
    #if poisson and requin dans la même case 
    #   poisson.kill())
    #   self.energie += 1
    #   compteur_sans_bouffe = 0 je reinitialise le compteur de la bouffe
    # else 
    #   self.energie -= 1
    #   comteur_sans_bouffe += 1
    #if compteur_sans_bouffe = 3
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


# dessin des lignes de la grille
for x in range(0, WIDTH, CASE_SIZE): 
    pygame.draw.line(fenetre, (0, 0, 0), (x, 0), (x, HEIGHT))
    pygame.draw.line(fenetre, (0, 0, 0), (0, x), (WIDTH, x))
# creation des groupes de sprite, un groupe pour les poissons et pour les requins(mais la classe pas encore faite)
poissons = pygame.sprite.Group()
requins = pygame.sprite.Group()#pour apres

# exemple d'ajout pour un seul  poisson 
poisson = Poisson(100, 100)
poissons.add(poisson)
poisson_2 = Poisson(300, 300)
poissons.add(poisson_2)

### attention -> pour le moment le fait de rajouter les entités avec une boucle range ça fini par créé des chevauchements des poissons
#je prefere pour le moment les initialiser comme plus haut
# ajout pour plusieurs poisson avec la boucle
# nb_poisson = 5

# for poisson in range(nb_poisson):
#     position_x = random.randint(0, WIDTH - CASE_SIZE) #randint entre 0 et width - case_size pour eviter qu'ils se retrouvent hors ecran
#     position_y = random.randint(0, HEIGHT - CASE_SIZE)
#     nouveau_poisson = (Poisson(position_x, position_y))
#     poissons.add(nouveau_poisson)
    

chronon_count = 0 #chronon à 0 avant le lancement du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    poissons.update()
    poissons.draw(fenetre)
    #definition d'un chronon à un demi seconde.
    chronon = time.sleep(0.5) 
    #compteur du chronon
    chronon_count += 1
    print(chronon_count) #voir la console
    pygame.display.update()


# Quitter Pygame
pygame.quit()
