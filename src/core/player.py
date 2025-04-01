import pygame
import os

from core.logs import get_logger

logger = get_logger("Player")


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.gravity = 1
        self.jump_velocity = -22.5
        self.is_grounded = True

        # Animation properties
        self.sprite_sheet = None
        self.frames = []
        self.current_frame = 0
        self.animation_speed = 0.2
        self.animation_timer = 0

        # Player scale
        self.scale = 5

        # Offset to sprite positioning
        self.sprite_offset_x = 0
        self.sprite_offset_y = 0

        # Fallback player sprite
        self.rect = pygame.Rect(x, y, 50, 80)

        # Attempt to load sprite sheet
        sprite_path = "assets/player/player.png"
        if os.path.exists(sprite_path):
            self.load_sprite_sheet(sprite_path, 32, 32)
        else:
            logger.warning(
                f"Sprite sheet '{sprite_path}' not found. Using rectangle as fallback."
            )

    def load_sprite_sheet(self, filename, frame_width, frame_height):
        try:
            # Load sprite sheet
            self.sprite_sheet = pygame.image.load(filename).convert_alpha()

            sheet_width, sheet_height = self.sprite_sheet.get_size()
            cols = sheet_width // frame_width
            rows = sheet_height // frame_height

            # Extract each frame from the sprite sheet
            for row in range(rows):
                for col in range(cols):
                    frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)

                    frame.blit(
                        self.sprite_sheet,
                        (0, 0),
                        (
                            col * frame_width,
                            row * frame_height,
                            frame_width,
                            frame_height,
                        ),
                    )

                    # Scale the tile
                    scaled_frame = pygame.transform.scale(
                        frame, (frame_width * self.scale, frame_height * self.scale)
                    )

                    self.frames.append(scaled_frame)

            if self.frames:
                self.calculate_hitbox(self.frames[0])

            logger.debug(f"Loaded {len(self.frames)} frames from sprite sheet")

        except Exception as e:
            logger.error(f"Error loading sprite sheet: {e}")

    def calculate_hitbox(self, frame):
        "Find the bounding box by using the non-transparent pixels from the sprite sheet"
        mask = pygame.mask.from_surface(frame)
        if mask.count() > 0:
            # Get all non-transparent areas
            bounds_list = mask.get_bounding_rects()

            # If there are multiple non-transparent regions, combine them
            if bounds_list:
                # Get the overall bounding rectangle that contains all non-transparent regions
                min_x = min(rect.left for rect in bounds_list)
                min_y = min(rect.top for rect in bounds_list)
                max_x = max(rect.right for rect in bounds_list)
                max_y = max(rect.bottom for rect in bounds_list)

                # Calculate offsets between sprite and hitbox
                self.sprite_offset_x = min_x
                self.sprite_offset_y = min_y

                # Create a hitbox with the calculated dimensions
                width = max_x - min_x
                height = max_y - min_y

                # Place the hitbox properly (centered horizontally, bottom aligned)
                self.rect = pygame.Rect(self.x, self.y, width, height)
        else:
            # Fallback to a reasonable size if no non-transparent pixels found
            frame_width, frame_height = frame.get_size()
            self.rect = pygame.Rect(
                self.x,
                self.y,
                frame_width // 2,
                frame_height // 2,
            )

    def update(self, ground_level):
        self.velocity += self.gravity
        self.rect.y += self.velocity

        if self.rect.bottom > ground_level:
            self.rect.bottom = ground_level
            self.velocity = 0
            self.is_grounded = True
        else:
            self.is_grounded = False

        # Update animation when player is on ground
        if self.is_grounded and len(self.frames) > 0:
            self.animation_timer += self.animation_speed
            if self.animation_timer >= 1:
                self.animation_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)

    def jump(self):
        if self.is_grounded:
            self.velocity = self.jump_velocity
            self.is_grounded = False

    def draw(self, surface, color=(255, 0, 255)):
        # Draw the current animation frame
        if len(self.frames) > 0:
            current_img = self.frames[self.current_frame]

            # Calculate sprite position
            sprite_x = self.rect.x - self.sprite_offset_x
            sprite_y = self.rect.y - self.sprite_offset_y

            surface.blit(current_img, (sprite_x, sprite_y))

            # Player hitbox
            # pygame.draw.rect(surface, (255, 0, 0), self.rect, 1)
        else:
            # Fallback player sprite
            pygame.draw.rect(surface, color, self.rect)
