import os
import pygame
from .obstacle import SmallObstacle, TallObstacle, WideObstacle
import random
from core.logs import get_logger

logger = get_logger("ObstacleManager")


class ObstacleManager:
    def __init__(self, screen_width, ground_level):
        self.screen_width = screen_width
        self.ground_level = ground_level
        self.obstacles = []
        self.last_obstacle_time = 0
        self.next_obstacle_interval = random.randint(600, 1500)
        self.spawn_y = ground_level
        self.paused = False
        self.pause_start_time = 0
        self.pause_accumulated_time = 0

        # Load obstacle textures
        self.textures = self._load_obstacle_textures()

        logger.debug(
            f"ObstacleManager initialized with screen_width={screen_width}, ground_level={ground_level}"
        )

    def _load_obstacle_textures(self):
        base_path = "assets/obstacle"
        textures = {"small": [], "tall": [], "wide": []}
        scale_factor = 2

        try:
            for obstacle_type in textures.keys():
                dir_path = os.path.join(base_path, obstacle_type)
                if os.path.exists(dir_path):
                    for file_name in os.listdir(dir_path):
                        if file_name.endswith(".png"):
                            texture_path = os.path.join(dir_path, file_name)
                            texture = pygame.image.load(texture_path).convert_alpha()

                            # Texture scaling
                            original_size = texture.get_size()
                            scaled_size = (
                                original_size[0] * scale_factor,
                                original_size[1] * scale_factor,
                            )
                            scaled_texture = pygame.transform.scale(
                                texture, scaled_size
                            )

                            textures[obstacle_type].append(scaled_texture)

                if not textures[obstacle_type]:
                    logger.warning(
                        f"No textures found for obstacle type '{obstacle_type}'. Using fallback rendering."
                    )
                    fallback_color = (
                        (255, 0, 0)
                        if obstacle_type == "small"
                        else (0, 255, 0)
                        if obstacle_type == "tall"
                        else (0, 0, 255)
                    )
                    fallback_size = (
                        30 * scale_factor
                        if obstacle_type != "wide"
                        else 60 * scale_factor,
                        30 * scale_factor
                        if obstacle_type == "small"
                        else 60 * scale_factor
                        if obstacle_type == "tall"
                        else 30 * scale_factor,
                    )
                    fallback_texture = pygame.Surface(fallback_size, pygame.SRCALPHA)
                    fallback_texture.fill(fallback_color)
                    textures[obstacle_type].append(fallback_texture)

            logger.info("Obstacle textures loaded successfully")
        except Exception as e:
            logger.error(f"Error loading obstacle textures: {e}")

        return textures

    def _spawn_obstacle(self):
        obstacle_classes = [
            (SmallObstacle, self.textures["small"]),
            (TallObstacle, self.textures["tall"]),
            (WideObstacle, self.textures["wide"]),
        ]
        obstacle_class, texture_list = random.choice(obstacle_classes)
        texture = random.choice(texture_list) if texture_list else None

        texture_width = texture.get_width() if texture else 0
        texture_height = texture.get_height() if texture else 0
        y_position = self.ground_level - texture_height

        obstacle = obstacle_class(
            x=self.screen_width,
            y=y_position,
            texture=texture,
        )
        obstacle.rect = pygame.Rect(
            obstacle.x, obstacle.y, texture_width, texture_height
        )

        return obstacle

    def update(self):
        if self.paused:
            return

        current_time = pygame.time.get_ticks()
        elapsed_time = (
            current_time - self.last_obstacle_time - self.pause_accumulated_time
        )

        if elapsed_time > self.next_obstacle_interval:
            new_obstacle = self._spawn_obstacle()
            self.obstacles.append(new_obstacle)
            self.last_obstacle_time = current_time
            self.pause_accumulated_time = 0
            self.next_obstacle_interval = random.randint(600, 1500)

        for obstacle in self.obstacles[:]:
            obstacle.update()
            if obstacle.rect.right < 0:
                self.obstacles.remove(obstacle)
                logger.debug("Removed obstacle that is out of view")

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

            # DEBUG: Obstacle hitbox
            if hasattr(obstacle, "rect"):
                pygame.draw.rect(surface, (0, 0, 0), obstacle.rect, 1)  # 1-pixel border

    def reset(self):
        self.obstacles = []
        self.last_obstacle_time = pygame.time.get_ticks()
        self.next_obstacle_interval = random.randint(600, 1500)
        self.pause_accumulated_time = 0
        logger.info("ObstacleManager reset")
        logger.debug(
            f"ObstacleManager reset: last_obstacle_time={self.last_obstacle_time}, next_obstacle_interval={self.next_obstacle_interval}"
        )
        logger.debug(f"Obstacles cleared: {self.obstacles}")

    def pause(self):
        if not self.paused:
            self.paused = True
            self.pause_start_time = pygame.time.get_ticks()
            logger.debug("ObstacleManager paused")

    def resume(self):
        if self.paused:
            self.paused = False
            pause_duration = pygame.time.get_ticks() - self.pause_start_time
            self.pause_accumulated_time += pause_duration
            logger.debug(f"ObstacleManager resumed after {pause_duration} ms")

    def get_passed_obstacles(self, player_x):
        passed_obstacles = [
            obstacle for obstacle in self.obstacles if obstacle.rect.right < player_x
        ]
        for obstacle in passed_obstacles:
            self.obstacles.remove(obstacle)
        return len(passed_obstacles)
