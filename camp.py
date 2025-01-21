import pygame
import pytmx

class Camp:
    def __init__(self, tmx_file, screen_width, screen_height):
        # Charger la carte
        self.tmx_data = pytmx.load_pygame(tmx_file, pixelalpha=True)
        
        # Dimensions originales de la carte
        self.map_width = self.tmx_data.width * self.tmx_data.tilewidth
        self.map_height = self.tmx_data.height * self.tmx_data.tileheight

        # Calcul du facteur d'échelle
        self.scale_x = screen_width / self.map_width
        self.scale_y = screen_height / self.map_height

        # Choix du facteur d'échelle le plus adapté
        self.scale = min(self.scale_x, self.scale_y)

        # Taille des tuiles redimensionnées
        self.scaled_tile_width = int(self.tmx_data.tilewidth * self.scale)
        self.scaled_tile_height = int(self.tmx_data.tileheight * self.scale)

        # Chargement des objets
        self.map_objects = self.load_objects()
        
    def draw(self, screen):
        # Parcourir les calques visibles
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        # Redimensionner la tuile
                        tile = pygame.transform.scale(
                            tile, (self.scaled_tile_width, self.scaled_tile_height)
                        )
                        # Dessiner la tuile redimensionnée
                        screen.blit(
                            tile,
                            (
                                x * self.scaled_tile_width,
                                y * self.scaled_tile_height,
                            ),
                        )
    def get_object_by_name(self, name):
        # Rechercher un objet par son nom 
        for obj in self.tmx_data.objects:
            if obj.name == name:
                return obj
        return None
    
    def get_scaled_object_position(self, name):
        obj = self.get_object_by_name(name)
        if obj:
            scaled_x = obj.x * self.scale
            scaled_y = obj.y * self.scale
            return scaled_x, scaled_y
        return None
    
    def load_objects(self):
        # Charge les objets depuis le fichier .tmx
        objects = []
        for obj in self.tmx_data.objects:
            scaled_position = self.get_scaled_object_position(obj.name)
            if scaled_position:
                scaled_x, scaled_y = scaled_position
            else:
                scaled_x, scaled_y = obj.x, obj.y  # Utiliser les coordonnées d'origine si la redimension échoue
            objects.append({
                "name": obj.name,
                "type": obj.type,
                "x": scaled_x,
                "y": scaled_y,
                "width": obj.width * self.scale,  # Adapter la largeur à l'échelle
                "height": obj.height * self.scale  # Adapter la hauteur à l'échelle
            })
        return objects
    
    def get_object_rect(self, name):
        for obj in self.tmx_data.objects:
            if obj.name == name:
                return pygame.Rect(obj.x * self.scale, obj.y * self.scale, obj.width * self.scale, obj.height * self.scale)
        return None
    
    def get_collision_rects(self):
        collision_rects = []
        for obj in self.map_objects:  # Parcourez tous les objets de la carte
            if obj.get('type') == 'collision':  # Vérifiez si l'objet est un objet de collision
                x, y, width, height = obj['x'], obj['y'], obj['width'], obj['height']
                rect = pygame.Rect(x, y, width, height)
                collision_rects.append((rect, obj['name']))  # Ajouter le nom de l'objet avec le rectangle
        return collision_rects
    
    