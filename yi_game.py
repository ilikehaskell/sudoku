from dataclasses import dataclass
from pprint import pprint
import random
import sys, pygame as pg
from yi import Solution
import copy


pg.init()
pg.font.init()

HEIGHT, WIDTH = 750, 750
CELL_SIZE = WIDTH/9

SCREENSIZE = (HEIGHT, WIDTH)

YELLOW = pg.Color('yellow')
WHITE = pg.Color('white')

FONT = pg.font.SysFont("comicsans", 40)


screen = pg.display.set_mode(SCREENSIZE)


def draw_cell(i,j,fill_with_text = None, color = WHITE):
    cell_rect = pg.Rect(i*CELL_SIZE, j*CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pg.draw.rect(screen, color, cell_rect)
    pg.draw.rect(screen, pg.Color('black'), cell_rect, width=1)
    if fill_with_text and fill_with_text != '.':
        text = FONT.render(str(fill_with_text), True, pg.Color('black'))
        text_rect = text.get_rect(center=cell_rect.center)
        screen.blit(text, text_rect,) 

def draw_grid(grid):
    # print(grid)
    screen.fill(pg.Color('white'))

    for i in range(9):
        for j in range(9):
            if original_board[i][j] == '.':
                draw_cell(i,j, grid[i][j], WHITE)
            else:
                draw_cell(i,j, grid[i][j], YELLOW)

    pg.display.update()
    pg.time.delay(20)





original_board = [[".",".","9","7","4","8",".",".","."],["7",".",".",".",".",".",".",".","."],[".","2",".","1",".","9",".",".","."],[".",".","7",".",".",".","2","4","."],[".","6","4",".","1",".","5","9","."],[".","9","8",".",".",".","3",".","."],[".",".",".","8",".","3",".","2","."],[".",".",".",".",".",".",".",".","6"],[".",".",".","2","7","5","9",".","."]]
# board = board = [["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]
# original_board = [['.', '.', '.', '.', '4', '8', '6', '3', '2'], ['.', '.', '3', '6', '5', '2', '4', '1', '9'], ['4', '2', '6', '1', '3', '9', '8', '7', '5'], ['3', '5', '7', '9', '8', '6', '2', '4', '1'], ['2', '6', '4', '3', '1', '7', '5', '9', '8'], ['1', '9', '8', '5', '2', '4', '3', '6', '7'], ['9', '7', '5', '8', '6', '3', '1', '2', '4'], ['8', '3', '2', '4', '9', '1', '7', '5', '6'], ['6', '4', '1', '2', '7', '5', '9', '8', '3']]

@dataclass
class GameState:
    board = copy.deepcopy(original_board)

gameState = GameState()

def remove_random_squares(board, num = 10):
    to_be_removed = random.sample(range(81), num)
    for square in to_be_removed:
        board[square%9][square//9] = '.'
    return board

class DrawingListener:
    def __init__(self) -> None:
        self.no_calls = 0
    def grid_changed_event(self, grid):
        gameState.board = grid

        if self.no_calls % 100 == 0:
            draw_grid(grid)
        self.no_calls += 1
        # get_events()

listener = DrawingListener()
g = Solution(gameState.board, listener).DFS()

def get_events():
    global g
    for event in pg.event.get():
        if event.type == pg.QUIT:sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_d:
                listener = DrawingListener()
                # solution_board = solve_board(Solution.DFS, gameState.board, listener)
                g = Solution(gameState.board, listener).DFS()
                # gameState.board = solution_board
            if event.key == pg.K_b:
                listener = DrawingListener()
                # solution_board = solve_board(Solution.BFS, gameState.board, listener)
                # gameState.board = solution_board

            if event.key == pg.K_r:
                gameState.board = copy.deepcopy(original_board)
            if event.key == pg.K_k:
                gameState.board = remove_random_squares(gameState.board)
            
            if event.key == pg.K_n:
                # for _ in range(100):
                print(next(g))

def game_loop(gameState):
    get_events()

    draw_grid(gameState.board)
    # pprint(gameState.board)
    pg.display.update()
    pg.time.delay(200)



while True:
    game_loop(gameState)


