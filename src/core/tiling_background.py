from pathlib import Path
import pygame


class TilingBackground:
    def __init__(self, image: str, unit_size: tuple[int, int]):
        self.image_path = (
            Path(__file__).parent.parent.parent / "assets" / "backgrounds" / image
        )
        self.unit_size = unit_size
        self.tile_image = pygame.image.load(self.image_path).convert_alpha()
        self.tile_image = pygame.transform.scale(self.tile_image, self.unit_size)

    def render(self, screen: pygame.Surface, offset_x=0):
        screen_width, screen_height = screen.get_size()

        # Loop through the screen dimensions and draw tiles with offset
        for x in range(-self.unit_size[0], screen_width, self.unit_size[0]):
            for y in range(0, screen_height, self.unit_size[1]):
                screen.blit(self.tile_image, (x + offset_x, y))
