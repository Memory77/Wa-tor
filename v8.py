import pygame
import random
import time

# Initialisation de Pygame
pygame.init()

class Monde:
    def __init__(self, largeur, hauteur, case_size):
        self.largeur = largeur
        self.hauteur = hauteur
        self.case_size = case_size
        self.grille_poissons = [[False] * (largeur // case_size) for _ in range(hauteur // case_size)]
        self.poissons_tab = pygame.sprite.Group()
        self.requins_tab = pygame.sprite.Group()
        self.grille_algues = [[False] * (largeur // case_size) for _ in range(hauteur // case_size)]
        self.algues_tab = pygame.sprite.Group()
    
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
        fenetre = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Déplacement et reproduction d'animaux")
        ocean = (176, 224, 230)
        fenetre.fill(ocean)
        self.algues_tab.draw(fenetre)
        self.poissons_tab.draw(fenetre)
        self.requins_tab.draw(fenetre)
        pygame.display.update()

class Algue(pygame.sprite.Sprite):
    def __init__(self, x, y, monde):
        super().__init__()
        self.image = pygame.image.load('img/algues.png')
        self.rect = self.image.get_rect(topleft=(x, y))
        self.monde = monde
        
class Poisson(pygame.sprite.Sprite):
    def __init__(self, x, y, monde):
        super().__init__()
        self.image = pygame.image.load('img/poisson5.png')
        self.rect = self.image.get_rect(topleft=(x, y))
        self.chronon = 0
        self.temps_reproduction_poisson = 3
        self.monde = monde
        
    def deplacer(self):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        random.shuffle(directions)

        for dx, dy in directions:
            nouvelle_position_x = self.rect.x + (dx * self.monde.case_size)
            nouvelle_position_y = self.rect.y + (dy * self.monde.case_size)
            
            # Gestion du tp (téléportation aux bords de l'écran)
            if nouvelle_position_x < 0:
                nouvelle_position_x = self.monde.largeur - self.monde.case_size
            elif nouvelle_position_x >= self.monde.largeur:
                nouvelle_position_x = 0

            if nouvelle_position_y < 0:
                nouvelle_position_y = self.monde.hauteur - self.monde.case_size
            elif nouvelle_position_y >= self.monde.hauteur:
                nouvelle_position_y = 0

            # Conversion des coordonnées pixels en indices de la grille
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
        #recuperation des anciennes positions avant de se déplacer
        ancienne_position_x = self.rect.x
        ancienne_position_y = self.rect.y

        self.deplacer()

        self.chronon += 1
        if self.chronon >= self.temps_reproduction_poisson:
            self.reproduire(ancienne_position_x, ancienne_position_y)


    def reproduire(self, ancienne_x, ancienne_y):
        index_x = ancienne_x // self.monde.case_size
        index_y = ancienne_y // self.monde.case_size

        #verification si l'ancienne position est libre
        if not self.monde.grille_poissons[index_y][index_x]:
            if self.__class__ == Poisson:
                self.monde.ajout_poisson(ancienne_x, ancienne_y)
            elif self.__class__ == Requin:
                self.monde.ajout_requin(ancienne_x, ancienne_y)
                print('requin reproduit')
            #marquer la case comme occupée et réinitialiser le temps de reproduction
            self.monde.grille_poissons[index_y][index_x] = True
        self.chronon = 0   


class Requin(Poisson):
    def __init__(self, x, y, monde):
        super().__init__(x, y, monde)
        self.image = pygame.image.load('img/req.png')
        self.rect = self.image.get_rect(topleft=(x, y))
        self.temps_survie_requin = 8
        self.temps_reproduction_requin = 10
        self.energie = 10
        self.cpt_sans_mange = 0
        
    def update(self):
        self.gestion_energie()
        #recuperation des anciennes positions avant de se déplacer
        ancienne_position_x = self.rect.x  
        ancienne_position_y = self.rect.y  
        self.deplacer()
          
        self.chronon += 1 #temps de reproduction en chronon voir time.sleep()
        if self.chronon >= self.temps_reproduction_requin:
            super().reproduire(ancienne_position_x,ancienne_position_y)

    def gestion_energie(self):
    
        a_mange = False
        cpt_sans_mange = 0
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
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
                            self.monde.grille_poissons[index_y][index_x] = False  #libère la grille
                            self.energie += 1
                            a_mange = True
                            cpt_sans_mange = 0 #reinitialise le cpt 
                            break  

        if not a_mange:
            self.energie -= 1
            self.cpt_sans_mange += 1  # Incrémenter l'attribut de l'instance
        else:
            self.cpt_sans_mange = 0  # Réinitialiser si le requin a mangé

        if self.energie <= 0 or self.cpt_sans_mange >= self.temps_survie_requin:
            self.kill()  




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
monde.ajout_requin(100, 100)
monde.ajout_algue(500, 750)
monde.ajout_algue(200, 200)
monde.ajout_algue(800, 200)

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    monde.afficher()  
    monde.poissons_tab.update()
    monde.requins_tab.update()
    time.sleep(0.5)


# Quitter Pygame
pygame.quit()
