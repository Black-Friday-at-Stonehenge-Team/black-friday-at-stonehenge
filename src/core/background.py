from pathlib import Path
from typing import Tuple, Union

import pygame


class Background:
    def __init__(self, color: Union[str | Tuple] = "white", image: str = None):
        self.color = color
        self.image = image

    def set_color(self, color: str):
        self.color = color

    def set_image(self, image: str):
        self.image = image

    def get_color(self) -> str:
        return self.color

    def get_image(self) -> str:
        return self.image

    def render(self, screen: pygame.Surface):
        if self.image:
            background = pygame.image.load(
                Path().parent / "assets" / "backgrounds" / self.image
            )
            screen.blit(
                pygame.transform.scale(
                    background, (screen.get_width(), screen.get_height())
                ),
                (0, 0),
            )
        else:
            screen.fill(pygame.Color(self.color))
