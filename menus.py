import pygame
import sys
from game import Game

# Initialisation de Pygame
pygame.init()

class MainMenu:
    def __init__(self):
        # Configuration de la fenêtre
        self.screen = pygame.display.set_mode((700, 600))
        pygame.display.set_caption("Miner-Game")
        self.fenetre_width, self.fenetre_height = self.screen.get_size()
        
        # Chargement et redimensionnement de l'image de fond
        fond = pygame.image.load("Images/fond_menu.png").convert()
        self.fond = pygame.transform.scale(fond, (self.fenetre_width, self.fenetre_height))
        
        # Chargement de l'icône
        try:
            icon = pygame.image.load("Images/icon.png")
            pygame.display.set_icon(icon)
        except pygame.error:
            print("Impossible de charger l'icône. Assurez-vous que le chemin est correct.")
        
        # Initialisation des couleurs
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        self.BLACK = (0, 0, 0)
        
        # Initialisation de la police
        self.titleFont = pygame.font.Font(None, 80)  # Taille de la police 30
        self.mainFont = pygame.font.Font(None, 50)  # Taille de la police 50
        self.exitFont= pygame.font.Font(None, 40)  # Taille de la police 30
        # Dimensions de la fenêtre
        self.fenetre_width, self.fenetre_height = self.screen.get_size()
        
        # Liste des boutons
        self.buttons = []

    def Start(self) -> None:
        while True:
            # Remplir l'écran avec la couleur blanche
            self.screen.blit(self.fond, (0, 0))
            
            # Création du titre
            title = self.titleFont.render("MINER GAME", True, self.BLACK)
            title_Rect = title.get_rect()
            title_Rect.center = (self.fenetre_width / 2, self.fenetre_height / 15)
            self.screen.blit(title, title_Rect)
            
            # Positions des boutons
            PlayGameBtn_rect = pygame.Rect(
                (self.fenetre_width - 300) / 2,
                self.fenetre_height / 2.3,
                300,
                80,
            )
            QuitBtn_rect = pygame.Rect(
                (self.fenetre_width - 150) / 2,
                self.fenetre_height / 1.3,
                150,
                40,
            )
            # Ajouter un fond et une bordure aux boutons
            pygame.draw.rect(self.screen, (200, 200, 200), PlayGameBtn_rect, border_radius=15)  # Fond gris clair
            pygame.draw.rect(self.screen, self.BLACK, PlayGameBtn_rect, 3, border_radius=15)    # Bordure noire
            
            pygame.draw.rect(self.screen, (200, 200, 200), QuitBtn_rect, border_radius=15)  # Fond gris clair
            pygame.draw.rect(self.screen, self.BLACK, QuitBtn_rect, 3, border_radius=15)    # Bordure noire
            
            # Ajouter le texte sur les boutons
            PlayGameBtn = self.mainFont.render("PLAY GAME", True, self.BLACK)
            PlayGameBtn_rect = PlayGameBtn.get_rect(center=PlayGameBtn_rect.center)
            self.screen.blit(PlayGameBtn, PlayGameBtn_rect)
            
            QuitBtn = self.exitFont.render("QUIT", True, self.RED)
            QuitBtn_rect = QuitBtn.get_rect(center=QuitBtn_rect.center)
            self.screen.blit(QuitBtn, QuitBtn_rect)
            
             # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche
                    if PlayGameBtn_rect.collidepoint(event.pos):
                        game=Game()
                        game.main_loop()
                    if QuitBtn_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                        
            
            # Mettre à jour l'écran
            pygame.display.flip()

