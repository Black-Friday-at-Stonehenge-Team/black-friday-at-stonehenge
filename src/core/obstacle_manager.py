import pygame
from .obstacle import Obstacle
from numpy import random
from core.logs import get_logger

logger = get_logger("ObstacleManager")


class ObstacleManager:
    def __init__(self, screen_width, ground_level):
        self.screen_width = screen_width
        self.ground_level = ground_level
        self.obstacles = []
        self.last_obstacle_time = 0
        self.next_obstacle_interval = self._get_gaussian_interval()

        self.spawn_y = ground_level
        logger.debug(
            f"ObstacleManager initialized with screen_width={screen_width}, ground_level={ground_level}"
        )

    def _get_gaussian_interval(self):
        """Returns a random interval using Gaussian distribution"""
        mean = 2500  # Mean time between obstacles (ms)
        std_dev = 400  # Standard deviation (ms)
        interval = random.normal(mean, std_dev)
        return max(2000, min(interval, 3000))

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_obstacle_time > self.next_obstacle_interval:
            new_obstacle = Obstacle(self.screen_width, self.spawn_y)
            new_obstacle.rect.bottom = self.ground_level
            self.obstacles.append(new_obstacle)
            self.last_obstacle_time = current_time
            self.next_obstacle_interval = self._get_gaussian_interval()

        for obstacle in self.obstacles[:]:
            obstacle.update()
            if not obstacle.active:
                self.obstacles.remove(obstacle)
                return 1
        return 0

    def check_collisions(self, player_rect):
        collision = any(
            obstacle.rect.colliderect(player_rect) for obstacle in self.obstacles
        )
        if collision:
            logger.info("Player collision detected")
        return collision

    def draw(self, surface):
        for obstacle in self.obstacles:
            obstacle.draw(surface)

    def reset(self):
        self.obstacles = []
        self.last_obstacle_time = pygame.time.get_ticks()
        self.next_obstacle_interval = self._get_gaussian_interval()
        logger.info("ObstacleManager reset")
        logger.debug(
            f"ObstacleManager reset: last_obstacle_time={self.last_obstacle_time}, next_obstacle_interval={self.next_obstacle_interval}"
        )
        logger.debug(f"Obstacles cleared: {self.obstacles}")
