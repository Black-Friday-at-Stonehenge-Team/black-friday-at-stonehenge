import pygame

from core.background import Background
from core.font import Font
from core.text import Text
from .state import State


class GameOverState(State):
    def __init__(self, game):
        super().__init__(game)

        # Background
        self.background = Background(image="menu_2.png")

        # Fonts
        self.title_font = Font(
            "antiquity-print.ttf",
            55,
            (255, 255, 255),
            shadow=True,
            shadow_offset=(4, 4),
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

        # Menu options
        self.selected_option = 0  # 0: Restart, 1: Quit to Menu
        self.options = ["Restart", "Quit to Menu"]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(
                        self.options
                    )
                elif event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(
                        self.options
                    )
                elif event.key == pygame.K_RETURN:
                    self.handle_menu_selection()
                elif event.key == pygame.K_r and self.selected_option == 0:
                    self.restart_game()
                elif event.key == pygame.K_q and self.selected_option == 1:
                    self.quit_to_menu()

    def handle_menu_selection(self):
        if self.selected_option == 0:  # Restart
            self.restart_game()
        elif self.selected_option == 1:  # Quit to Menu
            self.quit_to_menu()

    def restart_game(self):
        from .play_state import PlayState

        self.game.set_state(PlayState(self.game))

    def quit_to_menu(self):
        from .menu_state import MenuState

        self.game.set_state(MenuState(self.game))

    def update(self):
        pass

    def render(self):
        # Render the background
        self.background.render(self.game.screen)

        # Render the title
        title_text = Text(
            "GAME OVER",
            self.title_font,
            position=(
                self.game.width // 2
                - self.title_font.render("GAME OVER").get_width() // 2,
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
