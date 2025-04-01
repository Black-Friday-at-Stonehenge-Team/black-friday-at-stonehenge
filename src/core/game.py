import pygame
from core.state import MenuState
from core.logs import get_logger

logger = get_logger("Game")

FPS = 120


class Game:
    def __init__(self, width: int = 1280, height: int = 720, title: str = "Game"):
        self.width = width
        self.height = height
        self.title = title
        self.high_score = 0
        # Initialize pygame
        pygame.init()

        logger.info(f"Initializing game: {title} ({width}x{height})")

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

        self.clock = pygame.time.Clock()

        self.running = True

        self.state = MenuState(self)
        logger.info("Game initialized")

    def set_state(self, new_state):
        """Switch to a new state."""
        logger.debug(f"Switching state to {new_state.__class__.__name__}")
        self.state = new_state

    def run(self):
        """Main game loop."""
        logger.info("Starting game loop")
        while self.running:
            self.handle_events()
            self.state.update()
            self.state.render()

            self.clock.tick(FPS)
        logger.info("Game loop ended")

    def handle_events(self):
        """Delegate event handling to the current state."""
        self.state.handle_events()
