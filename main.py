import pygame
import sys
import copy
import random


class GameOfLife:
    def __init__(self):
        pygame.init()

        self.WIDTH, self.HEIGHT = 600, 600
        self.GRID_SIZE = 10
        self.GRID_WIDTH = self.WIDTH // self.GRID_SIZE
        self.GRID_HEIGHT = self.HEIGHT // self.GRID_SIZE
        self.GRID_COLOR = (255, 255, 255)
        self.BG_COLOR = (0, 0, 0)
        self.CELL_COLOR = (0, 150, 0)
        self.FPS = 30
        self.userFPS = 5
        self.numberOfIterations = 0

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Game of Life (Paused)")

        self.grid = [
            [0 for _ in range(self.GRID_WIDTH)] for _ in range(self.GRID_HEIGHT)
        ]

        self.clock = pygame.time.Clock()
        self.running = True
        self.isPaused = True

    def draw_grid(self):
        for x in range(0, self.WIDTH, self.GRID_SIZE):
            pygame.draw.line(self.screen, self.GRID_COLOR, (x, 0), (x, self.HEIGHT))
        for y in range(0, self.HEIGHT, self.GRID_SIZE):
            pygame.draw.line(self.screen, self.GRID_COLOR, (0, y), (self.WIDTH, y))

    def draw_cells(self):
        for x in range(self.GRID_WIDTH):
            for y in range(self.GRID_HEIGHT):
                if self.grid[x][y] == 1:
                    pygame.draw.rect(
                        self.screen,
                        self.CELL_COLOR,
                        (
                            x * self.GRID_SIZE,
                            y * self.GRID_SIZE,
                            self.GRID_SIZE,
                            self.GRID_SIZE,
                        ),
                    )

    def get_neighbour_count(self, x, y, board):
        counter = 0
        for let in [-1, 0, 1]:
            for jet in [-1, 0, 1]:
                if let == 0 and jet == 0:
                    continue
                if x + let < 0 or x + let == self.GRID_WIDTH:
                    continue
                if y + jet < 0 or y + jet == self.GRID_HEIGHT:
                    continue
                counter += board[x + let][y + jet]
        return counter

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(pygame.mouse.get_pos())
                    if (
                        self.grid[pygame.mouse.get_pos()[0] // self.GRID_SIZE][
                            pygame.mouse.get_pos()[1] // self.GRID_SIZE
                        ]
                        == 0
                    ):
                        self.grid[pygame.mouse.get_pos()[0] // self.GRID_SIZE][
                            pygame.mouse.get_pos()[1] // self.GRID_SIZE
                        ] = 1
                    else:
                        self.grid[pygame.mouse.get_pos()[0] // self.GRID_SIZE][
                            pygame.mouse.get_pos()[1] // self.GRID_SIZE
                        ] = 0

                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.isPaused = not self.isPaused
                    if self.isPaused:
                        self.userFPS = self.FPS
                        self.FPS = 30
                        pygame.display.set_caption("Game of Life (Paused)")
                        self.numberOfIterations = 0
                    else:
                        self.FPS = self.userFPS
                        pygame.display.set_caption(
                            "Game of Life, Speed: "
                            + str(self.FPS)
                            + ", number of iterations: "
                            + str(self.numberOfIterations)
                        )

                if self.isPaused:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        for x in range(self.GRID_HEIGHT):
                            for y in range(self.GRID_WIDTH):
                                self.grid[x][y] = int(random.uniform(0, 2))
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                        for x in range(self.GRID_HEIGHT):
                            for y in range(self.GRID_WIDTH):
                                self.grid[x][y] = 0

                if not self.isPaused:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                        if self.FPS > 1:
                            self.FPS -= 1
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                        if self.FPS < 200:
                            self.FPS += 1

            new_board = copy.deepcopy(self.grid)
            if not self.isPaused:
                self.numberOfIterations += 1
                pygame.display.set_caption(
                    "Game of Life, Speed: "
                    + str(self.FPS)
                    + ", number of iterations: "
                    + str(self.numberOfIterations)
                )

                for x in range(self.GRID_HEIGHT):
                    for y in range(self.GRID_WIDTH):
                        neighbour_count = self.get_neighbour_count(x, y, self.grid)
                        if self.grid[x][y] == 1 and (
                            neighbour_count == 2 or neighbour_count == 3
                        ):
                            continue
                        if self.grid[x][y] == 0 and neighbour_count == 3:
                            new_board[x][y] = 1
                            continue
                        new_board[x][y] = 0
            self.grid = copy.deepcopy(new_board)
            self.screen.fill(self.BG_COLOR)
            self.draw_grid()
            self.draw_cells()
            pygame.display.flip()
            self.clock.tick(self.FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = GameOfLife()
    game.run()
