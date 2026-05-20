import pygame
import random


class Obstacle:
    def __init__(self, lanes, height):
        self.lanes = lanes
        self.height = height

        self.type = random.choice(["low", "high"])

        # --------------------------------
        # CUSTOM SPAWN POSITIONS
        # --------------------------------
        self.spawn_positions = [
            200,   # left lane x position
            590    # right lane x position
        ]

        # choose one of your positions
        self.x = random.choice(self.spawn_positions)

        # start far away
        self.y = 200

        self.base_speed = 220
        self.max_speed = 650

        # load images
        if self.type == "low":
            self.base_image = pygame.image.load(
                "low_obstacle.png"
            ).convert_alpha()

            self.base_size = (80, 80)
            self.hitbox_size = (60, 60)

        else:
            self.base_image = pygame.image.load(
                "high_obstacle.png"
            ).convert_alpha()

            self.base_size = (160, 160)
            self.hitbox_size = (60, 90)

        self.image = self.base_image
        self.rect = self.image.get_rect(
            center=(self.x, self.y)
        )

        self.hitbox = pygame.Rect(
            0, 0, *self.hitbox_size
        )

        self.min_scale = 0.3
        self.max_scale = 3

    def update(self, dt):

        # -----------------------------
        # MOVE FORWARD (TOWARD PLAYER)
        # -----------------------------
        travel_zone = self.height + 200

        # normalize progress (0 = far, 1 = player)
        t = (self.y + 150) / travel_zone
        t = max(0, min(1, t))

        # -----------------------------
        # ACCELERATION (SUBWAY FEEL)
        # -----------------------------
        speed = self.base_speed + (self.max_speed - self.base_speed) * (t * t)

        self.y += speed * dt

        # -----------------------------
        # PERSPECTIVE SCALE
        # -----------------------------
        scale = self.min_scale + (self.max_scale - self.min_scale) * (t * t)

        w = int(self.base_size[0] * scale)
        h = int(self.base_size[1] * scale)

        self.image = pygame.transform.scale(self.base_image, (w, h))
        self.rect = self.image.get_rect(center=(self.x, self.y))

        # -----------------------------
        # HITBOX FOLLOWS SCALE
        # -----------------------------
        self.hitbox.size = (
            int(self.hitbox_size[0] * scale),
            int(self.hitbox_size[1] * scale)
        )

        self.hitbox.centerx = self.rect.centerx
        self.hitbox.bottom = self.rect.bottom

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def is_off_screen(self):
        return self.y > self.height + 200
