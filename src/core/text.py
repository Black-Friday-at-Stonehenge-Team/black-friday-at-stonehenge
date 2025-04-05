from typing import Tuple

import pygame

from core.font import Font


class Text:
    def __init__(self, text: str, font: Font, position: Tuple):
        self.text = text
        self.position = position
        self.font = font
        self._length = len(text)

    def __str__(self):
        return self.text

    def __len__(self):
        return self._length

    def render(self, screen: pygame.Surface):
        self.text_surface = self.font.render(self.text)
        screen.blit(self.text_surface, (self.position[0], self.position[1]))
