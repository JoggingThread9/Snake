import pygame
import sys
import random
from collections import namedtuple
import time

pygame.init()
# initializes the program


green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)
# colors
# (red, green, blue)

block_size = 20
block_number = 30
total = block_size * block_number
# dimensions and screen size
display = pygame.display.set_mode((total, total))
# builds the screen for the game

font = pygame.font.Font(None, 25)

clock = pygame.time.Clock()

point = namedtuple('point', 'x, y')
# the coordinate system


class apple:
    def __init__(self):
        self.x = None
        self.y = None
        self.pos = None
        # place holders for variables
        self.randomize()
        # gives the apple a random position

    def randomize(self):
        self.x = random.randint(0, block_number - 1) * block_size
        self.y = random.randint(0, block_number - 1) * block_size
        # randomizes the x and y coordinates
        self.pos = point(self.x, self.y)
        # puts the coordinates into a list, so they can be easily compared

    def draw_apple(self):
        apple_rect = pygame.Rect(self.x, self.y, block_size, block_size)
        # makes a rectangle for the apple
        pygame.draw.rect(display, red, apple_rect)
        # draws the rectangle on the screen


def draw_grid():
    between = block_size
    # space between the grid boxes
    grid_x = 0
    grid_y = 0
    # x and y position for the grid
    for i in range(block_number):
        # makes 30 boxes per row
        grid_x = grid_x + between
        # makes sure there is an equal space between the horizontal lines
        grid_y = grid_y + between
        # makes sure there is an equal space between the vertical line
        pygame.draw.line(display, white, (grid_x, 0), (grid_x, total))
        # draws the horizontal line
        pygame.draw.line(display, white, (0, grid_y), (total, grid_y))
        # draws the vertical lines


def draw_score():
    text = font.render(str(len(game.body) - 1), True, white)
    display.blit(text, [0, 0])


class game:
    x = total / 2
    y = total / 2
    # x and y coordinates for the snake
    # places the snake in the center of the board

    head = point(x, y)
    # defines the head of the snake
    # uses the named tuple to make a position for the snake

    body = [head]
    # a list with the multiple segments of the snake

    body_copy = [head]
    # a mutable copy of the snake

    apple = apple()
    # allows me to pull info and functions from the apple class

    def draw_snake(self):
        # function to draw the snake
        for block in game.body:
            # cycles through the body of the snake
            snake_rect = pygame.Rect(block.x, block.y, block_size, block_size)
            # gives the snake a rectangle
            pygame.draw.rect(display, green, snake_rect)
            # draws that said rectangle

    def run(self):
        # the game
        x_speed = 0
        y_speed = 0
        # how much the snake will move
        while True:
            clock.tick(900)
            # gives a 900 millisecond delay
            for event in pygame.event.get():
                # checks if the user has done anything
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    # if the user presses the exit button on the screen the game will end
                if event.type == pygame.KEYDOWN:
                    # checks if the user presses a key to move the snake
                    if event.key == pygame.K_d:
                        x_speed = block_size
                        y_speed = 0
                        # right
                    if event.key == pygame.K_a:
                        x_speed = -block_size
                        y_speed = 0
                        # left
                    if event.key == pygame.K_w:
                        x_speed = 0
                        y_speed = -block_size
                        # up
                    if event.key == pygame.K_s:
                        x_speed = 0
                        y_speed = block_size
                        # down

            game.x += x_speed
            game.y += y_speed
            # moves the snake by changing the increasing or decreasing the x or y

            game.head = point(game.x, game.y)
            # updates the head of the snake with the new values

            game.body = [game.head]
            # updates the body of the snake

            if game.head == game.apple.pos:
                game.apple.randomize()
                # checks if the snake has collided with the apple
                # grows the snake
                # changes the position of the apple

            if game.x < 0 or game.x > total - block_size:
                x_speed = 0
                y_speed = 0
                game.x = total / 2
                game.y = total / 2
                game.apple.randomize()
                # checks if the snake runs into the side
                # if it has, resets the speed and brings it back to the original position and changes the position of the apple
            elif game.y < 0 or game.y > total - block_size:
                x_speed = 0
                y_speed = 0
                game.x = total / 2
                game.y = total / 2
                game.apple.randomize()
                # checks if the snake has run into the top
            # if it has, resets the speed and brings it back to the original position and changes the position of the apple

            for part in game.body[1:]:
                if part == game.head:
                    x_speed = 0
                    y_speed = 0
                    game.x = total / 2
                    game.y = total / 2
                    # checks to see if the snake has run into itself
                    # if it has, resets the speed and brings it back to the original positon

            display.fill(black)
            # makes the display black

            draw_grid()
            draw_score()
            # draws the score and the grid

            game.apple.draw_apple()
            game.draw_snake()
            # draws the sprites

            pygame.display.update()
            # updates the display
            time.sleep(.1)
            # delays the program so it doesn't run too fast
            clock.tick(60)
            # makes it run at 60 fps


game = game()
game.run()
