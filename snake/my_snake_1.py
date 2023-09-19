import pygame
import sys
import random
from pygame.math import Vector2
textfile = open('Movements', 'w')
# colors = ((red, green, blue))
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


class snake:
    def __init__(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        # creates a snake with a 3 block body
        self.direction = Vector2(1, 0)
        # starts the initial movement of the snake
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            # defines the x position
            y_pos = int(block.y * cell_size)
            # defines the y position
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            # creates a snake at the designated x and y position and matches the cell_size
            pygame.draw.rect(window, (255, 0, 255), block_rect)
            # draws the rectangle

    def movement(self):
        if self.new_block:
            body_copy = self.body[:]
            # moves the body from the back first to the front, so it stays connected
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            brain.reward += 10
            # continues the movement
            self.new_block = False
            # once a block is added then it is reset to false, so it does not continuously keep adding block
        else:
            body_copy = self.body[:-1]
            # moves the body from the back first to the front, so it stays connected
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            # continues the movement

    def add_block(self):
        self.new_block = True

    def body_reset(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(1, 0)


class brain:
    reward = 0
    moves = []


class apple:
    def __init__(self):
        self.pos = None
        self.x = None
        self.y = None
        # place holders
        self.randomize()
        # places the apple in a random position

    def draw_apple(self):
        apple_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y) * cell_size, cell_size, cell_size)
        # creates a random x and y position and sets the width and height to match the cell_size
        # window.blit(apple_image, apple_rect)
        pygame.draw.rect(window, (255, 0, 0), apple_rect)
        # draws the apple

    def randomize(self):
        # creates a function to randomize the position
        self.x = random.randint(0, cell_number - 1)
        # allows for the x position to be randomized
        self.y = random.randint(0, cell_number - 1)
        # allows for the y position to be randomized
        # this allows for the snake to start at a random position
        self.pos = Vector2(self.x, self.y)


class main:
    # the body of the game
    def __init__(self):
        self.moves = []
        self.snake = snake()
        self.apple = apple()
        # allows us to access the snake and apple easier

    def update(self):
        self.snake.movement()
        # allows for snake movement
        self.collision()
        self.fail()

    def draw_elements(self):
        self.apple.draw_apple()
        self.snake.draw_snake()
        # draws the elements
        self.draw_score()

    def collision(self):
        if self.apple.pos == self.snake.body[0]:
            # checks to see if the head of the snake collides with the apple
            self.apple.randomize()
            # moves the apple to a random position
            self.snake.add_block()
            # adds a block to the snake making it larger
            brain.reward += 10

    def reset(self):
        self.apple.randomize()
        self.snake.body_reset()

    def fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.reset()
            print(brain.moves)
            brain.moves = []
            brain.reward -= 10
            print(brain.reward)
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                brain.reward -= 10
                self.reset()
                print(brain.moves)
                print(brain.reward)
                brain.moves = []

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, black)
        score_rect = score_surface.get_rect(center=(total - 60, total - 40))
        window.blit(score_surface, score_rect)


pygame.init()

cell_size = 40
cell_number = 15
total = cell_size * cell_number

window = pygame.display.set_mode((total, total))
# creates the display
pygame.display.set_caption("AI Snake")
# names the display

image = pygame.image.load('gold_apple.jpeg')
image_size = (cell_size, cell_size)
apple_image = pygame.transform.scale(image, image_size)

game_font = pygame.font.Font(None, 25)

main_game = main()

fps = 60
# frames per second
clock = pygame.time.Clock()
# defines the clock

WINDOW_UPDATE = pygame.USEREVENT
pygame.time.set_timer(WINDOW_UPDATE, 150)
# event is triggered every 150 milliseconds

while True:
    # runs the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # allows for user to close the game

        if event.type == WINDOW_UPDATE:
            main_game.update()
            move = random.randint(0, 3)
            # checks if there is a key press
            if move == 0:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
                    brain.moves.append("up")
                # makes sure the snake will not go into itself
                # up
            if move == 1:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
                    brain.moves.append("right")
                    # makes sure the snake will not go into itself
                # right
            if move == 2:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
                    brain.moves.append("down")
                    # makes sure the snake will not go into itself
                # down
            if move == 3:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
                    brain.moves.append("left")
                    # makes sure the snake will not go into itself
                # left

    window.fill(white)
    # colors the window

    main_game.draw_elements()
    pygame.display.update()
    # draw all our elements
    clock.tick(fps)
