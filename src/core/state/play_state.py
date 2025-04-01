import pygame

from core.logs import get_logger
from core.player import Player
from core.obstacle_manager import ObstacleManager
from core.ground import Ground
from .state import State

logger = get_logger("PlayState")


class PlayState(State):
    def __init__(self, game, previous_state=None):
        super().__init__(game)

        # Initialize player
        if previous_state and hasattr(previous_state, "player"):
            self.player = previous_state.player
        else:
            self.player = Player(100, self.game.height - 100)

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
        self.font = pygame.font.SysFont("Arial", 30)

        # Initialize ground object
        self.ground = Ground(
            screen_width=self.game.width,
            screen_height=self.game.height,
            ground_level=self.ground_level,
        )

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
            from .game_over_state import GameOverState

            self.game.set_state(GameOverState(self.game))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    from .pause_state import PauseState

                    self.game.set_state(PauseState(self.game, self))
                elif event.key == pygame.K_SPACE:
                    self.player.jump()

    def render(self):
        # Draw background
        self.game.screen.fill((91, 110, 225))

        # Render the ground
        self.ground.render(self.game.screen)

        # Draw game elements
        self.player.draw(self.game.screen)
        self.obstacle_manager.draw(self.game.screen)

        # Draw UI elements
        score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.game.screen.blit(score_text, (20, 20))
        high_score = self.game.high_score
        if high_score > 0:
            high_score_text = self.font.render(
                f"High Score: {high_score}", True, (0, 0, 0)
            )
            self.game.screen.blit(high_score_text, (20, 60))
        pause_text = self.font.render("Press P to pause", True, (255, 255, 255))
        self.game.screen.blit(
            pause_text, (self.game.width - pause_text.get_width() - 20, 20)
        )

        pygame.display.flip()
