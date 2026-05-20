import pygame
import random


class Gate:
    def __init__(self, difficulty):
        # QUESTIONS
        questions = {
            "Easy": [
                ("easy1_left.png", "easy1_right.png"),
                ("easy2_left.png", "easy2_right.png"),
                ("easy3_left.png", "easy3_right.png"),
                ("easy4_left.png", "easy4_right.png"),
                ("easy5_left.png", "easy5_right.png"),
                ("easy6_left.png", "easy6_right.png"),
                ("easy7_left.png", "easy7_right.png"),
                ("easy8_left.png", "easy8_right.png"),
                ("easy9_left.png", "easy9_right.png"),
                ("easy10_left.png", "easy10_right.png"),
            ],
            "Medium": [
                ("medium1_left.png", "medium1_right.png"),
                ("medium2_left.png", "medium2_right.png"),
                ("medium3_left.png", "medium3_right.png"),
                ("medium4_left.png", "medium4_right.png"),
                ("medium5_left.png", "medium5_right.png"),
                ("medium6_left.png", "medium6_right.png"),
                ("medium7_left.png", "medium7_right.png"),
                ("medium8_left.png", "medium8_right.png"),
                ("medium9_left.png", "medium9_right.png"),
                ("medium10_left.png", "medium10_right.png"),
            ],
            "Hard": [
                ("hard1_left.png", "hard1_right.png"),
                ("hard2_left.png", "hard2_right.png"),
                ("hard3_left.png", "hard3_right.png"),
                ("hard4_left.png", "hard4_right.png"),
                ("hard5_left.png", "hard5_right.png"),
                ("hard6_left.png", "hard6_right.png"),
                ("hard7_left.png", "hard7_right.png"),
                ("hard8_left.png", "hard8_right.png"),
                ("hard9_left.png", "hard9_right.png"),
                ("hard10_left.png", "hard10_right.png"),
            ]
        }

        # pick random pair
        wrong_file, correct_file = random.choice(questions[difficulty])

        # load images
        wrong_img = pygame.image.load(wrong_file).convert_alpha()
        correct_img = pygame.image.load(correct_file).convert_alpha()

        # scale
        wrong_img = pygame.transform.scale(wrong_img, (300, 340))
        correct_img = pygame.transform.scale(correct_img, (300, 340))
        # positions
        self.left_x = 40
        self.right_x = 460

        self.y = -300
        self.speed = 120

        # RANDOM SIDE
        if random.choice([True, False]):
            self.left_img = wrong_img
            self.right_img = correct_img
            self.answer = "right"
        else:
            self.left_img = correct_img
            self.right_img = wrong_img
            self.answer = "left"

        # ✅ NEW: prevent multiple checks (VERY IMPORTANT)
        self.answered = False

    def update(self, dt):
        self.y += self.speed * dt

    def draw(self, screen):
        screen.blit(self.left_img, (self.left_x, self.y))
        screen.blit(self.right_img, (self.right_x, self.y))

    def is_finished(self):
        # gate reached player zone
        return self.y > 520

    def check_answer(self, lane):
        # prevent multiple triggers (sound spam fix)
        if self.answered:
            return None

        self.answered = True

        if lane == 0:
            chosen = "left"
        elif lane == 1:
            chosen = "right"
        else:
            return False

        return chosen == self.answer
