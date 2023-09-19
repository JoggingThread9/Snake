import pygame
import sys
import random
from pygame.math import Vector2 as vector2
# vector2(x, y)
from collections import namedtuple

pygame.init()
# initializes the program

green = (0, 255, 0)
kinda_dark_green = (70, 138, 55)
dark_green = (41, 64, 36)
blue = (0, 0, 255)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)
# colors
# (red, green, blue)

block_size = 25
block_number = 30
total = block_size * block_number
# dimensions and screen size

display = pygame.display.set_mode((total, total))
# builds the screen for the game

font = pygame.font.Font(None, 25)
# makes a font for the program to write with

clock = pygame.time.Clock()

point = namedtuple('point', 'x, y')
# the coordinate system
# https://www.youtube.com/watch?v=--nsd2ZeYvs&t=689s

score = 0
# how many apples the snake eats

WINDOW_UPDATE = pygame.USEREVENT
pygame.time.set_timer(WINDOW_UPDATE, 100)
# event is triggered every 150 milliseconds


apple_sprite = pygame.image.load('apple.png')
# apple image
apple_sprite = pygame.transform.scale(apple_sprite, (block_size, block_size))
# scales the image to match the block size

#######################################################################################################################


def draw_grid():
    # https://www.youtube.com/watch?v=_Uq4RXtMRiU&ab_channel=TechWithTim
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
    text = font.render(str(score), True, white)
    # makes a variable that uses the font to write the score
    display.blit(text, [0, 0])
    # puts the text on the top left of the screen

#######################################################################################################################


class snake:
    def __init__(self):
        self.body = [vector2(15, 15)]
        # makes a body for the snake using the head and vectors
        self.head = point(self.body[0].x, self.body[0].y)
        # makes a variable for the first block of the snake
        self.direction = (1, 0)
        # uses the vector as a way for the snake to move
        self.grow = False
        # indicates if the snake should grow

    def draw_snake(self):
        for part in self.body:
            # cycles through the body of the snake
            if part == snake.body[0]:
                snake_rect = pygame.Rect(part.x * block_size, part.y * block_size, block_size, block_size)
                # makes a rectangle for the head of snake
                pygame.draw.rect(display, dark_green, snake_rect)
                # draws the rectangle
            else:
                snake_rect = pygame.Rect(part.x * block_size, part.y * block_size, block_size, block_size)
                # makes a rectangle for the body of snake
                pygame.draw.rect(display, kinda_dark_green, snake_rect)
                # draws the rectangle

    def movement(self):
        # https://www.youtube.com/watch?v=QFvqStqPCRU&ab_channel=ClearCode
        if self.grow:
            # if the snake will grow
            body_copy = self.body
            # makes a mutable copy of the body
            body_copy.insert(0, body_copy[0] + self.direction)
            #
            self.body = body_copy[:]
            # sets body to the body_copy with all the changes made
            self.grow = False
            # once a block is added then it is reset to false, so it does not continuously keep adding block
        else:
            # if the snake doesn't grow
            body_copy = self.body
            # makes sure that the body moves collectively and not just leave squares on the screen
            body_copy.insert(0, body_copy + self.direction)
            self.body = body_copy
            # sets body back to body copy, so it shows the changes made


#######################################################################################################################


class apple:
    def __init__(self):
        self.x = None
        self.y = None
        self.pos = None
        # place holders for variables
        self.randomize()
        # gives the apple a random position

    def randomize(self):
        self.x = random.randint(0, block_number - 1)
        self.y = random.randint(0, block_number - 1)
        # randomizes the x and y coordinates
        self.pos = point(self.x, self.y)
        # puts the coordinates into a list, so they can be easily compared

    def draw_apple(self):
        apple_rect = pygame.Rect(self.x * block_size, self.y * block_size, block_size, block_size)
        # makes a rect for the apple

        display.blit(apple_sprite, apple_rect)
        # puts the apple image over the apple rect so that they are in the same place

        # pygame.draw.rect(display, red, apple_rect)
        # draws the apple


#######################################################################################################################


class conditions:
    def reset(self):
        global score
        # allows for score to be used outside
        apple.randomize()
        # changes the position of the apple
        snake.body = [vector2(15, 15)]
        # resets the body of the snake
        snake.direction = vector2(1, 0)
        # resets the direction of the snake
        score = 0

    def eat(self):
        global score
        # allows for score to be used outside
        if snake.body[0] == apple.pos:
            # checks if the snake eats the apple
            apple.randomize()
            # changes the position of the apple
            snake.grow = True
            # sets grow to true so the snake can grow
            score += 1

    def fail(self):
        if snake.body[0].x < 0 or snake.body[0].x >= block_number:
            # checks if the snake runs into the left or right wall
            self.reset()
            # resets the snake and changes the position of the apple
        if snake.body[0].y < 0 or snake.body[0].y >= block_number:
            # checks if the snake ran into the top or bottom wall
            self.reset()
            # resets the snake and changes the position of the apple

    def collision(self):
        # if the snake runs into itself
        for part in snake.body[1:]:
            # cycles through the snakes body besides the head
            if snake.body[0] == part:
                # checks if any part of the snake is the same as the head
                self.reset()
                # resets the snake and changes apple position

    def update(self):
        snake.movement()
        self.eat()
        self.collision()
        self.fail()
        # checks all of these whenever update is called
#######################################################################################################################


snake = snake()
apple = apple()
conditions = conditions()
# allows you to call all of different classes for use


while True:
    for event in pygame.event.get():
        # checks if the user has done anything
        if event.type == WINDOW_UPDATE:
            conditions.update()
        if event.type == pygame.QUIT:
            # checks if the uses quits the game
            pygame.quit()
            sys.exit()
            # quits the game
        if event.type == pygame.KEYDOWN:
            # checks if the user presses a movement key
            if event.key == pygame.K_ESCAPE:
                # checks if the uses quits the game
                pygame.quit()
                sys.exit()
                # quits the game
        if snake.body[0].x < apple.pos.x:
            if snake.direction != (-1, 0):
                # checks if the snake is moving left, so it does not run into itself
                snake.direction = vector2(1, 0)
                # makes sure the snake will not go into itself
                # right
        if snake.body[0].x > apple.pos.x:
            if snake.direction != (1, 0):
                # checks if the snake is moving right, so it does not run into itself
                snake.direction = vector2(-1, 0)
                # makes sure the snake will not go into itself
                # left
        if snake.body[0].y > apple.pos.y:
            if snake.direction != (0, 1):
                # checks if the snake is moving down, so it does not run into itself
                snake.direction = vector2(0, -1)
                # makes sure the snake will not go into itself
                # up
        if snake.body[0].y < apple.pos.y:
            if snake.direction != (0, -1):
                # checks if the snake is moving up, so it does not run into itself
                snake.direction = vector2(0, 1)
                # makes sure the snake will not go into itself
                # down

    display.fill(black)
    # makes the display black

    draw_grid()
    draw_score()
    snake.draw_snake()
    apple.draw_apple()
    # draws the grid, score, snake, and apple

    pygame.display.update()
    # updates the display screen

    clock.tick(60)
    # allows for the game to run at 60 fps







