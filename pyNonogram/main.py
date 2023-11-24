import os

from scraper import Scraper
from game import Game
from solver import Solver
from display import Display

def list_all_files(dir) -> list:
    return os.listdir(dir)

def main():
    numbers = [67778]
    
    for number in numbers:
        url = f"https://www.nonograms.org/nonograms/i/{number}"
        path = f"src/nonograms/{number}.non"

        if not os.path.exists("src/nonograms"):
            os.mkdir("src/nonograms")

        if not os.path.isfile(f"src/nonograms/{number}.non"):
            sc = Scraper("page", url)
            sc.export(path)

        game = Game(path=path)
        solver = Solver(game)
        solver.run()
        game.save_solution()
        print(game)
        #display = Display(game)
        #display.show()
        #display.save(f"src/pictures/{number}.png")

if __name__ == "__main__":
    main()