import pygame
from core.background import Background
from core.font import Font
from core.text import Text
from .state import State


class PauseState(State):
    def __init__(self, game, play_state):
        super().__init__(game)
        self.play_state = play_state  # Keep for resuming the game
        self.selected_option = 0  # 0: Resume, 1: Restart, 2: Quit to Menu
        self.options = ["Resume", "Restart", "Quit to Menu"]
        self.pause_start = pygame.time.get_ticks()  # Record when the pause started

        # Background
        self.background = Background(image="menu_1.png")

        # Fonts
        self.title_font = Font(
            "antiquity-print.ttf",
            55,
            (255, 255, 255),
            shadow=True,
            shadow_offset=(3, 3),
            shadow_color=(0, 0, 0),
        )
        self.option_font = Font(
            "antiquity-print.ttf",
            30,
            (255, 255, 255),
            shadow=True,
            shadow_offset=(2, 2),
            shadow_color=(0, 0, 0),
        )
        self.instruction_font = Font(
            "antiquity-print.ttf",
            20,
            (255, 255, 255),
            shadow=True,
            shadow_offset=(1, 1),
            shadow_color=(0, 0, 0),
        )

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
        # Render the background
        self.background.render(self.game.screen)

        # Render the title
        title_text = Text(
            "PAUSED",
            self.title_font,
            position=(
                self.game.width // 2
                - self.title_font.render("PAUSED").get_width() // 2,
                self.game.height // 4,
            ),
        )
        title_text.render(self.game.screen)

        # Render the options
        for i, option in enumerate(self.options):
            color = (255, 0, 0) if i == self.selected_option else (255, 255, 255)
            option_font = Font(
                "antiquity-print.ttf",
                30,
                color,
                shadow=True,
                shadow_offset=(2, 2),
                shadow_color=(0, 0, 0),
            )
            option_text = Text(
                option,
                option_font,
                position=(
                    self.game.width // 2 - option_font.render(option).get_width() // 2,
                    self.game.height // 2 + i * 60,
                ),
            )
            option_text.render(self.game.screen)

        # Render the instructions
        instructions_text = Text(
            "Use ARROW KEYS and ENTER to select",
            self.instruction_font,
            position=(
                self.game.width // 2
                - self.instruction_font.render(
                    "Use ARROW KEYS and ENTER to select"
                ).get_width()
                // 2,
                self.game.height - 100,
            ),
        )
        instructions_text.render(self.game.screen)

        pygame.display.flip()
