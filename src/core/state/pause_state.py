import pygame
from .state import State


class PauseState(State):
    def __init__(self, game, play_state):
        super().__init__(game)
        self.play_state = play_state  # Keep for resuming the game
        self.font_large = pygame.font.SysFont("Arial", 50)
        self.font_medium = pygame.font.SysFont("Arial", 30)
        self.selected_option = 0  # 0: Resume, 1: Restart, 2: Quit to Menu
        self.options = ["Resume (P)", "Restart (R)", "Quit to Menu (Q)"]
        self.pause_start = pygame.time.get_ticks()  # Record when the pause started

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Resume the game
                    self._resume_game()
                elif event.key == pygame.K_r:  # Restart the game
                    from .play_state import PlayState

                    self.game.set_state(PlayState(self.game))
                elif event.key == pygame.K_q:  # Quit to menu
                    from .menu_state import MenuState

                    self.game.set_state(MenuState(self.game))
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(
                        self.options
                    )
                elif event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(
                        self.options
                    )
                elif event.key == pygame.K_RETURN:
                    self.handle_menu_selection()

    def handle_menu_selection(self):
        if self.selected_option == 0:
            self._resume_game()
        elif self.selected_option == 1:
            from .play_state import PlayState

            self.game.set_state(PlayState(self.game))
        elif self.selected_option == 2:
            from .menu_state import MenuState

            self.game.set_state(MenuState(self.game))

    def _resume_game(self):
        pause_duration = pygame.time.get_ticks() - self.pause_start

        self.play_state.obstacle_manager.pause_accumulated_time += pause_duration

        from .play_state import PlayState

        self.game.set_state(PlayState(self.game, self.play_state))

    def update(self):
        pass

    def render(self):
        self.game.screen.fill((255, 255, 0))

        title = self.font_large.render("PAUSED", True, (0, 0, 0))
        self.game.screen.blit(
            title,
            (self.game.width // 2 - title.get_width() // 2, self.game.height // 4),
        )

        for i, option in enumerate(self.options):
            color = (255, 0, 0) if i == self.selected_option else (0, 0, 0)
            text = self.font_medium.render(option, True, color)
            self.game.screen.blit(
                text,
                (
                    self.game.width // 2 - text.get_width() // 2,
                    self.game.height // 2 + i * 40,
                ),
            )

        instructions = self.font_medium.render(
            "Use ARROW KEYS and ENTER to select", True, (0, 0, 0)
        )
        self.game.screen.blit(
            instructions,
            (
                self.game.width // 2 - instructions.get_width() // 2,
                self.game.height - 100,
            ),
        )

        pygame.display.flip()
