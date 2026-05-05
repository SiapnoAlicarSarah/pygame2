import pygame

class Background:
    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height

        self.frames = [
            pygame.image.load("bg1.png").convert(),
            pygame.image.load("bg2.png").convert(),
            pygame.image.load("bg3.png").convert()
        ]

        self.frames = [
            pygame.transform.scale(img, (self.WIDTH, self.HEIGHT))
            for img in self.frames
        ]

        self.current_frame = 0
        self.frame_timer = 0
        self.frame_delay = 0.2 

    def update(self):
        self.frame_timer += 1

        if self.frame_timer >= 10:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.frame_timer = 0

    def draw(self, screen):
        screen.blit(self.frames[self.current_frame], (0, 0))
