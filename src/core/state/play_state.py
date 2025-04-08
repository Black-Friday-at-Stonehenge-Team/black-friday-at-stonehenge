import pygame

from core.logs import get_logger
from core.player import Player
from core.obstacle_manager import ObstacleManager
from core.ground import Ground
from core.sound_controller import SoundController
from core.state import State
from core.state import GameOverState
from core.font import Font
from core.text import Text
from core.tiling_background import TilingBackground

logger = get_logger("PlayState")


class PlayState(State):
    def __init__(self, game, previous_state=None):
        super().__init__(game)

        # Initialize player
        if previous_state and hasattr(previous_state, "player"):
            self.player = previous_state.player
        else:
            self.player = Player(100, self.game.height - 100)

        sound_config = {
            "window_size": 150,
            "z_threshold": 3.0,
            "holdoff_time": 0.2,
            "sensitivity": 0.50,
            "port": self.game.sound_port,
            "baudrate": self.game.sound_baudrate,
            "noise_floor": 100,
        }

        # Get Singleton instance of sound controller
        try:
            self.sound_controller = SoundController.get_instance(
                sound_config, self.player.jump
            )
            logger.info("Sound controller initialized or reused")
        except Exception as e:
            logger.error(f"Failed to initialize sound controller: {str(e)}")
            self.sound_controller = None

        # Initialize obstacle manager
        if previous_state and hasattr(previous_state, "obstacle_manager"):
            self.obstacle_manager = previous_state.obstacle_manager
        else:
            self.obstacle_manager = ObstacleManager(
                self.game.width, self.game.height - 100
            )

        # Game state
        self.score = previous_state.score if previous_state else 0
        self.ground_level = self.game.height - 100

        bg_scale = 16
        # Initialize the tiling background
        self.background = TilingBackground(
            image="background_bricks.png", unit_size=(50 * bg_scale, 33 * bg_scale)
        )

        # Fonts
        self.score_font = Font(
            "antiquity-print.ttf",
            39,
            (255, 255, 255),
            shadow=True,
            shadow_offset=(2, 2),
        )
        self.pause_font = Font(
            "antiquity-print.ttf",
            26,
            (255, 255, 255),
            shadow=True,
            shadow_offset=(3, 3),
        )

        # Initialize ground object
        self.ground = Ground(
            screen_width=self.game.width,
            screen_height=self.game.height,
            ground_level=self.ground_level,
            image="ground_tile.png",
        )

        # Scrolling attributes
        self.scroll_speed = 5
        self.background_offset = 0
        self.ground_offset = 0

    def update(self):
        self.player.update(self.ground_level)
        self.obstacle_manager.update()

        passed_obstacles = self.obstacle_manager.get_passed_obstacles(
            self.player.rect.left
        )
        self.score += passed_obstacles

        # Check for collisions
        if self.obstacle_manager.check_collisions(self.player.rect):
            self.game.high_score = max(self.game.high_score, self.score)

            self.game.set_state(GameOverState(self.game))

        # Update scrolling offsets
        self.background_offset = (self.background_offset - self.scroll_speed) % (
            self.background.unit_size[0]
        )
        self.ground_offset = (self.ground_offset - 2 * self.scroll_speed) % (
            self.ground.tile_width
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    from .pause_state import PauseState

                    self.game.set_state(PauseState(self.game, self))
                elif event.key == pygame.K_ESCAPE:
                    from .pause_state import PauseState

                    self.game.set_state(PauseState(self.game, self))
                elif event.key == pygame.K_SPACE:
                    self.player.jump()
            elif event.type == pygame.USEREVENT and event.action == "SOUND_TRIGGER":
                self.player.jump()

    def render(self):
        # Render the scrolling background
        for x in range(
            -self.background.unit_size[0], self.game.width, self.background.unit_size[0]
        ):
            self.background.render(
                self.game.screen, offset_x=x + self.background_offset
            )

        # Render the scrolling ground
        self.ground.render(self.game.screen, offset_x=self.ground_offset)

        # Render the player and obstacles
        self.player.draw(self.game.screen)
        self.obstacle_manager.draw(self.game.screen)

        # Render the score
        score_text = Text(
            f"Score: {self.score:03}",
            self.score_font,
            position=(20, 20),
        )
        score_text.render(self.game.screen)

        # Render the high score
        if self.game.high_score > 0:
            high_score_text = Text(
                f"High Score: {self.game.high_score:03}",
                self.score_font,
                position=(20, 90),
            )
            high_score_text.render(self.game.screen)

        # Render the pause instructions
        pause_text = Text(
            "Press P or ESC to pause",
            self.pause_font,
            position=(
                self.game.width
                - self.pause_font.render("Press P or ESC to pause").get_width()
                - 30,
                20,
            ),
        )
        pause_text.render(self.game.screen)

        pygame.display.flip()
