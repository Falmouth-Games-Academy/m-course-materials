import pygame
import time
import copy


tile_size = 70



class Board:
    def __init__(self, filename):
        self.numbers = [[None for i in range(9)] for j in range(9)]
        self.fixed = [[False for i in range(9)] for j in range(9)]

        with open(filename, 'rt') as f:
            y = 0
            for line in f:
                x = 0
                for c in line:
                    if c.isdigit():
                        self.numbers[x][y] = int(c)
                        self.fixed[x][y] = True
                    x += 1
                y += 1

    def draw(self, screen):
        screen.fill((255, 255, 255))

        for (x1, y1, x2, y2) in self.find_invalid_numbers():
            pygame.draw.rect(screen, (255, 200, 200), pygame.Rect(x1 * tile_size, y1 * tile_size, tile_size, tile_size))
            pygame.draw.rect(screen, (255, 200, 200), pygame.Rect(x2 * tile_size, y2 * tile_size, tile_size, tile_size))
            #pygame.draw.line(screen, (255, 100, 100), ((x1 + 0.5) * tile_size, (y1 + 0.5) * tile_size), ((x2 + 0.5) * tile_size, (y2 + 0.5) * tile_size), tile_size // 2)

        for i in range(1, 9):
            width = 3 if (i % 3) == 0 else 1
            pygame.draw.line(screen, (0, 0, 0), (i * tile_size, 0), (i * tile_size, 9 * tile_size), width)
            pygame.draw.line(screen, (0, 0, 0), (0, i * tile_size), (9 * tile_size, i * tile_size), width)

        big_font = pygame.font.Font("FreeSans.ttf", tile_size - 10)
        small_font = pygame.font.Font("FreeSans.ttf", (tile_size - 10) // 3)
        for y in range(9):
            for x in range(9):
                n = self.numbers[x][y]
                if n is None:
                    pass
                elif type(n) is int:
                    text = big_font.render(str(n), True, (0, 0, 0) if self.fixed[x][y] else (0, 0, 255))
                    text_rect = text.get_rect()
                    text_rect.center = ((x + 0.5) * tile_size, (y + 0.5) * tile_size)
                    screen.blit(text, text_rect)
                elif type(n) is list:
                    for x2 in range(3):
                        for y2 in range(3):
                            m = y2 * 3 + x2 + 1
                            if m in n:
                                text = small_font.render(str(m), True, (0, 0, 0) if self.fixed[x][y] else (0, 0, 255))
                                text_rect = text.get_rect()
                                text_rect.center = ((x + 0.5 + (x2 - 1) / 3) * tile_size, (y + 0.5 + (y2 - 1) / 3) * tile_size)
                                screen.blit(text, text_rect)

    def find_invalid_numbers(self):
        for y in range(9):
            for x in range(9):
                n = self.numbers[x][y]
                if type(n) is int:
                    # check row
                    for x2 in range(x+1, 9):
                        if self.numbers[x2][y] == n:
                            yield (x, y, x2, y)

                    # check column
                    for y2 in range(y+1, 9):
                        if self.numbers[x][y2] == n:
                            yield (x, y, x, y2)

                    # check square
                    sx = x // 3
                    sy = y // 3
                    for y2 in range(y, sy * 3 + 3):
                        start_x = x + 1 if y == y2 else sx * 3
                        for x2 in range(start_x, sx * 3 + 3):
                            if self.numbers[x2][y2] == n:
                                yield (x, y, x2, y2)

    def is_valid(self):
        for _ in self.find_invalid_numbers():
            return False
        else:
            return True


def solve_backtracking(screen, board, x, y):
    potential_values = range(1, 10)
    if board.fixed[x][y]:
        potential_values = [board.numbers[x][y]]

    next_x = x + 1
    if next_x < 9:
        next_y = y
    else:
        next_x = 0
        next_y = y + 1

    for v in potential_values:
        board.numbers[x][y] = v

        board.draw(screen)
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size), 3)
        pygame.display.flip()
        time.sleep(0.1)

        if board.is_valid() and (next_y == 9 or solve_backtracking(screen, board, next_x, next_y)):
            return True
    else:
        if not board.fixed[x][y]:
            board.numbers[x][y] = None
        return False


def solve_constraint_propagation(screen, board):
    # Initialise
    for y in range(9):
        for x in range(9):
            if board.numbers[x][y] is None:
                board.numbers[x][y] = list(range(1, 10))

    # Look at constraints
    changed = True
    while changed:
        changed = False
        for y in range(9):
            for x in range(9):
                candidates = board.numbers[x][y]
                if type(candidates) == list:
                    good_candidates = []
                    for candidate in candidates:
                        board.numbers[x][y] = candidate
                        if board.is_valid():
                            good_candidates.append(candidate)

                    if len(good_candidates) == 0:
                        return False
                    elif len(good_candidates) == 1:
                        board.numbers[x][y] = good_candidates[0]
                    else:
                        board.numbers[x][y] = good_candidates

                    if candidates != good_candidates:
                        changed = True

                    board.draw(screen)
                    pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size), 3)
                    pygame.display.flip()
                    time.sleep(0.3)

    return True


def solve_combined_bt(screen, board, x, y):
    potential_values = board.numbers[x][y]

    next_x = x + 1
    if next_x < 9:
        next_y = y
    else:
        next_x = 0
        next_y = y + 1

    if type(potential_values) != list:
        return solve_combined_bt(screen, board, next_x, next_y)

    for v in potential_values:
        old_board = copy.deepcopy(board.numbers)
        board.numbers[x][y] = v

        board.draw(screen)
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size), 3)
        pygame.display.flip()
        time.sleep(0.1)

        if solve_combined(screen, board):
            return True
        else:
            board.numbers = old_board
    else:
        return False


def solve_combined(screen, board):
    if not solve_constraint_propagation(screen, board):
        return False

    is_unsolved = False
    for y in range(9):
        for x in range(9):
            if type(board.numbers[x][y]) is list:
                is_unsolved = True
                if len(board.numbers[x][y]) == 0:
                    return False

    if is_unsolved:
        return solve_combined_bt(screen, board, 0, 0)
    else:
        return True


def main():
    # Initialise PyGame
    pygame.init()
    clock = pygame.time.Clock()

    board = Board("puzzle_easy.txt")

    window_width = 9 * tile_size
    window_height = 9 * tile_size
    window_size = (window_width, window_height)

    # Create the screen
    screen = pygame.display.set_mode(window_size)

    board.draw(screen)
    pygame.display.flip()

    solve_backtracking(screen, board, 0, 0)
    #solve_constraint_propagation(screen, board)
    #solve_combined(screen, board)

    board.draw(screen)
    pygame.display.flip()

    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            break


if __name__ == '__main__':
    main()
