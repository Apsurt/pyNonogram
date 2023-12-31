"""
This is an example of how to use the Nonogram class to create nonogram objects and display them.
"""
from pyNonogram.nonogram import Nonogram

def main():
    nonogram = Nonogram()
    nonogram.load("examples/flower.non")
    print(nonogram.is_solved())
    nonogram.load_solution()
    print("Author: " + nonogram.author)
    print("Date: " + nonogram.date)
    print("Picture rating: " + str(nonogram.picture))
    print("Difficulty: " + str(nonogram.difficulty))
    print("Width: " + str(nonogram.width))
    print("Height: " + str(nonogram.height))
    print("Rows: " + str(nonogram.rows))
    print("Columns: " + str(nonogram.columns))
    nonogram.print()

if __name__ == "__main__":
    main()