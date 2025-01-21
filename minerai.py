import pygame

class Minerai:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (139, 69, 19)  # Marron pour représenter un minerai

    def draw(self, fenetre):
        pygame.draw.rect(fenetre, self.color, self.rect)
