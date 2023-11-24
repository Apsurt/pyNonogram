class Nonogram:
    def __init__(self, **kwargs) -> None:
        self.init_vars()
        self.path = None
        
        if 'path' in kwargs:
            self.path = kwargs['path']
            self.load(self.path)
    
    def init_vars(self) -> None:
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
    
    def load(self, path: str) -> None:
        with open(path, 'r') as f:
            data = f.readlines()
        if len(data) != 9:
            raise Exception('Invalid file format')
        
        self.author = data[0].split(':')[1].strip('\n')
        self.date = data[1].split(':')[1].strip('\n')
        self.picture = int(data[2].split(':')[1].strip('\n'))
        self.difficulty = int(data[3].split(':')[1].strip('\n'))
        self.width = int(data[4].split(':')[1].strip('\n'))
        self.height = int(data[5].split(':')[1].strip('\n'))

        self.rows = data[6].split(':')[1].strip('\n').split(' ')
        for idx in range(len(self.rows)):
            self.rows[idx] = self.rows[idx].split(',')
            self.rows[idx] = list(map(int, self.rows[idx]))

        self.columns = data[7].split(':')[1].strip('\n').split(' ')
        for idx in range(len(self.columns)):
            self.columns[idx] = self.columns[idx].split(',')
            self.columns[idx] = list(map(int, self.columns[idx]))

        self.solution = data[8].split(':')[1].strip('\n')
        self.solution = list(map(''.join, zip(*[iter(self.solution)]*self.width)))
        for idx in range(len(self.solution)):
            self.solution[idx] = list(map(int, self.solution[idx]))
        if len(self.solution) == 0:
            self.solution = None
            self.solved = False
    
    def load_random(self, size: int) -> None:
        pass
    
    def print_solution(self) -> str:
        if self.solution is None:
            raise RuntimeError('Nonogram is not solved')
        result = ''
        for y in range(self.height):
            for x in range(self.width):
                result += u"\u2588"*2 if self.solution[y][x] == 1 else '  '
            result += '\n'
        print(result[:-1])

def main():
    non = Nonogram(path='src/nonograms/67723.non')
    print(non.author)
    print(non.date)
    print(non.picture)
    print(non.difficulty)
    print(non.width)
    print(non.height)
    print(non.rows)
    print(non.columns)
    print(non.solved)
    if non.solved:
        print(non.solution)

if __name__ == '__main__':
    main()
