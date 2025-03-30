import pygame

from core.state import MenuState, PlayState, PauseState, GameOverState

FPS = 120


class Game:
    def __init__(self, width: int = 1280, height: int = 720, title: str = "Game"):
        self.width = width
        self.height = height
        self.title = title
        self.high_score = 0
        # Initialize pygame
        pygame.init()

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

        self.clock = pygame.time.Clock()

        self.running = True

        self.state = MenuState(self)

    def set_state(self, new_state):
        """Switch to a new state."""
        self.state = new_state

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.state.update()
            self.state.render()

            self.clock.tick(FPS)

    def handle_events(self):
        """Delegate event handling to the current state."""
        self.state.handle_events()
