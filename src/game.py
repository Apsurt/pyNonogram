import numpy as np
from nonogram import Nonogram

class Game(Nonogram):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.grid = np.zeros((self.height, self.width), dtype=int)
    
    def set_cell(self, x, y, value):
        self.grid[y,x] = value
    
    def get_cell(self, x, y):
        return self.grid[y,x]
    
    def get_row(self, y):
        return self.grid[y]
    
    def get_col(self, x):
        return self.grid[:,x]
    
    def fill_row(self, y, value, with_overwritting=True):
        for x in range(self.width):
            if with_overwritting or self.grid[y,x] == 0:
                self.set_cell(x, y, value)

    def fill_col(self, x, value, with_overwritting=True):
        for y in range(self.height):
            if with_overwritting or self.grid[y,x] == 0:
                self.set_cell(x, y, value)
    
    def get_row_segments(self, y):
        segments = [0]
        for x in range(self.width):
            if self.get_cell(x,y) == 1:
                segments[-1] += 1
            else:
                segments.append(0)
        while 0 in segments:
            segments.remove(0)
        if len(segments) == 0:
            segments = [0]
        return segments
    
    def get_col_segments(self, x):
        segments = [0]
        for y in range(self.height):
            if self.get_cell(x,y) == 1:
                segments[-1] += 1
            else:
                segments.append(0)
        while 0 in segments:
            segments.remove(0)
        if len(segments) == 0:
            segments = [0]
        return segments
    
    def get_row_segments_empty(self, y):
        segments = [0]
        for x in range(self.width):
            if self.get_cell(x,y) == 0:
                segments[-1] += 1
            else:
                segments.append(0)
        while 0 in segments:
            segments.remove(0)
        if len(segments) == 0:
            segments = [0]
        return segments

    def check_row(self, y):
        segments = self.get_row_segments(y)
        if len(segments) == len(self.rows[y]):
            for i in range(len(segments)):
                if segments[i] != self.rows[y][i]:
                    return False
            return True
        return False
    
    def check_col(self, x):
        segments = self.get_col_segments(x)
        if len(segments) == len(self.columns[x]):
            for i in range(len(segments)):
                if segments[i] != self.columns[x][i]:
                    return False
            return True
        return False
    
    def check_all(self):
        results = []
        for y in range(self.height):
            results.append(self.check_row(y))
        for x in range(self.width):
            results.append(self.check_col(x))
        for line in results:
            if line != True:
                return False
        return True
    
    def is_solved(self):
        return self.check_all()
    
    def save_solution(self):
        self.solution = ""
        for y in range(self.height):
            for x in range(self.width):
                if self.get_cell(x,y) == 0:
                    raise RuntimeError('Nonogram is not solved')
                elif self.get_cell(x,y) == 1:
                    self.solution += "1"
                elif self.get_cell(x,y) == -1:
                    self.solution += "0"
        if self.solved == False:
            self.solved = True
            with open(self.path, 'a') as f:
                f.write(f"{self.solution}")
    
    def check_row_error(self, y):
        segments = self.get_row_segments(y)
        if segments == [0]:
            return False
        if sum(segments) > sum(self.rows[y]):
            return True
        for seg in segments:
            if seg > max(self.rows[y]):
                return True
        return False
    
    def check_col_error(self, x):
        segments = self.get_col_segments(x)
        if segments == [0]:
            return False
        if sum(segments) > sum(self.columns[x]):
            return True
        for seg in segments:
            if seg > max(self.columns[x]):
                return True
        return False
    
    def check_error(self):
        results = []
        for y in range(self.height):
            results.append(self.check_row_error(y))
        for x in range(self.width):
            results.append(self.check_col_error(x))
        if True in results:
            return True
        return False
    
    def biggest_empty_in_row(self, y):
        biggest = 0
        current = 0
        s_idx = -1
        for x in range(self.width):
            if self.get_cell(x,y) in [0,1]:
                current += 1
                if s_idx == -1:
                    s_idx = x
            else:
                if current > biggest:
                    biggest = current
                else:
                    s_idx = -1
                current = 0
        print(biggest, s_idx)

    def __str__(self) -> str:
        result = ''
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == 1:
                    result += u'\u2588'*2
                elif self.grid[y][x] == -1:
                    result += 'XX'
                else:
                    result += '--'
            result += '\n'
        return result[:-1]

def main():
    pass

if __name__ == "__main__":
    main()