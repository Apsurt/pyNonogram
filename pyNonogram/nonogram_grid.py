#Built-in imports
from typing import Tuple, List, Optional

#External imports
import numpy as np

class NonogramGrid(np.ndarray):
    """NonogramGrid class, used to store nonogram grid data.

    .. note:: Inherits from :class:`numpy.ndarray`
    """    
    def __new__(cls, *args, **kwargs) -> np.ndarray:
        """Creates a new NonogramGrid object.

        :return: Returns 2D array of type np.int8
        :rtype: np.ndarray
        """
        #set dtype to np.int8
        kwargs['dtype'] = np.int8
        return super().__new__(cls, *args, **kwargs)
    
    def __init__(self, shape: Tuple[int, int], *args, **kwargs) -> None:
        """Creates a new NonogramGrid object.

        :param shape: (height, width)
        :type shape: Tuple[int, int]
        """        
        args = (shape, *args)
        #initialize with zeros
        self.fill(0)
    
    def set_cell(self, x: int, y: int, value: int) -> None:
        """Sets a cell value.

        :param x: x coordinate
        :type x: int
        :param y: y coordinate
        :type y: int
        :param value: value to set (0, 1 or -1)
        :type value: int
        """
        #Swappped x and y because of numpy array indexing, y is row, x is column. Holds for all methods.
        if value not in [-1,0,1]:
            raise ValueError('Value must be -1, 0 or 1')
        self[y,x] = value
    
    def get_cell(self, x: int, y: int) -> int:
        """Returns a cell value.

        :param x: x coordinate
        :type x: int
        :param y: y coordinate
        :type y: int
        :return: cell value (0, 1 or -1)
        :rtype: int
        """        
        return self[y,x]
    
    def get_row(self, y: int) -> np.ndarray:
        """Returns cell values in a row.

        :param y: y coordinate of row
        :type y: int
        :return: row
        :rtype: np.ndarray
        """        
        return self[y]
    
    def get_col(self, x: int) -> np.ndarray:
        """Returns cell values in a column.

        :param x: x coordinate of column
        :type x: int
        :return: column
        :rtype: np.ndarray
        """        
        return self[:,x]
    
    def fill_row(self, y: int, value: int, with_overwritting: Optional[bool] = True) -> None:
        """Fills a row with a value.

        :param y: y coordinate of row
        :type y: int
        :param value: value to fill with (0, 1 or -1)
        :type value: int
        :param with_overwritting: decides if existing non-zero values should be overwritten, defaults to True
        :type with_overwritting: bool, optional
        """        
        for x in range(self.shape[1]):
            if with_overwritting or self[y,x] == 0:
                self.set_cell(x, y, value)
    
    def fill_col(self, x: int, value: int, with_overwritting: Optional[bool] = True) -> None:
        """Fills a column with a value.

        :param x: x coordinate of column
        :type x: int
        :param value: value to fill with (0, 1 or -1)
        :type value: int
        :param with_overwritting: decides if existing non-zero values should be overwritten, defaults to True
        :type with_overwritting: bool, optional
        """        
        for y in range(self.shape[0]):
            if with_overwritting or self[y,x] == 0:
                self.set_cell(x, y, value)
    
    def get_row_segments(self, y: int) -> List[int]:
        """Returns lengths of segments of 1s in a row.

        :param y: y coordinate of row
        :type y: int
        :return: Lengths of segments of 1s in a row.
        :rtype: List[int]
        """        
        row = self.get_row(y)
        #replace -1 with 0 as they are the same in this case
        row = np.maximum(row,0)
        row_str = ''.join(map(str, row))
        #splits into segments of 1s
        row_str = row_str.split('0')
        #removes empty segments
        segments = list(filter(lambda x: len(x) > 0, row_str))
        #maps segments to their lengths
        segments = list(map(len, segments))
        return segments
    
    def get_col_segments(self, x: int) -> List[int]:
        """Returns lengths of segments of 1s in a column.

        :param x: x coordinate of column
        :type x: int
        :return: Lengths of segments of 1s in a column.
        :rtype: List[int]
        """        
        col = self.get_col(x)
        col = np.maximum(col,0)
        col_str = ''.join(map(str, col))
        col_str = col_str.split('0')
        segments = list(filter(lambda x: len(x) > 0, col_str))
        segments = list(map(len, segments))
        return segments
    
    def __str__(self) -> str:
        """Returns string representation of NonogramGrid.

        :return: np.narray.__str__()
        :rtype: str
        """        
        return super().__str__()