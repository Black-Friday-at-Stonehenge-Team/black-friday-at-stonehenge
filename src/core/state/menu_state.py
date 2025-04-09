import pygame

from core.background import Background
from core.font import Font
from core.text import Text
from core.state import State
from core.logs import get_logger

logger = get_logger("MenuState")


class MenuState(State):
    def __init__(self, game):
        super().__init__(game)
        logger.info("Menu state initialized")

        # Background
        self.background = Background(image="menu_0.png")

        # Fonts
        self.title_font = Font(
            "antiquity-print.ttf",
            55,
            (0, 0, 0),
            shadow=True,
            shadow_offset=(3, 3),
            shadow_color=(255, 255, 255),
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
        self.selected_option = 0  # 0: Start Game, 1: Options, 2: Quit
        self.options = ["Start Game", "Options", "Quit"]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logger.info("Quit event received")
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
                elif event.key == pygame.K_q and self.selected_option == 1:
                    self.game.running = False

    def handle_menu_selection(self):
        if self.selected_option == 0:  # Start Game
            from .play_state import PlayState

            self.game.set_state(PlayState(self.game))
        elif self.selected_option == 1:  # Options
            from .options_state import OptionsState

            self.game.set_state(OptionsState(self.game, self))
        elif self.selected_option == 2:  # Quit
            self.game.running = False

    def update(self):
        pass

    def render(self):
        # Render the background
        self.background.render(self.game.screen)

        # Render the title
        title_text = Text(
            "Black Friday at Stonehenge",
            self.title_font,
            position=(
                self.game.width // 2
                - self.title_font.render("Black Friday at Stonehenge").get_width() // 2,
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
