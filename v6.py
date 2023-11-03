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
        
        directions = [(-1, 0),(0, -1),(0, 1),(1, 0)]
        
        random.shuffle(directions)

        #calcul des nouvelles positions
        for dx, dy in directions:
            nouvelle_position_x = self.rect.x + (dx * self.monde.taille_case) # exemple = 300 + (-1 * 100) = 300 - 100 = 200
            nouvelle_position_y = self.rect.y + (dy * self.monde.taille_case) 
            # print(self.rect.x, self.rect.y)
            # print(nouvelle_position_x, nouvelle_position_y)
            
          
            # gestion du tp
            if nouvelle_position_x < 0:
                nouvelle_position_x = self.monde.largeur - self.monde.taille_case
            elif nouvelle_position_x >= self.monde.largeur:
                nouvelle_position_x = 0

            if nouvelle_position_y < 0:
                nouvelle_position_y = self.monde.hauteur - self.monde.taille_case
            elif nouvelle_position_y >= self.monde.hauteur:
                nouvelle_position_y = 0


            if 0 <= nouvelle_position_x < self.monde.largeur and 0 <= nouvelle_position_y < self.monde.hauteur:
                
                #conversion des coordonnées pixels en grille en divisant par la taille des cases
                index_x = nouvelle_position_x // self.monde.taille_case
                index_y = nouvelle_position_y // self.monde.taille_case

                # print(index_x, index_y)
                
                if not self.monde.grille_poissons[index_y][index_x]:
                    #liberation de l'ancienne case
                    self.monde.grille_poissons[self.rect.y // self.monde.taille_case][self.rect.x // self.monde.taille_case] = False
                    #l'objet est dans sa nouvelle position
                    self.monde.grille_poissons[index_y][index_x] = True
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
            self.chronon = 0
            
    def reproduire(self, ancienne_x, ancienne_y):
        index_x = ancienne_x // self.monde.taille_case
        index_y = ancienne_y // self.monde.taille_case

        #verification si l'ancienne position est libre
        if not self.monde.grille_poissons[index_y][index_x]:
            if self.__class__ == Requin:
                print('requin reproduit')
                self.monde.ajout_requin(ancienne_x, ancienne_y)
            elif self.__class__ == Poisson:
                self.monde.ajout_poisson(ancienne_x, ancienne_y)
            #marquer la case comme occupée et réinitialiser le temps de reproduction
            self.monde.grille_poissons[index_y][index_x] = True
            

#class requin qui hérite de Poisson
class Requin(Poisson):
    def __init__(self, x, y, monde):
        super().__init__(x, y, monde)
        self.image = pygame.image.load('img/requin.png')
        self.rect = self.image.get_rect()
        self.temps_starvation_requin = 30 
        self.energie = 30 
        self.cpt_sans_mange = 0
        self.temps_reproduction_requin = 3
        
    def update(self):
        a_mange = self.gestion_energie()
        ancienne_position_x = self.rect.x
        ancienne_position_y = self.rect.y
        super().update()
        # if not a_mange:
        #     super().deplacer()

        # if self.chronon >= self.temps_reproduction_requin:
        #     super().reproduire(ancienne_position_x, ancienne_position_y)
            

    
        
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
                            fish.kill()  # enlève le poisson du groupe de sprites
                            print("poisson mangé")
                            index_x = nouvelle_position_x // self.monde.taille_case
                            index_y = nouvelle_position_y // self.monde.taille_case
                            self.monde.grille_poissons[index_y][index_x] = False  #libère la grille
                            self.energie += 2
                            print(self.energie)
                            a_mange = True
                            self.cpt_sans_mange = 0 #reinitialise le cpt 
                            break  

        if not a_mange:
            self.energie -= 1
            self.cpt_sans_mange += 1
            
        if self.energie <= 0 or self.cpt_sans_mange == self.temps_starvation_requin:
            self.kill()  
            print("je suis mort")
        
        
            

                        
class Monde:
    def __init__(self, largeur, hauteur, taille_case):
        self.largeur = largeur
        self.hauteur = hauteur
        self.taille_case = taille_case
        self.grille_poissons = [[False] * (largeur // taille_case) for _ in range(hauteur // taille_case)]
        self.poissons_tab = pygame.sprite.Group()
        self.requins_tab = pygame.sprite.Group()
    
    def ajout_poisson(self, x, y):
        nouveau_poisson = Poisson(x, y, self)
        self.poissons_tab.add(nouveau_poisson)
        
    def ajout_requin(self, x, y):
        nouveau_requin = Requin(x, y, self)
        self.requins_tab.add(nouveau_requin)
    
    
    def afficher(self):
        fenetre = pygame.display.set_mode((self.largeur, self.hauteur))
        pygame.display.set_caption("Déplacement et reproduction d'animaux")
        
        # # recuperation des variables input
        # nombre_poisson = int(input("Combien de poisson souhaitez-vous pour commencer ?"))
        # nombre_requins = int(input("Combien de poisson souhaitez-vous pour commencer ?"))
        

        # positions_deja_prises = []

        # # fonction pour générer une position aléatoire non prise
        # def generer_position_aleatoire():
        #     while True:
        #         x = random.randint(self.taille_case, self.largeur - self.taille_case)  # Assurez-vous que cela correspond à votre taille de case
        #         y = random.randint(self.taille_case, self.hauteur - self.taille_case)
        #         if (x, y) not in positions_deja_prises:
        #             positions_deja_prises.append((x, y))
        #             return x, y

        # for _ in range(nombre_poisson):
        #     x, y = generer_position_aleatoire()
        #     self.ajout_poisson(x, y)

        # for _ in range(nombre_requins):
        #     x, y = generer_position_aleatoire()
        #     self.ajout_requin(x, y)
                
        
        
        # Initialisation de Pygame
        pygame.init()


        # couleur du background
        ocean = (176, 224, 230)
       
        #definition du background
        fenetre.fill(ocean)


        chronon_count = 0  # chronon à 0 avant le lancement du jeu
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            fenetre.fill(ocean)  
            
            self.poissons_tab.update()
            self.poissons_tab.draw(fenetre)
            self.requins_tab.update()  # Pas encore utilisé dans ce code
            self.requins_tab.draw(fenetre)  # Pas encore utilisé dans ce code
            
            #definition d'un chronon à un demi seconde.
            time.sleep(0.5) 
            #compteur du chronon
            chronon_count += 1
            print(chronon_count)  # voir la console
            pygame.display.update()

        # Quitter Pygame
        pygame.quit()

monde = Monde(1000, 1000, 50)
#Ajouter des poissons
monde.ajout_poisson(150, 250)
monde.ajout_poisson(350, 100)
monde.ajout_requin(450, 500)
monde.ajout_requin(550, 200)
monde.ajout_requin(650, 700)
monde.ajout_poisson(200, 800)
monde.ajout_poisson(800, 150)
monde.ajout_poisson(900, 300)
monde.ajout_requin(300, 500)
monde.ajout_requin(100, 750)
monde.ajout_requin(600, 850)
monde.ajout_requin(850, 550)
monde.afficher()