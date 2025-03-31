import pygame


class Obstacle:
    def __init__(self, x, y, width=30, height=30, speed=5):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.active = True

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.active = False

    def draw(self, surface, color=(255, 0, 0)):
        pygame.draw.rect(surface, color, self.rect)
