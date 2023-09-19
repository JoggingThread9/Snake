import pygame
import time
import random

# init pygame
pygame.init()

# colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
orange = (255, 165, 0)
green = (0, 255, 0)
width, height = 600, 400

game_display = pygame.display.set_mode((width, height))
pygame.display.set_caption("NeuralNine Snake Game")

clock = pygame.time.Clock()

block_size = 10
snake_speed = 20

message_font = pygame.font.SysFont('ubuntu', 30)
score_font = pygame.font.SysFont('ubuntu', 25)


def draw_score(score):
    text = score_font.render("Score: " + str(score), True, orange)
    game_display.blit(text, [0, 0])


def draw_snake(snake_pixels):
    for pixel in snake_pixels:
        pygame.draw.rect(game_display, white, [pixel[0], pixel[1], block_size, block_size])


def run_game():
    prev_move = None
    game_over = True
    game_close = True

    x = width / 2
    y = width / 2

    x_speed = 0
    y_speed = 0

    snake_pixels = []
    snake_length = 3

    food_x = round(random.randint(0, (width - block_size) // block_size) * block_size)
    food_y = round(random.randint(0, (width - block_size) // block_size) * block_size)

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
            move = random.randint(0, 3)
            if move == 0:
                x_speed = -block_size
                y_speed = 0
                # left
            elif move == 1:
                x_speed = block_size
                y_speed = 0
                # right
            elif move == 2:
                y_speed = -block_size
                x_speed = 0
                # up
            elif move == 3:
                y_speed = block_size
                x_speed = 0
                # down
        x += x_speed
        y += y_speed

        if x >= width or x < 0 or y >= width or y < 0:
            x = width / 2
            y = width / 2

        x += x_speed
        y += y_speed

        game_display.fill(black)
        pygame.draw.rect(game_display, red, [food_x, food_y, block_size, block_size])
        snake_pixels.append([x, y])

        if len(snake_pixels) > snake_length:
            del snake_pixels[0]

        for pixel in snake_pixels[:-1]:
            if pixel == [x, y]:
                game_close = False

        draw_snake(snake_pixels)
        draw_score(snake_length - 3)

        pygame.display.update()

        if x == food_x and y == food_y:
            food_x = round(random.randint(0, (width - block_size) // block_size) * block_size)
            food_y = round(random.randint(0, (width - block_size) // block_size) * block_size)
            snake_length += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

run_game()
