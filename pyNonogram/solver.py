#Internal imports
from nonogram import NonogramType

#Built-in imports
from itertools import combinations
from operator import add
from typing import List, Optional

class Solver:
    """Solver class, contains all the logic to solve a nonogram
    """    
    def __init__(self, nonogram: NonogramType) -> None:
        """Creates a new Solver object.

        :param nonogram: Nonogram class object
        :type nonogram: `NonogramType`
        """        
        self.nonogram = nonogram
    
    def generate_all_possibilities(self) -> None:
        """Generates all possible combinations of rows and columns.
        """        
        self.rows_possibilities = self._generate_all_possibilities(self.nonogram.rows, self.nonogram.width)
        self.cols_possibilities = self._generate_all_possibilities(self.nonogram.columns, self.nonogram.height)
    
    def _generate_all_possibilities(self, values: List[List[int]], size: int) -> List[List[List[int]]]:
        """Generates all possible combinations of rows or columns.

        :param values: Row or column hints
        :type values: List[List[int]]
        :param size: Length of row or column
        :type size: int
        :return: List of all possible combinations
        :rtype: List[List[List[int]]]
        """        
        
        #Combinations generation inspired by:
        #https://towardsdatascience.com/solving-nonograms-with-120-lines-of-code-a7c6e0f627e4
        
        possibilities = []
        for value in values:
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
    
    def fill_from_possibilities(self) -> None:
        """Fills the grid with known values.
        
        .. notes:: First it checks if there is only one possibility, is so it must be correct. Then it checks cell by cell if there is only one possibility for that cell. If in every possibility the cell is 1, it sets it to 1. If in every possibility the cell is -1, it sets it to -1.
        """        
        
        for y, row in enumerate(self.rows_possibilities):
            #If there is only one possibility, it must be correct
            if len(row) == 1:
                for x, cell in enumerate(row[0]):
                    self.nonogram.grid.set_cell(x, y, cell)
            elif len(row) != 0:
                #Truth table for all and none occurrences
                all_occurrences = [True]*self.nonogram.width
                none_occurrences = [True]*self.nonogram.width
                #Iterates through all possibilities and cells
                for p in row:
                    for x, cell in enumerate(p):
                        #Compares cell values and updates truth tables
                        if cell == 1:
                            none_occurrences[x] = False
                        elif cell == -1:
                            all_occurrences[x] = False
                #If in every possibility the cell is +-1, it sets it to +-1
                for i in range(len(all_occurrences)):
                    if all_occurrences[i]:
                        self.nonogram.grid.set_cell(i, y, 1)
                    elif none_occurrences[i]:
                        self.nonogram.grid.set_cell(i, y, -1)
        #Same as above, but for columns
        for x, col in enumerate(self.cols_possibilities):
            if len(col) == 1:
                for y, cell in enumerate(col[0]):
                    self.nonogram.grid.set_cell(x, y, cell)
            elif len(col) != 0:
                all_occurrences = [True]*self.nonogram.height
                none_occurrences = [True]*self.nonogram.height
                for p in col:
                    for y, cell in enumerate(p):
                        if cell == 1:
                            none_occurrences[y] = False
                        elif cell == -1:
                            all_occurrences[y] = False
                for i in range(len(all_occurrences)):
                    if all_occurrences[i]:
                        self.nonogram.grid.set_cell(x, i, 1)
                    elif none_occurrences[i]:
                        self.nonogram.grid.set_cell(x, i, -1)
    
    def remove_possibilities(self) -> None:
        """Removes possibilities that are not possible.
        
        .. notes:: Iterates through all rows and columns. If a row or column is solved, it removes all possibilities for that row or column. If a row or column is not solved, it checks if the actual row or column is possible for every possibility. If not, it removes that possibility.
        """        
        #Iterates through all rows
        for y, row in enumerate(self.rows_possibilities):
            #If a row is solved, it removes all possibilities for that row
            if self.nonogram.check_row(y):
                self.rows_possibilities[y] = []
                self.nonogram.grid.fill_row(y, -1, False)
            else:
                #If a row is not solved, it checks if the actual row is possible for every possibility
                actual = self.nonogram.grid.get_row(y)
                for p in row:
                    if not self.is_possible(actual, p):
                        self.rows_possibilities[y].remove(p)
        #Same as above, but for columns
        for x, col in enumerate(self.cols_possibilities):
            if self.nonogram.check_col(x):
                self.cols_possibilities[x] = []
                self.nonogram.grid.fill_col(x, -1, False)
            else:
                actual = self.nonogram.grid.get_col(x)
                for p in col:
                    if not self.is_possible(actual, p):
                        self.cols_possibilities[x].remove(p)
    
    def is_possible(self, actual: List[int], possibility: List[int]) -> bool:
        """Checks if a row or column is certain combination is possible.

        :param actual: row or column
        :type actual: List[int]
        :param possibility: List of possible combinations
        :type possibility: List[int]
        :return: True if possible, False if not
        :rtype: bool
        """        
        #Adds elementwise actual and the possibility.
        #As possibilities are -1 or 1 and actual -1, 0 or 1
        #when the sum is 0, it means the values had to be different,
        #thus if there is 0 in the sum it means that:
        #currently checked possibility is to be discarded.
        _sum = list(map(add, actual, possibility))
        if 0 in _sum:
            return False
        return True
    
    def fill_with_crosses(self) -> None:
        """Fill rows and columns that are solved with crosses.
        """        
        #Iterates through all rows
        for row in range(self.nonogram.height):
            #If a row is solved, it fills it with crosses withouth overwritting
            if self.nonogram.check_row(row):
                self.nonogram.grid.fill_row(row, -1, False)
        
        #Same as above, but for columns
        for col in range(self.nonogram.width):
            if self.nonogram.check_col(col):
                self.nonogram.grid.fill_col(col, -1, False)
    
    def find_full(self) -> None:
        """Fills rows and columns that are full.
        """        
        #Iterates through all row hints
        for idx, row in enumerate(self.nonogram.rows):
            #If there is only one hint and it is equal to the width of the grid
            if len(row) == 1:
                if row[0] == self.nonogram.width:
                    #Fills the row with 1
                    self.nonogram.grid.fill_row(idx, 1)
            else:
                #If there is more than one hint, it checks if the sum of hints and spaces between them 
                #is equal to the width of the grid
                if len(row)-1 + sum(row) == self.nonogram.width:
                    cursor = 0
                    #Iterates through all hints and fills the row with 1s and -1s
                    for segment in row:
                        for _ in range(segment):
                            self.nonogram.grid.set_cell(cursor, idx, 1)
                            cursor += 1
                        try:
                            self.nonogram.grid.set_cell(cursor, idx, -1)
                            cursor += 1
                        except IndexError:
                            pass
        #Same as above, but for columns
        for idx, col in enumerate(self.nonogram.columns):
            if len(col) == 1:
                if col[0] == self.nonogram.height:
                    self.nonogram.grid.fill_col(idx, 1)
            else:
                if len(col)-1 + sum(col) == self.nonogram.height:
                    cursor = 0
                    for segment in col:
                        for _ in range(segment):
                            self.nonogram.grid.set_cell(idx, cursor, 1)
                            cursor += 1
                        try:
                            self.nonogram.grid.set_cell(idx, cursor, -1)
                            cursor += 1
                        except IndexError:
                            pass
    
    def fill_middle(self) -> None:
        """Fills rows and columns that are longer than half of the grid.
        """        
        #Iterates through all row hints
        for idx, row in enumerate(self.nonogram.rows):
            #If there is only one hint and it is longer than half of the grid
            if len(row) == 1 and row[0] > self.nonogram.width/2:
                #Creates two lists of 0s, one for the left side and one for the right side
                left = [0]*self.nonogram.width
                right = [0]*self.nonogram.width
                #Populates the lists with 1s on the left and right side
                for i in range(row[0]):
                    left[i] = 1
                    right[-(i+1)] = 1
                for i in range(self.nonogram.width):
                    if left[i] == 1 and right[i] == 1:
                        #Fills the intersection of the two lists with 1s
                        self.nonogram.grid.set_cell(i, idx, 1)
                    elif self.nonogram.grid.get_cell(i, idx) == 0:
                        self.nonogram.grid.set_cell(i, idx, 0)
        #Same as above, but for columns
        for idx, col in enumerate(self.nonogram.columns):
            if len(col) == 1 and col[0] > self.nonogram.height/2:
                left = [0]*self.nonogram.height
                right = [0]*self.nonogram.height
                for i in range(col[0]):
                    left[i] = 1
                    right[-(i+1)] = 1
                for i in range(self.nonogram.height):
                    if left[i] == 1 and right[i] == 1:
                        self.nonogram.grid.set_cell(idx, i, 1)
                    elif self.nonogram.grid.get_cell(idx, i) == 0:
                        self.nonogram.grid.set_cell(idx, i, 0)
    
    def fill_edges(self) -> None:
        """Fills rows and columns that are on the edge of the grid.
        """        
        #Gets the top, bottom, left and right row and column
        top = self.nonogram.grid.get_row(0)
        bottom = self.nonogram.grid.get_row(self.nonogram.height-1)
        left = self.nonogram.grid.get_col(0)
        right = self.nonogram.grid.get_col(self.nonogram.width-1)
        
        #Treats each edge separately
        #It could be done in a loop, but this is more readable
        
        #Iterates through each cell in the top row
        for x, cell in enumerate(top):
            #If the cell is 1 and the hint is longer than 1
            if cell == 1 and self.nonogram.columns[x][0] > 1:
                y = 0
                #Iterates down in column and fills with 1s until the hint is satisfied
                for offset in range(self.nonogram.columns[x][0]):
                    self.nonogram.grid.set_cell(x,y+offset, 1)
                try:
                    if self.nonogram.grid.get_cell(x,y+self.nonogram.columns[x][0]) == 0:
                        self.nonogram.grid.set_cell(x,y+self.nonogram.columns[x][0], -1)
                #Could be catched with if statement, but this is quicker and im lazy
                except IndexError:
                    pass
                    
        for x, cell in enumerate(bottom):
            if cell == 1 and self.nonogram.columns[x][-1] > 1:
                y = self.nonogram.height-1
                for offset in range(self.nonogram.columns[x][-1]):
                    self.nonogram.grid.set_cell(x,y-offset, 1)
                try:
                    if self.nonogram.grid.get_cell(x,y-self.nonogram.columns[x][-1]) == 0:
                        self.nonogram.grid.set_cell(x,y-self.nonogram.columns[x][-1], -1)
                except IndexError:
                    pass
                    
        for y, cell in enumerate(left):
            if cell == 1 and self.nonogram.rows[y][0] > 1:
                x = 0
                for offset in range(self.nonogram.rows[y][0]):
                    self.nonogram.grid.set_cell(x+offset,y, 1)
                try:
                    if self.nonogram.grid.get_cell(x+self.nonogram.rows[y][0],y) == 0:
                        self.nonogram.grid.set_cell(x+self.nonogram.rows[y][0],y, -1)
                except IndexError:
                    pass
        
        for y, cell in enumerate(right):
            if cell == 1 and self.nonogram.rows[y][-1] > 1:
                x = self.nonogram.width-1
                for offset in range(self.nonogram.rows[y][-1]):
                    self.nonogram.grid.set_cell(x-offset,y, 1)
                try:
                    if self.nonogram.grid.get_cell(x-self.nonogram.rows[y][-1],y) == 0:
                        self.nonogram.grid.set_cell(x-self.nonogram.rows[y][-1],y, -1)
                except IndexError:
                    pass

    def run(self, limit: Optional[int] = 250) -> None:
        """Runs the solver.

        :param limit: limits the number of steps to prevent infinite loops, defaults to 250
        :type limit: Optional[int], optional
        """            
        
        counter = 0
        
        print("Generating possibilities...")
        self.generate_all_possibilities()
        
        print("Solving...")
        self.find_full()
        self.fill_middle()
        self.fill_edges()
        self.fill_with_crosses()
        #Above functions arent used in the main loop as they are deteministic and dont need to be repeated. 
        #It wouldnt change much, especially that possibilities can handle it.
        #These functions are not needed at all, however they speed up the solving process.
        #Possibilities begin slower and accelerate as the solving progresses.
        
        #removes possibilities after the deterministic functions
        self.remove_possibilities()
        
        #Enters the main loop until the nonogram is solved or the limit is reached
        while not self.nonogram.is_solved() and limit > counter:
            counter += 1
            print(f"Step {counter}")
            #Fills the grid with known values
            #Removes possibilities that are not possible
            self.fill_from_possibilities()
            self.remove_possibilities()
        if limit <= counter:
            print("Limit reached")