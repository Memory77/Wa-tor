import pygame
import random
import time





class Poisson(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('img/poisson5.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.temps_reproduction_poisson = 0  

    def deplacer(self):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        random.shuffle(directions)

        for dx, dy in directions:
            nouvelle_position_x = self.rect.x + dx * Tableau.taille_case
            nouvelle_position_y = self.rect.y + dy * Tableau.taille_case

            # gestion du tp
            if nouvelle_position_x < 0:
                nouvelle_position_x = Tableau.largeur - Tableau.taille_case
            elif nouvelle_position_x >= Tableau.largeur:
                nouvelle_position_x = 0

            if nouvelle_position_y < 0:
                nouvelle_position_y = Tableau.hauteur - Tableau.taille_case
            elif nouvelle_position_y >= Tableau.hauteur:
                nouvelle_position_y = 0

            index_x = nouvelle_position_x // Tableau.taille_case
            index_y = nouvelle_position_y // Tableau.taille_case

            # verification si le point x et y remplissent les conditions pour le deplacement
            if 0 <= index_x < Tableau.largeur // Tableau.taille_case and 0 <= index_y < Tableau.hauteur // Tableau.taille_case:
                if not Tableau.grille_poissons[index_y][index_x]:
                    Tableau.grille_poissons[self.rect.y // Tableau.taille_case][self.rect.x // Tableau.taille_case] = False
                    Tableau.grille_poissons[index_y][index_x] = True
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
            x = ancienne_x + dx * Tableau.taille_case
            y = ancienne_y + dy * Tableau.taille_case

            if x < 0 or x >= Tableau.largeur or y < 0 or y >= Tableau.hauteur:
                continue

            index_x = x // Tableau.taille_case
            index_y = y // Tableau.taille_case

            if not Tableau.grille_poissons[index_y][index_x]:
                Tableau.grille_poissons[index_y][index_x] = True
                if self.__class__ == Poisson:
                    nouveau_poisson = Poisson(x, y)
                    Tableau.poissons.add(nouveau_poisson)
                    self.temps_reproduction_poisson = 0
                    break
                elif self.__class__ == Requin:
                    nouveau_poisson = Requin(x, y)
                    Tableau.requins.add(nouveau_poisson)
                    self.temps_reproduction_poisson = 0
                    break

#class requin qui hérite de Poisson
class Requin(Poisson):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.image.load('img/req.png')
        self.rect = self.image.get_rect()
        self.rect.x = x  
        self.rect.y = y  
        self.temps_reproduction_poisson = 0
        self.energie = 6
        
        
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
    




class Tableau:
    def __init__(self, largeur, hauteur, taille_case):
        self.largeur = largeur  # Largeur de la fenêtre en pixels
        self.hauteur = hauteur  # Hauteur de la fenêtre en pixels
        self.taille_case = taille_case  # Taille d'une case en pixels
        self.fenetre = pygame.display.set_mode((largeur, hauteur))  
        self.grille_poissons = [[False] * (largeur // taille_case) for _ in range(hauteur // taille_case)] # Liste pour stocker les animaux (Poissons et Requins)
        self.poissons = pygame.sprite.Group()
        self.requins = pygame.sprite.Group()


    def afficher(self):
        # Initialisation de Pygame
        pygame.init()

        # couleur de la couleur
        ocean = (255, 255, 255)
        fenetre = self.fenetre
        #definition du background
        fenetre.fill(ocean) 


        # exemple d'ajout pour un seul poisson 
        poisson = Poisson(100, 100)
        self.poissons.add(poisson)
        poisson_2 = Poisson(300, 300)
        self.poissons.add(poisson_2)  

        requin = Requin(200,200)
        self.requins.add(requin)
        requin_2 = Requin(500,500)
        self.requins.add(requin_2)


        chronon_count = 0  # chronon à 0 avant le lancement du jeu
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.poissons.update()
            self.poissons.draw(fenetre)
            self.requins.update()  
            self.requins.draw(fenetre)  
            #definition d'un chronon à un demi seconde.
            time.sleep(0.5) 
            #compteur du chronon
            chronon_count += 1
            print(chronon_count)  # voir la console
            pygame.display.update()

        # Quitter Pygame
        pygame.quit()




monde = Tableau(1000,1000,100)

monde.afficher()