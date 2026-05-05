import pygame
import sys

from lanes import Lanes
from character import Character
from background import Background
from obstacles import Obstacle
from gates import Gate

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Run & Resolve!")


class Game:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 800, 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

        self.running = True
        self.meter_paused = False

        # ---------------- STATES ----------------
        self.state = "menu"
        self.selected_character = 0
        self.paused = False
        self.difficulty = "Easy"

        # ---------------- SOUNDS ----------------
        self.tap_sound = pygame.mixer.Sound("tap.ogg")
        self.correct_sound = pygame.mixer.Sound("win.ogg")
        self.wrong_sound = pygame.mixer.Sound("lose.ogg")
        self.hit_sound = pygame.mixer.Sound("obs_lose.ogg")
    
        self.hit_sound.set_volume(0.6)
        self.tap_sound.set_volume(0.5)
        self.correct_sound.set_volume(0.6)
        self.wrong_sound.set_volume(0.6)
        
        # ---------------- BACKGROUND MUSIC ----------------
        self.menu_music = "bg_sound.ogg"
        self.game_music = "bg_sound.ogg"  # you can change this later

        pygame.mixer.music.load(self.menu_music)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)

        # ---------------- SYSTEMS ----------------
        self.background = Background(800, 800)
        self.lanes = Lanes(self.WIDTH, self.HEIGHT)
        self.player = Character(self.lanes, self.HEIGHT, self.selected_character)

        self.font = pygame.font.SysFont(None, 40)
        self.big_font = pygame.font.SysFont(None, 80)

        # ---------------- GAME DATA ----------------
        self.obstacles = []
        self.spawn_timer = 0
        self.spawn_delay = 3

        self.meters = 0
        self.meter_speed = 5
        self.survival_time = 0

        self.next_gate_meter = 100

        self.gate = None
        self.in_gate_mode = False

        self.gate_timer = 0
        self.gate_think_time = 5
        self.gate_answer_phase = False

        # ---------------- BUTTONS ----------------
        self.start_btn = pygame.Rect(220, 330, 360, 95)
        self.quit_btn = pygame.Rect(220, 450, 360, 95)

        self.easy_btn = pygame.Rect(220, 280, 360, 95)
        self.medium_btn = pygame.Rect(220, 400, 360, 95)
        self.hard_btn = pygame.Rect(220, 520, 360, 95)

        # 🔥 CHARACTER BUTTONS (5)
        self.char_buttons = []
        start_x = (800 - (5 * 110 + 4 * 20)) // 2
        start_y = 300
        spacing = 130

        for i in range(5):
            rect = pygame.Rect(start_x + i * spacing, start_y, 110, 150)
            self.char_buttons.append(rect)

        # ---------------- IMAGES ----------------
        self.title_img = pygame.transform.scale(
            pygame.image.load("title.png").convert_alpha(), (700, 200)
        )
        self.start_img = pygame.transform.scale(
            pygame.image.load("start.png").convert_alpha(), (360, 95)
        )
        self.easy_img = pygame.transform.scale(
            pygame.image.load("easy.png").convert_alpha(), (360, 95)
        )
        self.medium_img = pygame.transform.scale(
            pygame.image.load("medium.png").convert_alpha(), (360, 95)
        )
        self.hard_img = pygame.transform.scale(
            pygame.image.load("hard.png").convert_alpha(), (360, 95)
        )
        self.quit_img = pygame.transform.scale(
            pygame.image.load("quit.png").convert_alpha(), (360, 95)
        )
        self.select_img = pygame.transform.scale(
            pygame.image.load("select_difficulty.png").convert_alpha(), (400, 80)
        )

        # 🔥 CHARACTER PREVIEWS
        self.char_images = []
        for i in range(5):
            img = pygame.image.load(f"char{i+1}.png").convert_alpha()
            img = pygame.transform.scale(img, (110, 150))
            self.char_images.append(img)

        self.title_rect = self.title_img.get_rect(center=(400, 150))

    # ---------------- RESET ----------------
    def restart(self):
        pygame.mixer.music.fadeout(300)
        pygame.mixer.music.load(self.game_music)
        pygame.mixer.music.play(-1, fade_ms=300)
        
        self.obstacles.clear()
        self.meters = 0
        self.spawn_timer = 0

        self.player = Character(self.lanes, self.HEIGHT, self.selected_character)

        self.state = "playing"
        self.paused = False

        self.gate = None
        self.in_gate_mode = False
        self.next_gate_meter = 100

        self.gate_timer = 0
        self.gate_answer_phase = False
        self.meter_paused = False

    # ---------------- TEXT ----------------
    def draw_text(self, text, x, y, big=False):
        font = self.big_font if big else self.font
        surface = font.render(text, True, (255, 255, 255))
        rect = surface.get_rect(center=(x, y))
        self.screen.blit(surface, rect)

    # ---------------- EVENTS ----------------
    def handle_events(self):
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and self.state == "playing":
                    self.paused = not self.paused

            if event.type == pygame.MOUSEBUTTONDOWN:

                if self.state == "menu":
                    if self.start_btn.collidepoint(mouse):
                        self.tap_sound.play()
                        self.state = "difficulty"

                    elif self.quit_btn.collidepoint(mouse):
                        self.tap_sound.play()
                        self.running = False

                elif self.state == "difficulty":

                    if self.easy_btn.collidepoint(mouse):
                        self.tap_sound.play()
                        self.spawn_delay = 3
                        self.meter_speed = 5
                        self.difficulty = "Easy"
                        self.state = "character_select"

                    elif self.medium_btn.collidepoint(mouse):
                        self.tap_sound.play()
                        self.spawn_delay = 2
                        self.meter_speed = 10
                        self.difficulty = "Medium"
                        self.state = "character_select"

                    elif self.hard_btn.collidepoint(mouse):
                        self.tap_sound.play()
                        self.spawn_delay = 1
                        self.meter_speed = 15
                        self.difficulty = "Hard"
                        self.state = "character_select"

                elif self.state == "character_select":
                    for i, btn in enumerate(self.char_buttons):
                        if btn.collidepoint(mouse):
                            self.tap_sound.play()
                            self.selected_character = i
                            self.restart()

                elif self.state == "game_over":
                    
                    pygame.mixer.music.fadeout(300)
                    pygame.mixer.music.load(self.menu_music)
                    pygame.mixer.music.play(-1, fade_ms=300)
                                    
                    self.state = "menu"

            if self.state == "playing" and not self.paused:
                self.player.handle_input(event)

    # ---------------- UPDATE ----------------
    def update(self, dt):
        if self.state != "playing" or self.paused:
            return

        self.player.update(dt)
        self.background.update()

        if not self.meter_paused:
            self.meters += self.meter_speed * dt

        self.survival_time += dt

        if self.gate is None and self.meters >= self.next_gate_meter:
            self.gate = Gate(self.difficulty)
            self.in_gate_mode = True
            self.obstacles.clear()

            self.meter_paused = True
            self.gate_timer = 0
            self.gate_answer_phase = False

            self.next_gate_meter += 100

        if self.gate is not None:

            self.gate.update(dt)

            if not self.gate_answer_phase:
                if self.gate.y >= 300:
                    self.gate_answer_phase = True
                    self.gate_timer = 0

            else:
                self.gate_timer += dt
                self.player.update(0)

                if self.gate_timer >= self.gate_think_time:
                    result = self.gate.check_answer(self.player.lane)

                    if result is False:
                        self.wrong_sound.play()
                        self.state = "game_over"
                    else:
                        self.correct_sound.play()

                    self.gate = None
                    self.in_gate_mode = False
                    self.meter_paused = False
                    self.gate_answer_phase = False

        if not self.in_gate_mode:
            self.spawn_timer += dt

            if self.spawn_timer >= self.spawn_delay:
                self.obstacles.append(Obstacle(self.lanes, self.HEIGHT))
                self.spawn_timer = 0

        for obs in self.obstacles:
            obs.update(dt)

        self.obstacles = [o for o in self.obstacles if not o.is_off_screen()]

        for obs in self.obstacles:
            if obs.y < 0:
                continue

            if self.player.hitbox.colliderect(obs.hitbox):

                if obs.type == "low" and not self.player.is_jumping:
                    self.hit_sound.play()
                    self.state = "game_over"

                elif obs.type == "high" and self.player.state != "crouch":
                    self.hit_sound.play()
                    self.state = "game_over"

    # ---------------- DRAW ----------------
    def draw(self):
        self.screen.fill((30, 30, 30))

        if self.state == "menu":
            self.background.draw(self.screen)
            self.screen.blit(self.title_img, self.title_rect)
            self.screen.blit(self.start_img, self.start_btn)
            self.screen.blit(self.quit_img, self.quit_btn)

        elif self.state == "difficulty":
            self.background.draw(self.screen)
            self.screen.blit(self.select_img, (200, 120))
            self.screen.blit(self.easy_img, self.easy_btn)
            self.screen.blit(self.medium_img, self.medium_btn)
            self.screen.blit(self.hard_img, self.hard_btn)

        elif self.state == "character_select":
            self.background.draw(self.screen)

            self.draw_text("Select Character", 400, 150, True)
            self.draw_text(f"Mode: {self.difficulty}", 400, 220)

            for i, btn in enumerate(self.char_buttons):
                self.screen.blit(self.char_images[i], btn)

                if i == self.selected_character:
                    pygame.draw.rect(self.screen, (255, 255, 0), btn, 4)

                if btn.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.screen, (0, 255, 0), btn, 2)

        else:
            self.background.draw(self.screen)

            for obs in self.obstacles:
                obs.draw(self.screen)

            if self.gate:
                self.gate.draw(self.screen)

            self.player.draw(self.screen)

            self.draw_text(f"{int(self.meters)} m", 70, 30)

            minutes = int(self.survival_time // 60)
            seconds = int(self.survival_time % 60)
            self.draw_text(f"Time: {minutes:02}:{seconds:02}", 105, 70)

            self.draw_text(f"Mode: {self.difficulty}", 95, 110)

            if self.paused:
                self.draw_text("PAUSED", 400, 350, True)

            if self.state == "game_over":
                self.draw_text("GAME OVER", 400, 330, True)
                self.draw_text("CLICK TO RETURN MENU", 400, 410)

        pygame.display.flip()

    # ---------------- RUN ----------------
    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()


Game().run()
