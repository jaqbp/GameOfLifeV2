import pygame
from pygame.locals import *

# Define the dimensions of the grid
GRID_SIZE = 20
CUBE_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 20
GRID_DEPTH = 20

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Define your 3D matrix (replace this with your data)
matrix = [[[0] * GRID_DEPTH for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((GRID_WIDTH * CUBE_SIZE, GRID_HEIGHT * CUBE_SIZE))
pygame.display.set_caption("3D Grid")


def draw_cube(x, y, z):
    if matrix[x][y][z] == 1:
        pygame.draw.rect(
            screen, RED, (x * CUBE_SIZE, z * CUBE_SIZE, CUBE_SIZE, CUBE_SIZE)
        )


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    screen.fill(WHITE)

    # Draw the 3D grid
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            for z in range(GRID_DEPTH):
                draw_cube(x, y, z)

    pygame.display.flip()

pygame.quit()
