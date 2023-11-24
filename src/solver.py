from itertools import combinations
from operator import add
import torch

class Solver:
    def __init__(self, game, **kwargs) -> None:
        self.game = game
        self.init_kwargs(**kwargs)
        self.init_pytorch()
    
    def init_kwargs(self, **kwargs):
        if "warnings" in kwargs:
            self.warnings = kwargs["warnings"]
        else:
            self.warnings = True
        if "gpu_enabled" in kwargs:
            self.gpu_enabled = kwargs["gpu_enabled"]
            if self.warnings:
                if self.game.width * self.game.height < 1000:
                    raise Warning("GPU is not recommended for small puzzles")
        else:
            self.gpu_enabled = False
    
    def init_pytorch(self):
        if torch.cuda.is_available() and self.gpu_enabled:
            self.device = torch.device("cuda")
        elif torch.backends.mps.is_available() and torch.backends.mps.is_built() and self.gpu_enabled:
            self.device = torch.device("mps")
        else:
            self.device = torch.device("cpu")
    
    def generate_all_possibilities(self):
        if self.gpu_enabled:
            self.rows_possibilities = self._generate_all_possibilities(self.game.rows, self.game.width)
            for idx, row in enumerate(self.rows_possibilities):
                self.rows_possibilities[idx] = torch.tensor(row).to(self.device)
            self.cols_possibilities = self._generate_all_possibilities(self.game.columns, self.game.height)
            for idx, col in enumerate(self.cols_possibilities):
                self.cols_possibilities[idx] = torch.tensor(col).to(self.device)
        else:
            self.rows_possibilities = self._generate_all_possibilities(self.game.rows, self.game.width)
            self.cols_possibilities = self._generate_all_possibilities(self.game.columns, self.game.height)
    
    def _generate_all_possibilities_wrapper(self, func):
        pass
    
    def _generate_all_possibilities(self, values, size):
        possibilities = []
        max_step = self.game.width+self.game.height
        for idx, value in enumerate(values):
            possibilities.append([])
            ones = [[1]*x for x in value]
            n_groups = len(value)
            n_empty = size - sum(value) - (n_groups-1)
            opts = combinations(range(n_groups+n_empty), n_groups)
            for opt in opts:
                selected = [-1]*(n_groups+n_empty)
                ones_idx = 0
                for val in opt:
                    selected[val] = ones_idx
                    ones_idx += 1
                res_opt = [ones[val]+[-1] if val > -1 else [-1] for val in selected]
                res_opt = [item for sublist in res_opt for item in sublist][:-1]
                possibilities[-1].append(res_opt)
        return possibilities
    
    def fill_from_possibilities(self):
        for y, row in enumerate(self.rows_possibilities):
            if len(row) == 1:
                for x, cell in enumerate(row[0]):
                    self.game.set_cell(x, y, cell)
            elif len(row) != 0:
                all_occurrences = [True]*self.game.width
                none_occurrences = [True]*self.game.width
                for p in row:
                    for x, cell in enumerate(p):
                        if cell == 1:
                            none_occurrences[x] = False
                        elif cell == -1:
                            all_occurrences[x] = False
                for i in range(len(all_occurrences)):
                    if all_occurrences[i]:
                        self.game.set_cell(i, y, 1)
                    elif none_occurrences[i]:
                        self.game.set_cell(i, y, -1)
        for x, col in enumerate(self.cols_possibilities):
            if len(col) == 1:
                for y, cell in enumerate(col[0]):
                    self.game.set_cell(x, y, cell)
            elif len(col) != 0:
                all_occurrences = [True]*self.game.height
                none_occurrences = [True]*self.game.height
                for p in col:
                    for y, cell in enumerate(p):
                        if cell == 1:
                            none_occurrences[y] = False
                        elif cell == -1:
                            all_occurrences[y] = False
                for i in range(len(all_occurrences)):
                    if all_occurrences[i]:
                        self.game.set_cell(x, i, 1)
                    elif none_occurrences[i]:
                        self.game.set_cell(x, i, -1)
    
    def is_possible(self, actual, possibility):
        _sum = list(map(add, actual, possibility))
        if 0 in _sum:
            return False
        return True
    
    def _remove_possibilities(self):
        for y, row in enumerate(self.rows_possibilities):
            if self.game.check_row(y):
                self.rows_possibilities[y] = []
                self.game.fill_row(y, -1, False)
            else:
                actual = self.game.get_row(y)
                for p in row:
                    if not self.is_possible(actual, p):
                        self.rows_possibilities[y].remove(p)
        for x, col in enumerate(self.cols_possibilities):
            if self.game.check_col(x):
                self.cols_possibilities[x] = []
                self.game.fill_col(x, -1, False)
            else:
                actual = self.game.get_col(x)
                for p in col:
                    if not self.is_possible(actual, p):
                        self.cols_possibilities[x].remove(p)
    
    def is_possible_gpu(self, actual, possibilities):
        pass
    
    def _remove_possibilities_gpu(self):
        pass
        #rows
        actual_rows = torch.tensor(self.game.grid).to(self.device)
        print(actual_rows)
        print(self.rows_possibilities)
        #cols
        actual_cols = torch.tensor(self.game.grid.T).to(self.device)

    def remove_possibilities(self):
        if self.gpu_enabled:
            self._remove_possibilities_gpu()
        else:
            self._remove_possibilities()
    
    def fill_with_crosses(self):
        for row in range(self.game.height):
            if self.game.check_row(row):
                self.game.fill_row(row, -1, False)
            
        for col in range(self.game.width):
            if self.game.check_col(col):
                self.game.fill_col(col, -1, False)
    
    def find_full(self):
        for idx, row in enumerate(self.game.rows):
            if len(row) == 1:
                if row[0] == self.game.width:
                    self.game.fill_row(idx, 1)
            else:
                if len(row)-1 + sum(row) == self.game.width:
                    cursor = 0
                    for segment in row:
                        for cell in range(segment):
                            self.game.set_cell(cursor, idx, 1)
                            cursor += 1
                        try:
                            self.game.set_cell(cursor, idx, -1)
                            cursor += 1
                        except IndexError:
                            pass
        for idx, col in enumerate(self.game.columns):
            if len(col) == 1:
                if col[0] == self.game.height:
                    self.game.fill_col(idx, 1)
            else:
                if len(col)-1 + sum(col) == self.game.height:
                    cursor = 0
                    for segment in col:
                        for cell in range(segment):
                            self.game.set_cell(idx, cursor, 1)
                            cursor += 1
                        try:
                            self.game.set_cell(idx, cursor, -1)
                            cursor += 1
                        except IndexError:
                            pass
    
    def fill_middle(self):
        for idx, row in enumerate(self.game.rows):
            if len(row) == 1 and row[0] > self.game.width/2:
                left = [0]*self.game.width
                right = [0]*self.game.width
                for i in range(row[0]):
                    left[i] = 1
                    right[-(i+1)] = 1
                for i in range(self.game.width):
                    if left[i] == 1 and right[i] == 1:
                        self.game.set_cell(i, idx, 1)
                    elif self.game.get_cell(i, idx) == 0:
                        self.game.set_cell(i, idx, 0)
        for idx, col in enumerate(self.game.columns):
            if len(col) == 1 and col[0] > self.game.height/2:
                left = [0]*self.game.height
                right = [0]*self.game.height
                for i in range(col[0]):
                    left[i] = 1
                    right[-(i+1)] = 1
                for i in range(self.game.height):
                    if left[i] == 1 and right[i] == 1:
                        self.game.set_cell(idx, i, 1)
                    elif self.game.get_cell(idx, i) == 0:
                        self.game.set_cell(idx, i, 0)
    
    def fill_edges(self):
        top = self.game.get_row(0)
        bottom = self.game.get_row(self.game.height-1)
        left = self.game.get_col(0)
        right = self.game.get_col(self.game.width-1)
        for x, cell in enumerate(top):
            if cell == 1 and self.game.columns[x][0] > 1:
                y = 0
                for offset in range(self.game.columns[x][0]):
                    self.game.set_cell(x,y+offset, 1)
                try:
                    if self.game.get_cell(x,y+self.game.columns[x][0]) == 0:
                        self.game.set_cell(x,y+self.game.columns[x][0], -1)
                except:
                    pass
                    
        for x, cell in enumerate(bottom):
            if cell == 1 and self.game.columns[x][-1] > 1:
                y = self.game.height-1
                for offset in range(self.game.columns[x][-1]):
                    self.game.set_cell(x,y-offset, 1)
                try:
                    if self.game.get_cell(x,y-self.game.columns[x][-1]) == 0:
                        self.game.set_cell(x,y-self.game.columns[x][-1], -1)
                except:
                    pass
                    
        for y, cell in enumerate(left):
            if cell == 1 and self.game.rows[y][0] > 1:
                x = 0
                for offset in range(self.game.rows[y][0]):
                    self.game.set_cell(x+offset,y, 1)
                try:
                    if self.game.get_cell(x+self.game.rows[y][0],y) == 0:
                        self.game.set_cell(x+self.game.rows[y][0],y, -1)
                except:
                    pass
        
        for y, cell in enumerate(right):
            if cell == 1 and self.game.rows[y][-1] > 1:
                x = self.game.width-1
                for offset in range(self.game.rows[y][-1]):
                    self.game.set_cell(x-offset,y, 1)
                try:
                    if self.game.get_cell(x-self.game.rows[y][-1],y) == 0:
                        self.game.set_cell(x-self.game.rows[y][-1],y, -1)
                except:
                    pass

    def run(self):
        print("Generating possibilities...")
        self.generate_all_possibilities()
        limit = 1000
        counter = 0
        print("Solving...")
        self.find_full()
        self.fill_middle()
        self.fill_edges()
        self.fill_with_crosses()
        self.remove_possibilities()
        while not self.game.is_solved() and limit > counter:
            counter += 1
            print(f"Step {counter}")
            self.fill_from_possibilities()
            self.remove_possibilities()
        if limit <= counter:
            print("Limit reached")

if __name__ == "__main__":
    from game import Game
    def main():
        game = Game(path="src/nonograms/test.non")
        solver = Solver(game, gpu_enabled=True, warnings=False)
        solver.generate_all_possibilities()
        solver._remove_possibilities_gpu()
    
    main()