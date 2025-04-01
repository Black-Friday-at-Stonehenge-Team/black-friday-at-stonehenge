import pygame
from .state import State


class MenuState(State):
    def __init__(self, game):
        super().__init__(game)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    from .play_state import PlayState

                    self.game.set_state(PlayState(self.game))
                if event.key == pygame.K_q:
                    self.game.running = False

    def update(self):
        pass

    def render(self):
        self.game.screen.fill((0, 0, 0))
        font = pygame.font.SysFont("Arial", 50)
        title_text = font.render("Black Friday at Stonehenge", True, (255, 255, 255))
        message_text = font.render(
            "Press ENTER to start or Q to exit.", True, (255, 255, 255)
        )

        self.game.screen.blit(
            title_text, (self.game.width // 2 - title_text.get_width() // 2, 100)
        )
        self.game.screen.blit(
            message_text, (self.game.width // 2 - message_text.get_width() // 2, 200)
        )
        pygame.display.flip()
