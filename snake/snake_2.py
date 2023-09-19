import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()

font = pygame.font.Font(None, 25)


# gives the program something to write with


class direction(Enum):
    right = 1
    left = 2
    up = 3
    down = 4
    # movement system


Point = namedtuple('Point', 'x, y')
speed = 40
block_size = 20


class snakegameAI:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # gives the height and width
        self.display = pygame.display.set_mode(self.w, self.h)
        pygame.display.set_caption('Snake')
        # creates and names the display
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.direction = direction.right

        self.head = Point(self.w / 2, self.h / 2)

        self.snake = [self.head,
                      Point(self.head.x - block_size, self.head.y),
                      Point(self.head.x - block_size, self.head.y)]

        self.score = 0
        self.food = None
        self.place_food()
        self.frame_iteration = 0

    def place_food(self):
        x = random.randint(0, (self.w - block_size) // block_size) * block_size
        y = random.randint(0, (self.h - block_size) // block_size) * block_size

        self.food = Point(x, y)

        if self.food in self.snake:
            self.place_food()

    def play_step(self, action):
        self.frame_iteration += 1

        for event in pygame.event.get():
            if event.type == pygame.quit():
                pygame.quit()
                quit()

        # move
        self.move(action)  # update the head
        self.snake.insert(0, self.head)

        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # place new food or just move
        if self.head == self.food:
            self.score += 1
            reward += 10
            self.place_food()
        else:
            self.snake.pop()

        # update ui and clock
        self.update_ui()
        self.clock.tick(speed)

        # return game over and score
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - block_size or pt.x < 0 or pt.y > self.h - block_size or pt.y < 0:
            return True

        # hits itself
        if pt in self.snake[1:]:
            return True

        return False

    def update_ui(self):
        self.display.fill(0, 0, 0)

        for pt in self.snake:
            pygame.draw.rect(self.display, (255, 0, 0), pygame.Rect(pt.x, pt.y, block_size, block_size))
            pygame.draw.rect(self.display, (0, 255, 0), pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        pygame.draw.rect(self.display, (255, 0, 0), pygame.Rect(self.food.x, self.food.y, block_size, block_size))

        text = font.render("Score: " + str(self.score), True, (255, 255, 255))

        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def move(self, action):
        clock_wise = [direction.right, direction.down, direction.left, direction.up]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]
        else:
            next_idx = (idx - 4) % 4
            new_dir = clock_wise[next_idx]

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == direction.right:
            x += block_size
        elif self.direction == direction.left:
            x -= block_size
        elif self.direction == direction.down:
            y += block_size
        elif self.direction == direction.up:
            y -= block_size

        self.head = Point(x, y)
