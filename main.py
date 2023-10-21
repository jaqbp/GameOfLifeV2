import pygame
import sys
import copy
import random
import time


class GameOfLife:
    def __init__(self):
        pygame.init()

        self.WIDTH, self.HEIGHT = 600, 600
        self.GRID_SIZE = 20
        self.GRID_WIDTH = self.WIDTH // self.GRID_SIZE
        self.GRID_HEIGHT = self.HEIGHT // self.GRID_SIZE
        self.GRID_COLOR = (255, 255, 255)
        self.BG_COLOR = (0, 0, 0)
        self.CELL_COLOR = (0, 200, 0)
        self.FPS = 30
        self.userFPS = 5
        self.numberOfIterations = 0
        self.currNumberOfIterations = 0

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Game of Life (Paused)")

        self.grid = [
            [0 for _ in range(self.GRID_WIDTH)] for _ in range(self.GRID_HEIGHT)
        ]

        self.clock = pygame.time.Clock()
        self.running = True
        self.isPaused = True
        self.show_instructions = True

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

    def show_instruction_screen(self):
        self.screen.fill(self.BG_COLOR)
        font = pygame.font.Font(None, 25)
        text = "Welcome to the Game of Life"
        text2 = "Use your mouse to draw, press space to start the simulation"
        text3 = "Use arrows to change the speed of the simulation"
        text4 = "Press C to clear the board and R to generate randomly filled board"
        text5 = "Press S to start"

        rendered_text = font.render(text, True, (0, 200, 0))
        text_rect = rendered_text.get_rect()
        text_rect.center = (self.WIDTH // 2, self.HEIGHT // 2 - 100)
        self.screen.blit(rendered_text, text_rect.topleft)

        rendered_text2 = font.render(text2, True, (0, 200, 0))
        text_rect2 = rendered_text2.get_rect()
        text_rect2.center = (self.WIDTH // 2, self.HEIGHT // 2 - 50)
        self.screen.blit(rendered_text2, text_rect2.topleft)

        rendered_text3 = font.render(text3, True, (0, 200, 0))
        text_rect3 = rendered_text3.get_rect()
        text_rect3.center = (self.WIDTH // 2, self.HEIGHT // 2)
        self.screen.blit(rendered_text3, text_rect3.topleft)

        rendered_text4 = font.render(text4, True, (0, 200, 0))
        text_rect4 = rendered_text4.get_rect()
        text_rect4.center = (self.WIDTH // 2, self.HEIGHT // 2 + 50)
        self.screen.blit(rendered_text4, text_rect4.topleft)

        rendered_text5 = font.render(text5, True, (0, 200, 0))
        text_rect5 = rendered_text5.get_rect()
        text_rect5.center = (self.WIDTH // 2, self.HEIGHT // 2 + 100)
        self.screen.blit(rendered_text5, text_rect5.topleft)
        pygame.display.flip()

        while self.show_instructions:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.show_instructions = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.show_instructions = False

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
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
                        self.currNumberOfIterations = self.numberOfIterations
                    else:
                        self.numberOfIterations = self.currNumberOfIterations
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
                        self.currNumberOfIterations = 0
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

    def run(self):
        while self.running:
            if self.show_instructions:
                self.show_instruction_screen()
            else:
                self.game_loop()

        pygame.quit()


if __name__ == "__main__":
    game = GameOfLife()
    game.run()
