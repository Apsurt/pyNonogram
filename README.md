# pyNonogram v1.0.0

Framework for puzzle game *Nonogram*. It was made thinking about projects that aim to solve puzzles. I wanted to create comprehensive library that would take some work of nonogram developers' shoulders.

It is my first package thus, reporting issues and pull request are more than appreciated.

## Table of Contents

- [Installation](#installation)
- [Documentation](#documentation)
- [Usage](#usage)
    - [File extension](#file-extension-non)
    - [Code example](#code-example)
- [Contributing](#contributing)
- [License](#license)

## Installation

Install with [pip](https://pypi.org/project/pyNonogram/):

```
pip install pyNonogram
```

## Documentation

The documentation is available [here](https://apsurt.github.io/pyNonogram-docs/)

## Usage

### File extension (.non)

Example .non file:

```
author:Apsurt
date:31.12.23
picture:2
difficulty:2
width:5
height:5
rows:1 3 2,2 3 1 1
columns:1 3 2,3 3 1
solution:001000111011011011100010000100
```

Note that there is no space before nor after the colon. Separate row or column hints are separated by space character, whereas hints in the same row or column are separated with coma. For row hints in sequence are from left to right, for columns from top to bottom.

### Code example

```
from pyNonogram import Nonogram

my_nonogram = Nonogram()
my_nonogram.load("house.non")

my_nonogram.grid.fill_row(2, 1)

my_nonogram.print()
```

For more elaborate examples check out [GitHub](https://github.com/Apsurt/pyNonogram/tree/main/examples)

## Contributing

All contributions are welcome. Just keep in mind agenda of this package, lightweight framework. Before creating pull request remember to run tests via:
```
python setup.py test
```


## License

This project is licensed under the [MIT License](LICENSE).