import pygame
from camp import Camp
from player import Player
from mine import Mine

pygame.font.init()

class Game:
    def __init__(self):
        self.fenetre = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.background_color = (0, 0, 0)
        self.fenetre_width, self.fenetre_height = pygame.display.get_surface().get_size()
        self.horloge = pygame.time.Clock()

        self.camp = Camp("Maps/map_camp.tmx", self.fenetre_width, self.fenetre_height)

        player_spawn = self.camp.get_scaled_object_position("SpawnPoint")
        if player_spawn:
            spawn_x, spawn_y = player_spawn
        else:
            print("Erreur : Objet 'SpawnPoint' non trouvé dans la carte.")
            spawn_x, spawn_y = 100, 100

        # Charger l'image des sprites du joueur
        sprite_sheet_path = "Images/Player.png"
        self.player = Player(spawn_x, spawn_y, 30, 30, sprite_sheet_path)
        
        # charger la mine
        self.in_mine = False
        self.mine = Mine("Maps/map_mine.tmx", self.fenetre_width, self.fenetre_height)
        
        self.running = True
        self.proximity_distance = 300  # Distance à partir de laquelle les boutons apparaissent

    def main_loop(self):
        collision_rects = self.camp.get_collision_rects()
        while self.running:
            dt = self.horloge.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if not self.in_mine:
                        clicked_object = self.player.check_button_click(mouse_pos)
                        if clicked_object == "Mine":  # Assurez-vous que le nom de l'objet est "Mine"
                            print("Entrée dans la mine")
                            self.in_mine = True

            keys = pygame.key.get_pressed()

            if self.in_mine:
                # Logique dans la mine
                self.player.move(keys, [], dt)
                self.mine.collect_minerai(self.player.rect)
                self.fenetre.fill(self.background_color)
                self.mine.draw(self.fenetre)
                self.player.draw(self.fenetre, self.mine, self.proximity_distance)
            else:
                # Logique sur la carte principale
                self.player.move(keys, collision_rects, dt)
                self.fenetre.fill(self.background_color)
                self.camp.draw(self.fenetre)
                self.player.draw(self.fenetre, self.camp, self.proximity_distance)

            pygame.display.flip()
