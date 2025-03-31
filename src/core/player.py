import pygame


class Player:
    def __init__(self, x, y, width=50, height=80):
        self.rect = pygame.Rect(x, y, width, height)
        self.velocity = 0
        self.gravity = 0.5
        self.jump_velocity = -15
        self.is_grounded = True

    def update(self, ground_level):
        self.velocity += self.gravity
        self.rect.y += self.velocity

        if self.rect.bottom > ground_level:
            self.rect.bottom = ground_level
            self.velocity = 0
            self.is_grounded = True
        else:
            self.is_grounded = False

    def jump(self):
        if self.is_grounded:
            self.velocity = self.jump_velocity
            self.is_grounded = False

    def draw(self, surface, color=(255, 0, 255)):
        pygame.draw.rect(surface, color, self.rect)
