import pygame
import sys
import copy

pygame.init()

WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
GRID_COLOR = (255, 255, 255)
BG_COLOR = (0, 0, 0)
CELL_COLOR = (255, 0, 0)
FPS = 30

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")

grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]


def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))


def draw_cells():
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x][y] == 1:
                pygame.draw.rect(
                    screen,
                    CELL_COLOR,
                    (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE),
                )


def getNeighbourCount(x, y, board):
    counter = 0
    for let in [-1, 0, 1]:
        for jet in [-1, 0, 1]:
            if let == 0 and jet == 0:
                continue
            if x + let < 0 or x + let == GRID_WIDTH:
                continue
            if y + jet < 0 or y + jet == GRID_HEIGHT:
                continue
            counter += board[x + let][y + jet]
    return counter


clock = pygame.time.Clock()

running = True
isPaused = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
            grid[int(pygame.mouse.get_pos()[0] / GRID_WIDTH)][
                int(pygame.mouse.get_pos()[1] / GRID_HEIGHT)
            ] = 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            isPaused = not isPaused
            print("jdjd")
        if isPaused:
            FPS = 30
        else:
            FPS = 1

    newBoard = copy.deepcopy(grid)
    if not isPaused:
        for x in range(GRID_HEIGHT):
            for y in range(GRID_WIDTH):
                neighbour_count = getNeighbourCount(x, y, grid)
                if grid[x][y] == 1 and (neighbour_count == 2 or neighbour_count == 3):
                    continue
                if grid[x][y] == 0 and neighbour_count == 3:
                    newBoard[x][y] = 1
                    continue
                newBoard[x][y] = 0

    grid = copy.deepcopy(newBoard)
    screen.fill(BG_COLOR)
    draw_grid()
    draw_cells()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
