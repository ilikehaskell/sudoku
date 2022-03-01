from pprint import pprint
from typing import Any, List
from collections import defaultdict, deque
import json

def cross(A,B):
  return [(a,b) for a in A for b in B]
squares = [(row, col) for row in range(9) for col in range(9)]
digits = '123456789'
# cols = [  [(0,0), (1,0), (2,0) … ],  [(0,1), (1, 1) …]  ]
cols = [cross(range(9),[c]) for c in range(9)]
rows = [cross([r], range(9)) for r in range(9)]
box_idxs = [[0,1,2],[3,4,5],[6,7,8]]
boxes = [ cross(row_idxs, col_idxs) for row_idxs in box_idxs for col_idxs in box_idxs]
unit_list = rows+cols+boxes
units = { s:[u for u in unit_list if s in u] for s in squares}
peers = {s:set(sum(units[s],[]))-set([s]) for s in squares}

class Solution:
  def __init__(self, board: List[List[str]], lisener) -> None:
    self.lisener = lisener
    self.board = board

  def get_value(self, square, board):
    i, j = square
    return board[i][j]
  
  def set_value(self, value, square, board):
    i,j = square
    board[i][j] = value
    if self.lisener:
      self.lisener.grid_changed_event(board)

  def DFS(self) -> None:
      def search(board, square_ord, found  = False):
        if square_ord == 81:
          return True
        square = (square_ord//9, square_ord%9)
        if self.get_value(square, board) != '.':
          return search(board, square_ord+1)
        for d in digits:
          if d not in [self.get_value(p, board) for p in peers[square]]:
              self.set_value(d, square, board)
              found = search(board, square_ord+1)
              if found:
                return True
              self.set_value('.', square, board)

      search(self.board, 0)

  def BFS(self) -> Any:
    frontier = deque([json.dumps(self.board)])
    explored = set()
    while frontier:
      node_state = frontier.popleft()
      explored.add(node_state)
      node = json.loads(node_state)

      for square_ord in range(81):
        square = (square_ord//9, square_ord%9)
        if self.get_value(square, node) != '.':
          continue
        for d in digits:
          if d not in [self.get_value(p, node) for p in peers[square]]:
              self.set_value(d, square, node)
              child_state = json.dumps(node)
              if child_state not in explored and child_state not in frontier:
                if test_if_solved(child_state):
                  self.board = node
                  return True
                frontier.append(child_state)
              self.set_value('.', square, node)
              
def test_if_solved(grid):
  if grid.find('.') != -1:
    return False
  return True


class CountingLisener:
    def __init__(self) -> None:
        self.no_calls = 0
    def grid_changed_event(self, grid):
        self.no_calls += 1

def solve_board(method, board, listener = None):
    print(f"Board is missing {str(board).count('.')} values")
    if listener is None:
      listener = CountingLisener()
    solution = Solution(board, listener)
    method(solution)
    pprint(solution.board)
    print(f'Solved in {listener.no_calls} steps with {method.__name__}!\n\n')
    return solution.board

if __name__ == '__main__':
  hard_board = [[".",".",".","7","4","8",".",".","."],["7",".",".",".",".",".",".",".","."],[".","2",".","1",".","9",".",".","."],[".",".","7",".",".",".","2","4","."],[".","6","4",".","1",".","5","9","."],[".","9","8",".",".",".","3",".","."],[".",".",".","8",".","3",".","2","."],[".",".",".",".",".",".",".",".","6"],[".",".",".","2","7","5","9",".","."]]
  easy_board = [['.', '.', '.', '.', '4', '8', '6', '3', '2'], ['.', '.', '3', '6', '5', '2', '.', '1', '9'], ['4', '2', '6', '1', '3', '9', '8', '7', '5'], ['3', '5', '7', '9', '8', '6', '2', '4', '1'], ['2', '6', '4', '3', '1', '7', '5', '9', '8'], ['1', '9', '8', '5', '2', '4', '3', '6', '7'], ['9', '7', '5', '8', '6', '3', '1', '2', '4'], ['8', '3', '2', '4', '9', '1', '7', '5', '6'], ['6', '4', '1', '2', '7', '5', '9', '8', '3']]
  solve_board(Solution.DFS, hard_board)
  solve_board(Solution.BFS, easy_board)
  solve_board(Solution.DFS, easy_board)

  