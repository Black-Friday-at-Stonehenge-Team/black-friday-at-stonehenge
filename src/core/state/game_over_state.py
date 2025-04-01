import pygame
from .state import State


class GameOverState(State):
    def __init__(self, game):
        super().__init__(game)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    from .play_state import PlayState

                    self.game.set_state(PlayState(self.game))
                elif event.key == pygame.K_q:
                    from .menu_state import MenuState

                    self.game.set_state(MenuState(self.game))

    def update(self):
        pass

    def render(self):
        self.game.screen.fill((255, 0, 0))
        lg_font = pygame.font.SysFont("Arial", 50)
        game_over_text = lg_font.render("GAME OVER", True, (255, 255, 255))
        self.game.screen.blit(
            game_over_text,
            (
                self.game.width // 2 - game_over_text.get_width() // 2,
                self.game.height // 2,
            ),
        )

        sm_font = pygame.font.SysFont("Arial", 24)
        game_over_text = sm_font.render(
            "Press R to restart or Q to go to the main menu.", True, (255, 255, 255)
        )
        self.game.screen.blit(
            game_over_text,
            (
                self.game.width // 2 - game_over_text.get_width() // 2,
                self.game.height // 2 + 100,
            ),
        )

        pygame.display.flip()
