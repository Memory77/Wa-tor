import pygame
import random
import time

class Poisson(pygame.sprite.Sprite):
    def __init__(self, x, y, grille_poisson, case_size):
        super().__init__()
        self.image = pygame.image.load('img/poisson-clown.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.chronon = 0
        self.temps_reproduction_poisson = 2
        self.grille_poisson = grille_poisson
        self.case_size = case_size

    def deplacer(self):
        
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        random.shuffle(directions)

        #calcul des nouvelles positions
        for dx, dy in directions:
            nouvelle_position_x = self.rect.x + (dx * self.case_size) # exemple = 300 + (-1 * 100) = 300 - 100 = 200
            nouvelle_position_y = self.rect.y + (dy * self.case_size)
            # print(self.rect.x, self.rect.y)
            # print(nouvelle_position_x, nouvelle_position_y)
            
          
            # gestion du tp
            if nouvelle_position_x < 0:
                nouvelle_position_x = WIDTH - self.case_size
            elif nouvelle_position_x >= WIDTH:
                nouvelle_position_x = 0

            if nouvelle_position_y < 0:
                nouvelle_position_y = HEIGHT - self.case_size
            elif nouvelle_position_y >= HEIGHT:
                nouvelle_position_y = 0


            if 0 <= nouvelle_position_x < WIDTH and 0 <= nouvelle_position_y < HEIGHT:
                
                #conversion des coordonnées pixels en grille en divisant par la taille des cases
                index_x = nouvelle_position_x // self.case_size
                index_y = nouvelle_position_y // self.case_size

                # print(index_x, index_y)
                
                if not self.grille_poisson[index_y][index_x]:
                    #liberation de l'ancienne case
                    self.grille_poisson[self.rect.y // self.case_size][self.rect.x // self.case_size] = False
                    #l'objet est dans sa nouvelle position
                    self.grille_poisson[index_y][index_x] = True
                    self.rect.x = nouvelle_position_x
                    self.rect.y = nouvelle_position_y
                    break
        
    
    def update(self):
        #recuperation des anciennes positions avant de se déplacer
        ancienne_position_x = self.rect.x
        ancienne_position_y = self.rect.y

        self.deplacer()

        self.chronon += 1
        if self.chronon >= self.temps_reproduction_poisson:
            self.reproduire(ancienne_position_x, ancienne_position_y)

    def reproduire(self, ancienne_x, ancienne_y):
        index_x = ancienne_x // self.case_size
        index_y = ancienne_y // self.case_size

        #verification si l'ancienne position est libre
        if not self.grille_poisson[index_y][index_x]:
            if self.__class__ == Poisson:
                nouveau_poisson = Poisson(ancienne_x, ancienne_y, self.grille_poisson, self.case_size)
                poissons.add(nouveau_poisson)
            elif self.__class__ == Requin:
                nouveau_requin = Requin(ancienne_x, ancienne_y, self.grille_poisson, self.case_size)
                requins.add(nouveau_requin)
            #marquer la case comme occupée et réinitialiser le temps de reproduction
            self.grille_poisson[index_y][index_x] = True
            self.chronon = 0   

#class requin qui hérite de Poisson
class Requin(Poisson):
    def __init__(self, x, y, grille_poisson, case_size):
        super().__init__(x, y, grille_poisson, case_size)
        self.image = pygame.image.load('img/requin.png')
        self.rect = self.image.get_rect()
        self.rect.x = x  
        self.rect.y = y  
        self.temps_starvation_requin = 4
        self.temps_reproduction_requin = 6
        self.energie = 3
        self.grille_poisson = grille_poisson
        self.case_size = case_size
        
    def update(self):
        self.gestion_energie()
        #recuperation des anciennes positions avant de se déplacer
        ancienne_position_x = self.rect.x  
        ancienne_position_y = self.rect.y  
        super().deplacer()
          
        self.chronon += 1 #temps de reproduction en chronon voir time.sleep()
        if self.chronon >= self.temps_reproduction_requin:
            super().reproduire(ancienne_position_x,ancienne_position_y)
   
    def gestion_energie(self):
        global poissons

        a_mange = False
        cpt_sans_mange = 0
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for dx, dy in directions:
            nouvelle_position_x = self.rect.x + dx * self.case_size
            nouvelle_position_y = self.rect.y + dy * self.case_size

            if 0 <= nouvelle_position_x < WIDTH and 0 <= nouvelle_position_y < HEIGHT:
                for fish in poissons:
                    if isinstance(fish, Poisson) and not isinstance(fish, Requin):
                        if fish.rect.x == nouvelle_position_x and fish.rect.y == nouvelle_position_y:
                            fish.kill()  # enlève le poisson du groupe de sprites
                            print("poisson mangé")
                            index_x = nouvelle_position_x // self.case_size
                            index_y = nouvelle_position_y // self.case_size
                            self.grille_poisson[index_y][index_x] = False  #libère la grille
                            self.energie += 1
                            a_mange = True
                            cpt_sans_mange = 0 #reinitialise le cpt 
                            break  

        if not a_mange:
            self.energie -= 1
            cpt_sans_mange += 1

        if self.energie <= 0 or cpt_sans_mange == self.temps_starvation_requin:
            self.kill()  





    
# Initialisation de Pygame
pygame.init()

WIDTH, HEIGHT = 1000, 1000
CASE_SIZE = 50

# creation fenetre
fenetre = pygame.display.set_mode((WIDTH, HEIGHT))

# couleur du background
ocean = (176, 224, 230)

#definition du background
fenetre.fill(ocean)

#definition de la grille
#liste comprehension qui créé une grille 2d donc une liste de liste
grille_poissons = [[False] * (WIDTH // CASE_SIZE) for _ in range(HEIGHT // CASE_SIZE)]


# creation des groupes de sprite
poissons = pygame.sprite.Group()
requins = pygame.sprite.Group()  

# exemple d'ajout pour un seul poisson 
poisson = Poisson(100, 100, grille_poissons, CASE_SIZE)
poissons.add(poisson)
poisson_2 = Poisson(300, 300, grille_poissons, CASE_SIZE)
poissons.add(poisson_2)  
poisson_3 = Poisson(500, 400, grille_poissons, CASE_SIZE)
poissons.add(poisson_3) 

requin = Requin(200,200, grille_poissons, CASE_SIZE)
requins.add(requin)
requin_2 = Requin(500,500, grille_poissons, CASE_SIZE)
requins.add(requin_2)
requin_3 = Requin(800,500, grille_poissons, CASE_SIZE)
requins.add(requin_3)

chronon_count = 0  # chronon à 0 avant le lancement du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    fenetre.fill(ocean)  
    
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
