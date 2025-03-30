import random
import pygame

from .state import State


class PlayState(State):
    def __init__(self, game, previous_state=None):
        super().__init__(game)

        if previous_state:
            self.dino_rect = previous_state.dino_rect.copy()
            self.dino_velocity = previous_state.dino_velocity
            self.obstacles = [obstacle.copy() for obstacle in previous_state.obstacles]
            self.score = previous_state.score
            self.last_obstacle_time = previous_state.last_obstacle_time
            self.next_obstacle_interval = previous_state.next_obstacle_interval
        else:
            self.dino_rect = pygame.Rect(100, self.game.height - 100, 50, 80)
            self.dino_velocity = 0
            self.obstacles = []
            self.score = 0
            self.last_obstacle_time = 0

            self.next_obstacle_interval = self._get_gaussian_interval()

        self.gravity = 0.5
        self.ground_level = self.game.height - 100
        self.font = pygame.font.SysFont("Arial", 30)

    def _get_gaussian_interval(self):
        """Returns a random interval using Gaussian distribution"""
        mean = 1500  # Mean time between obstacles (ms)
        std_dev = 400  # Standard deviation (ms)

        interval = random.gauss(mean, std_dev)

        interval = max(800, min(interval, 2500))

        return int(interval)

    def update(self):
        self.dino_velocity += self.gravity
        self.dino_rect.y += self.dino_velocity

        if self.dino_rect.bottom > self.ground_level:
            self.dino_rect.bottom = self.ground_level
            self.dino_velocity = 0

        current_time = pygame.time.get_ticks()
        if current_time - self.last_obstacle_time > self.next_obstacle_interval:
            self.obstacles.append(
                pygame.Rect(self.game.width, self.ground_level - 30, 30, 30)
            )
            self.last_obstacle_time = current_time
            self.next_obstacle_interval = self._get_gaussian_interval()

        for obstacle in self.obstacles[:]:
            obstacle.x -= 5
            if obstacle.right < 0:
                self.obstacles.remove(obstacle)
                self.score += 1

            if obstacle.colliderect(self.dino_rect):
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

                    # Pass the current game state to the pause state
                    self.game.set_state(PauseState(self.game, self))
                elif (
                    event.key == pygame.K_SPACE
                    and self.dino_rect.bottom >= self.ground_level
                ):
                    self.dino_velocity = -15

    def render(self):
        self.game.screen.fill((255, 255, 255))

        pygame.draw.line(
            self.game.screen,
            (0, 0, 0),
            (0, self.ground_level),
            (self.game.width, self.ground_level),
            2,
        )

        pygame.draw.rect(self.game.screen, (255, 0, 255), self.dino_rect)

        for obstacle in self.obstacles:
            pygame.draw.rect(self.game.screen, (255, 0, 0), obstacle)

        score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.game.screen.blit(score_text, (20, 20))

        high_score = self.game.high_score
        if high_score > 0:
            high_score_text = self.font.render(
                f"High Score: {high_score}", True, (0, 0, 0)
            )
            self.game.screen.blit(high_score_text, (20, 60))

        pause_text = self.font.render("Press P to pause", True, (100, 100, 100))
        self.game.screen.blit(
            pause_text, (self.game.width - pause_text.get_width() - 20, 20)
        )

        pygame.display.flip()
