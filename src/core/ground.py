import os
import random
import pygame
from core.logs import get_logger

logger = get_logger("Ground")


class Ground:
    def __init__(
        self,
        screen_width,
        screen_height,
        ground_level,
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.ground_level = ground_level

        self.tile_cell_width, self.tile_cell_height = 32, 32
        self.ground_tile_height = 11
        self.scale = 5

        self.ground_textures = []
        self.ground_surface = None

        self._load_ground_textures("assets/ground/ground.png")
        self._create_ground_surface()

    def _load_ground_textures(self, tileset_path):
        tile_width = self.tile_cell_width
        tile_height = self.ground_tile_height

        if not os.path.exists(tileset_path):
            logger.warning(f"Tileset '{tileset_path}' not found. Using fallback color.")
            fallback = pygame.Surface(
                (tile_width * self.scale, tile_height * self.scale)
            )
            fallback.fill((139, 69, 19))
            self.ground_textures.append(fallback)
            return

        try:
            tileset = pygame.image.load(tileset_path).convert_alpha()
            tileset_width, _ = tileset.get_size()
            columns = tileset_width // tile_width

            for col in range(columns):
                tile_x = col * tile_width
                # Extract the bottom portion (ground_tile_height) of each cell
                tile_y = self.tile_cell_height - tile_height
                tile = pygame.Surface((tile_width, tile_height), pygame.SRCALPHA)
                tile.blit(tileset, (0, 0), (tile_x, tile_y, tile_width, tile_height))

                scaled_tile = pygame.transform.scale(
                    tile, (tile_width * self.scale, tile_height * self.scale)
                )
                self.ground_textures.append(scaled_tile)
            logger.debug(f"Loaded {len(self.ground_textures)} ground textures")
        except Exception as e:
            logger.error(f"Error loading ground textures: {e}")
            fallback = pygame.Surface(
                (tile_width * self.scale, tile_height * self.scale)
            )
            fallback.fill((139, 69, 19))
            self.ground_textures.append(fallback)

    def _create_ground_surface(self):
        if not self.ground_textures:
            self.ground_surface = None
            return

        tile_width = self.ground_textures[0].get_width()
        tile_height = self.ground_textures[0].get_height()
        ground_area_height = self.screen_height - self.ground_level

        self.ground_surface = pygame.Surface(
            (self.screen_width, ground_area_height), pygame.SRCALPHA
        )

        rows = ground_area_height // tile_height + 1
        cols = self.screen_width // tile_width + 1

        for row in range(rows):
            for col in range(cols):
                tile = random.choice(self.ground_textures)
                x = col * tile_width
                y = row * tile_height
                self.ground_surface.blit(tile, (x, y))

    def render(self, surface):
        if self.ground_surface:
            # Use the cached ground surface
            surface.blit(self.ground_surface, (0, self.ground_level))
        else:
            # Fallback ground tile
            pygame.draw.rect(
                surface,
                (139, 69, 19),
                (
                    0,
                    self.ground_level,
                    self.screen_width,
                    self.screen_height - self.ground_level,
                ),
            )
