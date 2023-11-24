#Internal imports
from nonogram import NonogramType

#External imports
import matplotlib.pyplot as plt

class Display:
    """Display class, used to display nonogram grid data.
    """    
    def __init__(self, nonogram: NonogramType) -> None:
        """Creates a new Display object.

        :param nonogram: Nonogram class object
        :type nonogram: NonogramType
        """        
        self.nonogram = nonogram
    
    def generate(self) -> None:
        """Generates a matplotlib figure.
        """        
        self.fig = plt.figure()
        self.fig.set_size_inches(self.nonogram.width/5, self.nonogram.height/5)
        self.ax = plt.Axes(self.fig, [0., 0., 1., 1.])
        self.ax.set_axis_off()
        self.fig.add_axes(self.ax)
        plt.set_cmap('binary')
        self.ax.imshow(self.nonogram.grid)
    
    def show(self) -> None:
        """Shows the matplotlib figure.
        """        
        self.generate()
        plt.show()
    
    def save(self, path: str) -> None:
        """Saves the matplotlib figure to png.

        :param path: path to save to
        :type path: str
        """        
        self.generate()
        plt.savefig(path)