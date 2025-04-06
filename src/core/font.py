import pygame
from pathlib import Path


class Font:
    def __init__(
        self,
        font_name: str,
        size: int,
        color: tuple[int, int, int],
        antialiased: bool = False,
        shadow: bool = False,
        shadow_offset: tuple[int, int] = (2, 2),
        shadow_color: tuple[int, int, int] = (0, 0, 0),
    ):
        # Font properties
        self.font_name = font_name
        self.size = size

        # Drop Shadow properties
        self.shadow = shadow
        self.shadow_offset = shadow_offset
        self.shadow_color = shadow_color

        # Load the font
        self.font = pygame.font.Font(
            Path(__file__).parent.parent.parent / f"assets/fonts/{font_name}", size
        )

        self.color = color
        self.antialiased = antialiased

    def render(self, text: str) -> pygame.Surface:
        # Render the drop shadow if enabled
        if self.shadow:
            shadow_surface = self.font.render(text, self.antialiased, self.shadow_color)
            shadow_width, shadow_height = shadow_surface.get_size()
            surface = pygame.Surface(
                (
                    shadow_width + abs(self.shadow_offset[0]),
                    shadow_height + abs(self.shadow_offset[1]),
                ),
                pygame.SRCALPHA,
            )
            surface.blit(shadow_surface, self.shadow_offset)
        else:
            surface = pygame.Surface((0, 0), pygame.SRCALPHA)

        # Render the main text
        text_surface = self.font.render(text, self.antialiased, self.color)
        surface.blit(text_surface, (0, 0))

        return surface
