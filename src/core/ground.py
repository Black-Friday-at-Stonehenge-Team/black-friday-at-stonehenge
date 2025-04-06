import pygame
from pathlib import Path
from core.logs import get_logger

logger = get_logger("Ground")


class Ground:
    def __init__(
        self, screen_width, screen_height, ground_level, image="ground_tile.png"
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.ground_level = ground_level

        # Load the tileable ground image
        self.image_path = (
            Path(__file__).parent.parent.parent / "assets" / "ground" / image
        )
        try:
            self.ground_image = pygame.image.load(self.image_path).convert_alpha()
        except FileNotFoundError:
            logger.error(f"Ground image '{image}' not found. Using fallback color.")
            self.ground_image = pygame.Surface((100, 50))  # Fallback size
            self.ground_image.fill((139, 69, 19))  # Brown color

        # Scale the ground image if necessary
        self.ground_image = pygame.transform.scale(
            self.ground_image,
            (self.ground_image.get_width(), self.ground_image.get_height()),
        )

        self.tile_width = self.ground_image.get_width()

    def render(self, surface, offset_x=0):
        # Draw the ground image repeatedly across the screen width
        for x in range(-self.tile_width, self.screen_width, self.tile_width):
            surface.blit(self.ground_image, (x + offset_x, self.ground_level))
