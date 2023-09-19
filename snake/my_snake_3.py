import pygame
import sys
import random
from collections import namedtuple

pygame.init()

green = (0, 255, 0)
dark_green = (0, 150, 100)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)
# colors

score = 0

block_size = 20
block_number = 30
total = block_size * block_number

display = pygame.display.set_mode((total, total))
font = pygame.font.Font(None, 25)

clock = pygame.time.Clock()

point = namedtuple('Point', 'x, y')


def draw_score():
    text = font.render("Score " + str(score), True, white)
    display.blit(text, [0, 0])


class snake:
    def __init__(self):
        self.x = total / 2
        self.y = total / 2
        self.head = point(self.x, self.y)
        self.snake_body = [self.head,
                  point(self.head.x + block_size, self.head.y),
                  point(self.head.x + block_size, self.head.y)]

    def draw_snake(self):
        for block in self.snake_body:
            pygame.draw.rect(display, green, block.x, block.y, block_size)


class apple:
    def __init__(self):
        self.x = None
        self.y = None
        self.pos = None
        self.randomize()

    def randomize(self):
        self.x = random.randint(0, total)
        self.y = random.randint(0, total)
        self.pos = point(self.x, self.y)

    def draw_apple(self):
        apple_rect = pygame.Rect(self.x, self.y, block_size, block_size)
        pygame.draw.rect(display, red, apple_rect)


apple = apple()
snake = snake()


def collision():
    if snake.snake_body[0] in apple.pos:
        apple.randomize()
        snake.snake_body.insert(0, snake.head)
        snake.snake_length += 1


def fail():
    if snake.x > total or snake.x < 0 or snake.y > total or snake.y < 0:
        snake.x = total / 2
        snake.y = total / 2
        apple.randomize()
    for block in snake.snake_body[:-1]:
        if block == snake.snake_pos:
            snake.x = total / 2
            snake.y = total / 2
            apple.randomize()


def update():
    collision()
    fail()


def draw_elements():
    apple.draw_apple()
    draw_snake(snake)
    draw_score()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:  # right
                snake.x_speed = block_size
                snake.y_speed = 0
            if event.key == pygame.K_a:  # left
                snake.x_speed = -block_size
                snake.y_speed = 0
            if event.key == pygame.K_w:  # up
                snake.x_speed = 0
                snake.y_speed = -block_size
            if event.key == pygame.K_s:  # down
                snake.x_speed = 0
                snake.y_speed = block_size

    snake.x += snake.x_speed
    snake.y += snake.y_speed

    display.fill(black)

    draw_elements()
    update()


    pygame.display.update()
    clock.tick(60)


