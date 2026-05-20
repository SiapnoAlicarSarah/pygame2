import pygame


class Character:
    def __init__(self, lanes, height, char_type=0):
        self.lanes = lanes
        self.height = height
        self.char_type = char_type  # 🔥 WHICH CHARACTER

        self.lane = 0
        self.y = height - 200
        self.x = self.lanes.get_lane_x(self.lane)

        self.move_cd = 0
        self.jump_cd = 0

        self.move_delay = 0.15
        self.jump_delay = 0.25

        self.state = "idle"
        self.velocity_y = 0
        self.gravity = 1
        self.is_jumping = False

        self.lane_speed = 10

        # 🔥 LOAD 3 FRAMES FOR SELECTED CHARACTER
        self.frames = []
        for i in range(3):
            img = pygame.image.load(
                f"char{char_type+1}_frame{i+1}.png"
            ).convert_alpha()

            img = pygame.transform.scale(img, (100, 150))
            self.frames.append(img)

        # 🔥 LOAD UNIQUE CROUCH/JUMP PER CHARACTER
        self.crouch_img = pygame.transform.scale(
            pygame.image.load(f"char{char_type+1}_crouch.png").convert_alpha(),
            (100, 100),
        )

        self.jump_img = pygame.transform.scale(
            pygame.image.load(f"char{char_type+1}_jump.png").convert_alpha(),
            (100, 100),
        )

        # rect
        self.rect = self.frames[0].get_rect(center=(self.x, self.y))

        # hitbox (stable)
        self.hitbox = pygame.Rect(0, 0, 30, 45)

        self.frame_index = 0
        self.animation_speed = 10
        self.animation_timer = 0

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT and self.move_cd == 0:
                if self.lane == 1:
                    self.lane = 0
                    self.move_cd = self.move_delay

            if event.key == pygame.K_RIGHT and self.move_cd == 0:
                if self.lane == 0:
                    self.lane = 1
                    self.move_cd = self.move_delay

            if event.key == pygame.K_UP and not self.is_jumping and self.jump_cd == 0:
                self.is_jumping = True
                self.velocity_y = -20
                self.state = "jump"
                self.jump_cd = self.jump_delay

            if event.key == pygame.K_DOWN and not self.is_jumping:
                self.state = "crouch"

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN and not self.is_jumping:
                self.state = "idle"

    def update(self, dt):
        self.move_cd -= dt
        self.jump_cd -= dt

        if self.move_cd < 0:
            self.move_cd = 0
        if self.jump_cd < 0:
            self.jump_cd = 0

        target_x = self.lanes.get_lane_x(self.lane)

        # smooth lane movement
        self.x += (target_x - self.x) * self.lane_speed * dt

        if abs(self.x - target_x) < 1:
            self.x = target_x

        # jumping physics
        if self.is_jumping:
            self.velocity_y += self.gravity
            self.y += self.velocity_y

            if self.y >= self.height - 200:
                self.y = self.height - 200
                self.is_jumping = False
                self.state = "idle"

            if self.is_jumping:
                self.state = "jump"
        elif self.state != "crouch":
            self.state = "idle"

        # 🔥 ANIMATION (only when running)
        if self.state == "idle":
            self.animation_timer += dt
            if self.animation_timer >= 1 / self.animation_speed:
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.animation_timer = 0

        self.rect.center = (self.x, self.y)

        # hitbox (stable)
        if self.state == "crouch":
            self.hitbox.size = (30, 30)
        else:
            self.hitbox.size = (30, 45)

        self.hitbox.midbottom = self.rect.midbottom

    def draw(self, screen):
        if self.state == "jump":
            current_frame = self.jump_img
        elif self.state == "crouch":
            current_frame = self.crouch_img
        else:
            current_frame = self.frames[self.frame_index]

        self.rect.center = (self.x, self.y)
        screen.blit(current_frame, self.rect)
