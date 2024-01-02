from pyNonogram.nonogram import Nonogram

def main():
    nonogram = Nonogram()
    nonogram.load("examples/flower.non")
    nonogram.print()
    while not nonogram.check_all():
        x = int(input("x: "))
        y = int(input("y: "))
        value = int(input("value: "))
        nonogram.grid.set_cell(x, y, value)
        nonogram.print()
    print("Solved!")
    

if __name__ == '__main__':
    main()