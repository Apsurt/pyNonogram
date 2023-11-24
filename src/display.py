import matplotlib.pyplot as plt

class Display:
    def __init__(self, game):
        self.game = game
    
    def generate(self):
        self.fig = plt.figure()
        self.fig.set_size_inches(self.game.width/5, self.game.height/5)
        self.ax = plt.Axes(self.fig, [0., 0., 1., 1.])
        self.ax.set_axis_off()
        self.fig.add_axes(self.ax)
        plt.set_cmap('binary')
        self.ax.imshow(self.game.grid)
    
    def show(self):
        self.generate()
        plt.show()
    
    def save(self, path):
        self.generate()
        plt.savefig(path)