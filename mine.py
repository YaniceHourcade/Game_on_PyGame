import pygame
from random import randint
from minerai import Minerai
import pytmx  # Assurez-vous d'avoir pytmx installé

class Minerai:
    def __init__(self, x, y, width, height, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, fenetre):
        fenetre.blit(self.image, self.rect.topleft)

class Mine:
    def __init__(self, map_path, fenetre_width, fenetre_height):
        self.map_path = map_path
        self.fenetre_width = fenetre_width
        self.fenetre_height = fenetre_height
        self.minerais = []
        self.create_minerais()
        self.background_color = (50, 50, 50)  # Couleur de fond de la mine

        # Charger la carte Tiled
        self.tmx_data = pytmx.TiledMap(map_path)
        self.map_width = self.tmx_data.width * self.tmx_data.tilewidth
        self.map_height = self.tmx_data.height * self.tmx_data.tileheight
        self.scale_x = fenetre_width / self.map_width
        self.scale_y = fenetre_height / self.map_height

    def get_scaled_object_position(self, object_name):
        for obj in self.tmx_data.objects:
            if obj.name == object_name:
                return obj.x * self.scale_x, obj.y * self.scale_y
        return None

    def create_minerais(self):
        image_path = "Images/icon.png"
        # Génère quelques minerais aléatoirement dans la mine
        for _ in range(30):  # Exemple : 10 minerais
            x = randint(100, self.fenetre_width - 100)  # Utiliser randint ici
            y = randint(100, self.fenetre_height - 100)
            self.minerais.append(Minerai(x, y, 20, 20, image_path))

    def draw(self, fenetre):
        fenetre.fill(self.background_color)
        for minerai in self.minerais:
            minerai.draw(fenetre)

    def collect_minerai(self, player_rect):
        for minerai in self.minerais[:]:
            if player_rect.colliderect(minerai.rect):
                self.minerais.remove(minerai)
                print("Minerai collecté !")
