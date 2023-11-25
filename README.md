# pyNonogram

Framework for puzzle game *Nonogram*. It was made thinking about projects that aim to solve puzzles. I wanted to create comprahensive library that would take some work of nonogram developers' shoulders.

It is my first package thus, reporting issues and pull request are more than appreciated.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
    - [File extension](#file-extension-non)
    - [Code example](#code-example)
- [Contributing](#contributing)
- [License](#license)

## Installation

Install with pip:
```
pip install pyNonogram
```

## Usage

### File extension (.non)

Example .non file:
```
author:Apsurt
date:25.11.23
picture:3
difficulty:2
width:5
height:5
rows:1 3 5 1,1 1,1
columns:1 4 3 4 1
solution:
```
Note that there is no space before or after the colon. Separate row or column hints are separated by space character, whereas hints in the same row or column are separated with coma. For row hints in sequence are from left to right, for columns from top to bottom.

### Code example

```python
from pyNonogram import Nonogram

my_nonogram = Nonogram()
my_nonogram.load("house.non")

my_nonogram.grid.fill_row(2, 1)

my_nonogram.print()
```
For more elaborate examples check out [GitHub](https://github.com/Apsurt/pyNonogram/tree/main/examples)

## Contributing

TBA

## License

This project is licensed under the [MIT License](LICENSE).