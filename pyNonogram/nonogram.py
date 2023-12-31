#Internal imports
from .nonogram_grid import NonogramGrid

#Built-in imports
import os
from typing import Optional, Union

#External imports
import numpy as np

class Nonogram:
    """Nonogram class, used to store nonogram data.
    
    :param \**kwargs:
        See below
    
    :Keyword Arguments:
        * *path* (``str``) --
          Path to nonogram file (.non) or directory with nonogram files
    """    
    def __init__(self, **kwargs) -> None:
        """Creates a new Nonogram object.

        :raises Exception: Invalid path when path is neither file nor directory.
        """        
        self.path = None
        self.path_type = None
        if 'path' in kwargs:
            self.path = kwargs['path']
            if os.path.isfile(self.path):
                self.path_type = 'file'
            elif os.path.isdir(self.path):
                self.path_type = 'dir'
            else:
                raise Exception('Invalid path')
        
        #declare variables
        self.author = None
        self.date = None
        self.picture = None
        self.difficulty = None
        self.width = None
        self.height = None
        self.rows = None
        self.columns = None
        self.solution = None
        
        self.solved = False
        self.is_loaded = False
        
        self.grid = None
        
    def load(self, path: Optional[str] = None) -> None:
        """Loads a nonogram from a file.

        :param path: Path to nonogram file (.non)
        :type path: Optional[str]
        :raises Exception: Invalid path when path is neither file nor directory.
        :raises Exception: When path and self.path are None.
        :raises Exception: Invalid path type when path is not a file.
        :raises Exception: Invalid file format when file does not end with (.non)
        :raises Exception: Invalid file format when file does not have 9 lines.
        """        
        if path is not None:
            self.path = path
            if os.path.isfile(self.path):
                self.path_type = 'file'
            elif os.path.isdir(self.path):
                self.path_type = 'dir'
            else:
                raise Exception('Invalid path')
        
        if self.path is None:
            raise Exception('Path not specified')

        if self.path_type != 'file':
            raise Exception('Invalid path type. (Expected file got {})'.format(self.path_type))

        if not self.path.endswith('.non'):
            raise Exception('Invalid file format (Expected .non got {})'.format(self.path.split('.')[-1]))

        #reads file
        with open(self.path, 'r') as f:
            data = f.readlines()

        #checks if file has 9 lines (author, date, picture, difficulty, width, height, rows, columns, solution)
        #this is the structure of a nonogram file (.non)
        if len(data) != 9:
            raise Exception('Invalid file format')
        
        #first line: author
        self.author = data[0].split(':')[1].strip('\n')
        #second line: date
        self.date = data[1].split(':')[1].strip('\n')
        #third line: picture rating
        self.picture = int(data[2].split(':')[1].strip('\n'))
        #fourth line: difficulty
        self.difficulty = int(data[3].split(':')[1].strip('\n'))
        #fifth line: width
        self.width = int(data[4].split(':')[1].strip('\n'))
        #sixth line: height
        self.height = int(data[5].split(':')[1].strip('\n'))
        
        #seventh line: row hints
        self.rows = data[6].split(':')[1].strip('\n').split(' ')
        for idx in range(len(self.rows)):
            self.rows[idx] = self.rows[idx].split(',')
            self.rows[idx] = list(map(int, self.rows[idx]))
        
        #eighth line: column hints
        self.columns = data[7].split(':')[1].strip('\n').split(' ')
        for idx in range(len(self.columns)):
            self.columns[idx] = self.columns[idx].split(',')
            self.columns[idx] = list(map(int, self.columns[idx]))
        
        #ninth line: solution
        self.solution = data[8].split(':')[1].strip('\n')
        self.solution = list(map(''.join, zip(*[iter(self.solution)]*self.width)))
        for idx in range(len(self.solution)):
            self.solution[idx] = list(map(int, self.solution[idx]))
        #if solution is empty, set it to None
        if len(self.solution) == 0:
            self.solution = None
            self.solved = False
        
        self.is_loaded = True
        
        #load grid
        self.load_grid()
    
    def load_random(self, path: Optional[str]) -> None:
        """Loads a random nonogram from a directory.

        :param path: Path to directory with nonogram files (.non)
        :type path: Optional[str]
        :raises Exception: Invalid path when path is neither file nor directory.
        :raises Exception: When path and self.path are None.
        :raises Exception: Invalid path type when path is not a directory.
        """        
        if path is not None:
            self.path = path
            if os.path.isfile(self.path):
                self.path_type = 'file'
            elif os.path.isdir(self.path):
                self.path_type = 'dir'
            else:
                raise Exception('Invalid path')
        
        if self.path is None:
            raise Exception('Path not specified')

        if self.path_type != 'dir':
            raise Exception('Invalid path type. (Expected dir got {})'.format(self.path_type))
        
        #gets random file from directory
        files = os.listdir(self.path)
        _file = np.random.choice(files)
        
        #loads it
        self.load(os.path.join(self.path, _file))
    
    def load_grid(self) -> None:
        """Loads the nonogram grid object.

        :raises Exception: Nonogram not loaded.
        """        
        if not self.is_loaded:
            raise Exception('Nonogram not loaded')
        self.grid = NonogramGrid((self.height, self.width))
    
    def save_solution(self) -> None:
        """Saves current grid state as solution in nonogram file at self.path.
        
        :raises Exception: When path and self.path are None.
        :raises Exception: Invalid path type when path is not a file.
        :raises RuntimeError: _description_
        """
        if self.path is None:
            raise Exception('Path not specified')

        if self.path_type != 'file':
            raise Exception('Invalid path type. (Expected file got {})'.format(self.path_type))
        #iterate over grid and save solution
        self.solution = ""
        for y in range(self.height):
            for x in range(self.width):
                if self.grid.get_cell(x,y) == 0:
                    raise RuntimeError('Nonogram is not solved')
                elif self.grid.get_cell(x,y) == 1:
                    self.solution += "1"
                elif self.grid.get_cell(x,y) == -1:
                    self.solution += "0"
        if self.solved == False:
            self.solved = True
            with open(self.path, 'a') as f:
                f.write(f"{self.solution}")
    
    def load_solution(self) -> None:
        """Loads solution from nonogram file at self.path.

        :raises Exception: Nonogram not loaded.
        :raises Exception: Nonogram is not solved or has no solution.
        """        
        if not self.is_loaded:
            raise Exception('Nonogram not loaded')
        if self.solution is None or self.solved == False:
            raise Exception('Nonogram has no solution')
        #iterate over solution and load it into grid
        for y in range(self.height):
            for x in range(self.width):
                if self.solution[y][x] == 1:
                    self.grid.set_cell(x, y, 1)
                elif self.solution[y][x] == 0:
                    self.grid.set_cell(x, y, -1)
    
    def check_row(self, y: int) -> bool:
        """Checks if a row is solved.

        :param y: y coordinate of row
        :type y: int
        :return: True if row is solved, False otherwise.
        :rtype: bool
        """        
        segments = self.grid.get_row_segments(y)
        #if number of segments is not equal to number of hints, row is not solved
        if len(segments) != len(self.rows[y]):
            return False
        #if all segments are equal to their corresponding hint, row is solved
        if np.all(segments == self.rows[y]):
            return True
        #otherwise row is not solved
        return False
    
    def check_col(self, x: int) -> bool:
        """Checks if a column is solved.

        :param x: x coordinate of column
        :type x: int
        :return: True if column is solved, False otherwise.
        :rtype: bool
        """        
        segments = self.grid.get_col_segments(x)
        if len(segments) != len(self.columns[x]):
            return False
        if np.all(segments == self.columns[x]):
            return True
        return False
    
    def check_all(self) -> bool:
        """Checks if all rows and columns are solved.

        :return: True if all rows and columns are solved, False otherwise.
        :rtype: bool
        """
        #if any row or column is not solved, nonogram is not solved
        for y in range(self.height):
            res = self.check_row(y)
            if not res:
                return False
        for x in range(self.width):
            res = self.check_col(x)
            if not res:
                return False
        return True
    
    def is_solved(self) -> bool:
        """Is nonogram solved.

        :return: True if nonogram is solved, False otherwise.
        :rtype: bool
        """        
        return self.check_all()

    def print(self) -> None:
        """Prints the nonogram to the console.

        :raises Exception: Nonogram not loaded.
        """        
        if not self.is_loaded:
            raise Exception('Nonogram not loaded')
        if self.grid is None:
            self.load_grid()
        
        #get max row and column length
        max_row_len = max(list(map(len, self.rows)))
        max_col_len = max(list(map(len, self.columns)))
        
        #get spacing between columns
        col_space = len(str(np.max(list(map(np.max, self.columns)))))+1
            
        for i in range(max_col_len):
            #print empty space in left upper corner
            print('   '*max_row_len, end='')
            
            #print column hints
            i = max_col_len - i - 1
            col_str = ''
            for x in range(self.width):
                if i < len(self.columns[x]):
                    col_str += str(self.columns[x][i]).rjust(col_space)
                else:
                    col_str += ' '*col_space
            print(col_str)
        
        for y in range(self.height):
            #print row hints
            strs = list(map(lambda num: str(num).rjust(2), self.rows[y]))
            while len(strs) < max_row_len:
                strs.insert(0, '  ')
            print(' '.join(strs), end=' ')
            
            #print board
            row = self.grid.get_row(y)
            row_str = ''.join(map(str, row))
            row_str = row_str.replace('0', ' '*col_space)
            row_str = row_str.replace('-1', '-'*col_space)
            row_str = row_str.replace('1', u'\u2588'*col_space)
            
            print(row_str)

NonogramType = Union[Nonogram, object]