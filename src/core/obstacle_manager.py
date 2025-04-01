import pygame
from .obstacle import Obstacle
from numpy import random


class ObstacleManager:
    def __init__(self, screen_width, ground_level):
        self.screen_width = screen_width
        self.ground_level = ground_level
        self.obstacles = []
        self.last_obstacle_time = 0
        self.next_obstacle_interval = self._get_gaussian_interval()
        self.spawn_y = ground_level - 30

    def _get_gaussian_interval(self):
        """Returns a random interval using Gaussian distribution"""
        mean = 2500  # Mean time between obstacles (ms)
        std_dev = 400  # Standard deviation (ms)
        interval = random.normal(mean, std_dev)
        return max(2000, min(interval, 3000))

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_obstacle_time > self.next_obstacle_interval:
            self.obstacles.append(Obstacle(self.screen_width, self.spawn_y))
            self.last_obstacle_time = current_time
            self.next_obstacle_interval = self._get_gaussian_interval()

        for obstacle in self.obstacles[:]:
            obstacle.update()
            if not obstacle.active:
                self.obstacles.remove(obstacle)
                yield True  # Signal that we passed an obstacle
            else:
                yield False

    def check_collisions(self, player_rect):
        return any(
            obstacle.rect.colliderect(player_rect) for obstacle in self.obstacles
        )

    def draw(self, surface):
        for obstacle in self.obstacles:
            obstacle.draw(surface)

    def reset(self):
        self.obstacles = []
        self.last_obstacle_time = pygame.time.get_ticks()
        self.next_obstacle_interval = self._get_gaussian_interval()
