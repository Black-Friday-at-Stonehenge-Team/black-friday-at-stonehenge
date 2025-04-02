import pygame


class BaseObstacle:
    def __init__(self, x, y, texture):
        self.x = x
        self.y = y
        self.texture = texture
        self.rect = pygame.Rect(x, y, texture.get_width(), texture.get_height())

    def update(self):
        self.x -= 10
        self.rect.x = self.x

    def draw(self, surface):
        if self.texture:
            surface.blit(self.texture, (self.x, self.y))


class SmallObstacle(BaseObstacle):
    pass


class TallObstacle(BaseObstacle):
    pass


class WideObstacle(BaseObstacle):
    pass
