import pygame
import math

class Player:
    def __init__(self, x, y, width, height, sprite_sheet_path, color=(255, 0, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.speed = 3
        self.buttons = []  # Stocker les boutons visibles
        self.tiles = []
        self.coins = 0  # Par défaut, 0 pièces
        self.backpack({"charbon": 0, "fer": 0, "or": 0, "diamant": 0, "amethyste": 0})

        # Animation
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.frames = self._load_frames(6, 4, width, height)  # 6 colonnes, 4 lignes
        self.animations = {
            "idle": self.frames[0:6],  # Liste simple de frames
            "right": self.frames[6:12],  # Colonne 2
            "up": self.frames[12:18],  # Ligne 3
            "down": self.frames[18:24],  # Ligne 2
        }
        self.current_animation = "idle"
        self.animation_index = 0
        self.animation_speed = 0.2  # Contrôle la vitesse de l'animation
        self.flip = False  # Inverser les sprites
        self.time_elapsed = 0

    def _load_frames(self, columns, rows, frame_width, frame_height):
        frames = []
        for y in range(rows):
            for x in range(columns):
                frame = self.sprite_sheet.subsurface(
                    pygame.Rect(x * frame_width, y * frame_height, frame_width, frame_height)
                )
                frames.append(frame)
        return frames

    def move(self, keys, collision_rects, dt):
        dx, dy = 0, 0
        self.current_animation = "idle"

        if keys[pygame.K_z]:
            dy -= self.speed
            self.current_animation = "up"
        if keys[pygame.K_s]:
            dy += self.speed
            self.current_animation = "down"
        if keys[pygame.K_q]:
            dx -= self.speed
            self.current_animation = "right"  # Marche à droite mais inversée
            self.flip = True
        if keys[pygame.K_d]:
            dx += self.speed
            self.current_animation = "right"
            self.flip = False

        # Vérification des collisions
        future_rect = self.rect.move(dx, dy)
        future_rect_x = self.rect.move(dx, 0)
        future_rect_y = self.rect.move(0, dy)

        for rect, obj_name in collision_rects:
            if future_rect_x.colliderect(rect):
                if dx > 0:
                    dx = rect.left - self.rect.right
                elif dx < 0:
                    dx = rect.right - self.rect.left

        self.rect.x += dx

        for rect, obj_name in collision_rects:
            if future_rect_y.colliderect(rect):
                if dy > 0:
                    dy = rect.top - self.rect.bottom
                elif dy < 0:
                    dy = rect.bottom - self.rect.top

        self.rect.y += dy

        # Animation index mise à jour
        if dx != 0 or dy != 0:  # Si le joueur se déplace
            self.time_elapsed += dt
            if self.time_elapsed > self.animation_speed:
                self.time_elapsed = 0
                self.animation_index = (self.animation_index + 1) % len(self.animations[self.current_animation])
        else:  # Réinitialiser l'animation si le joueur est immobile
            self.animation_index = 0
            
    def backpack(self, minerais):
        # Initialiser l'inventaire s'il n'existe pas
        if not hasattr(self, "inventory"):
            self.inventory = {
                "charbon": 0,
                "fer": 0,
                "or": 0,
                "diamant": 0,
                "amethyste": 0
            }

        # Ajouter les minerais à l'inventaire
        for minerai, quantité in minerais.items():
            if minerai in self.inventory:
                self.inventory[minerai] += quantité
            else:
                self.inventory[minerai] = quantité
        
        
    def money(self, amount):
        # Initialiser l'argent s'il n'existe pas
        if not hasattr(self, "coins"):
            self.coins = 0

        # Ajouter ou soustraire de l'argent
        self.coins += amount

        # Assurer que l'argent ne devienne pas négatif
        if self.coins < 0:
            self.coins = 0

        
        
    def draw(self, screen, camp, proximity_distance):
        
        if self.current_animation not in self.animations or not self.animations[self.current_animation]:
            self.current_animation = "idle"  # Revenir à l'animation par défaut

        # Protection de l'index
        frame_list = self.animations[self.current_animation]
        if frame_list:  # Si l'animation a des frames
            self.animation_index %= len(frame_list)  # Boucle sur les frames
            frame = frame_list[self.animation_index]
            if self.flip:
                frame = pygame.transform.flip(frame, True, False)
            screen.blit(frame, (self.rect.x, self.rect.y))

        self.buttons.clear()

        # Vérifie la proximité et dessine les boutons
        for object_name in ["Base", "Forge", "Shop", "Mine"]:
            button_rect = self._check_and_draw_button(screen, camp, object_name, proximity_distance)
            if button_rect:
                self.buttons.append((button_rect, object_name))
                
        # --- Afficher les informations ---
        font = pygame.font.Font(None, 36)

        # Affichage de l'argent
        if hasattr(self, "coins"):
            money_text = f"Argent : {self.coins} pièces"
            money_surface = font.render(money_text, True, (255, 255, 0))  # Texte jaune
            screen.blit(money_surface, (10, 10))

        # Affichage du sac à dos (inventaire)
        if hasattr(self, "inventory"):
            y_offset = 50  # Décalage initial sous l'argent
            for minerai in ["charbon", "fer", "or", "diamant", "amethyste"]:
                quantité = self.inventory.get(minerai, 0)
                item_text = f"{minerai.capitalize()} : {quantité}"
                item_surface = font.render(item_text, True, (255, 255, 255))  # Texte blanc
                screen.blit(item_surface, (10, y_offset))
                y_offset += 30  # Décalage pour chaque ligne

    def _check_and_draw_button(self, screen, camp, object_name, proximity_distance):
        obj_position = camp.get_scaled_object_position(object_name)
        if obj_position:
            obj_x, obj_y = obj_position
            obj_rect = pygame.Rect(obj_x, obj_y, 100, 50)

            distance = math.sqrt((self.rect.centerx - obj_rect.centerx) ** 2 + (self.rect.centery - obj_rect.centery) ** 2)

            if distance <= proximity_distance:
                pygame.draw.rect(screen, (0, 255, 0), obj_rect)
                font = pygame.font.Font(None, 36)
                text = font.render(object_name.capitalize(), True, (0, 0, 0))
                screen.blit(text, (obj_rect.x + 10, obj_rect.y + 10))
                return obj_rect
        return None

    def check_button_click(self, mouse_pos):
        for button_rect, object_name in self.buttons:
            if button_rect.collidepoint(mouse_pos):
                print(f"Clic sur le bouton : {object_name}")
                return object_name
        return None