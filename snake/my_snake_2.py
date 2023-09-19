import pygame
import sys
import random
from collections import namedtuple

pygame.init()

green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)
# colors

block_size = 20
block_number = 30
total = block_size * block_number

display = pygame.display.set_mode((total, total))
font = pygame.font.Font(None, 25)

point = namedtuple('point', 'x, y')


class snake:
    def __init__(self):
        self.pos = None
        self.head = point(game.x, game.y)
        self.snake_body = [self.head,
                           point(self.head.x - block_size, self.head.y),
                           point(self.head.x - block_size, self.head.y)]

    def draw_snake(self):
        self.head.x = point(game.x - block_size, game.y)
        self.head.y = point(game.x, game.y - block_size)

        for block in self.snake_body:
            block_rect = pygame.Rect(block.x, block.y, block_size, block_size)
            pygame.draw.rect(display, green, block_rect)


class apple:
    def __init__(self):
        self.pos = None
        self.x = None
        self.y = None
        self.randomize()

    def draw_apple(self):
        apple_rect = pygame.Rect(int(self.x * block_size), int(self.y * block_size), block_size, block_size)
        pygame.draw.rect(display, red, apple_rect)

    def randomize(self):
        self.x = round(random.randint(0, block_number - 1))
        self.y = round(random.randint(0, block_number - 1))
        self.pos = [self.x, self.y]


class game:
    x = total / 2
    y = total / 2

    x_speed = 0
    y_speed = 0

    def __init__(self):
        self.snake = snake()
        self.apple = apple()

    def draw_elements(self):
        self.apple.draw_apple()
        self.snake.draw_snake()

    def reset(self):
        self.apple.randomize()
        self.snake.head.x = game.x
        self.snake.head.y = game.y
        self.snake.snake_body = [self.snake.head,
                                 point(snake.head.x - block_size, snake.head.y),
                                 point(snake.head.x - block_size, snake.head.y)]

    def fail(self):
        pass

    def update(self):
        pass

    def grow(self):
        if self.snake.pos == self.apple.pos:
            self.apple.randomize()
            pass


game = game()
snake = snake()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        move = random.randint(0, 3)

        if move == 0:
            game.x += block_size
        elif move == 1:
            game.x += -block_size
        elif move == 2:
            game.y += block_size
        elif move == 3:
            game.y += -block_size

        snake.head = point(snake.head.x, snake.head.y)

    display.fill(black)

    game.draw_elements()

    game.update()

    pygame.display.update()
