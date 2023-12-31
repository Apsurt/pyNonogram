"""
This is an example of how to use the Nonogram class to create nonogram objects.
It is not solved, to see how a solved example looks like, see flower.py example.
"""
from pyNonogram.nonogram import Nonogram

def main():
    nonogram = Nonogram()
    nonogram.load("examples/house.non")
    print("Author: " + nonogram.author)
    print("Date: " + nonogram.date)
    print("Picture rating: " + str(nonogram.picture))
    print("Difficulty: " + str(nonogram.difficulty))
    print("Width: " + str(nonogram.width))
    print("Height: " + str(nonogram.height))
    print("Rows: " + str(nonogram.rows))
    print("Columns: " + str(nonogram.columns))

if __name__ == "__main__":
    main()