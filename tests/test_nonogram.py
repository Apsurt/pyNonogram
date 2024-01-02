import pytest
import pyNonogram.nonogram as nonogram
import pyNonogram.nonogram_grid as nonogram_grid
import pyNonogram.errors as errors
import numpy as np

test_path = "tests/test_nonograms/test1.non"
invalid_test_path = "tests/test_nonograms/invalid_test.non"
dir_test_path = "tests/test_nonograms"

def test_object_init():
    nonogram_object = nonogram.Nonogram()

def test_object_init_with_path():
    nonogram_object = nonogram.Nonogram(path=test_path)
    assert nonogram_object.path == test_path and nonogram_object.path_type == "file"

def test_object_init_with_invalid_path():
    with pytest.raises(errors.PathException):
        nonogram_object = nonogram.Nonogram(path=invalid_test_path)

def test_object_init_with_dir_path():
    nonogram_object = nonogram.Nonogram(path=dir_test_path)
    assert nonogram_object.path == dir_test_path and nonogram_object.path_type == "dir"

def test_load():
    nonogram_object = nonogram.Nonogram(path=test_path)
    nonogram_object.load()

def test_load_with_path():
    nonogram_object = nonogram.Nonogram()
    nonogram_object.load(path=test_path)

def test_load_with_invalid_path():
    nonogram_object = nonogram.Nonogram()
    with pytest.raises(errors.PathException):
        nonogram_object.load(path=invalid_test_path)

def test_load_with_dir_path():
    nonogram_object = nonogram.Nonogram()
    with pytest.raises(errors.PathException):
        nonogram_object.load(path=dir_test_path)

def test_load_with_invalid_file():
    with pytest.raises(errors.PathException):
        nonogram_object = nonogram.Nonogram(path=invalid_test_path)
        nonogram_object.load()

def test_load_variables():
    nonogram_object = nonogram.Nonogram(path=test_path)
    nonogram_object.load()
    pass_test = nonogram_object.author == "Test Author" 
    assert nonogram_object.date == "2.1.24"
    assert nonogram_object.picture == 1
    assert nonogram_object.difficulty == 1
    assert nonogram_object.width == 5
    assert nonogram_object.height == 6
    assert nonogram_object.rows == [[1], [3], [2,2], [3], [1], [1]]
    assert nonogram_object.columns == [[1], [3], [2,3], [3], [1]]
    assert nonogram_object.solution == [[0,0,1,0,0], [0,1,1,1,0], [1,1,0,1,1], [0,1,1,1,0], [0,0,1,0,0], [0,0,1,0,0]]

def test_load_random():
    nonogram_object = nonogram.Nonogram()
    nonogram_object.load_random(dir_test_path)
    assert nonogram_object.author == "Test Author" or nonogram_object.author == "Test Author 2"

def test_load_solution():
    nonogram_object = nonogram.Nonogram(path=test_path)
    nonogram_object.load()
    nonogram_object.load_solution()
    nonogram_grid_object = nonogram_grid.NonogramGrid((6,5))
    nonogram_grid_object.fill(0)
    for y in range(nonogram_object.height):
        for x in range(nonogram_object.width):
            nonogram_grid_object.set_cell(x, y, 1 if nonogram_object.solution[y][x] == 1 else -1)
    assert (nonogram_object.grid == nonogram_grid_object).all()

def test_load_grid():
    nonogram_object = nonogram.Nonogram(path=test_path)
    nonogram_object.load()
    assert (nonogram_object.grid == np.zeros((6,5))).all()

def test_chcek_row():
    nonogram_object = nonogram.Nonogram(path=test_path)
    nonogram_object.load()
    nonogram_object.load_solution()
    assert nonogram_object.check_row(0) == True
    assert nonogram_object.check_row(1) == True
    assert nonogram_object.check_row(2) == True
    assert nonogram_object.check_row(3) == True
    assert nonogram_object.check_row(4) == True
    assert nonogram_object.check_row(5) == True

def test_check_col():
    nonogram_object = nonogram.Nonogram(path=test_path)
    nonogram_object.load()
    nonogram_object.load_solution()
    assert nonogram_object.check_col(0) == True
    assert nonogram_object.check_col(1) == True
    assert nonogram_object.check_col(2) == True
    assert nonogram_object.check_col(3) == True
    assert nonogram_object.check_col(4) == True

def test_check_all():
    nonogram_object = nonogram.Nonogram(path=test_path)
    nonogram_object.load()
    nonogram_object.load_solution()
    assert nonogram_object.check_all() == True

def test_is_solved():
    nonogram_object = nonogram.Nonogram(path=test_path)
    nonogram_object.load()
    nonogram_object.load_solution()
    assert nonogram_object.is_solved() == True

def test_is_solved_with_empty_grid():
    nonogram_object = nonogram.Nonogram(path=test_path)
    nonogram_object.load()
    assert nonogram_object.is_solved() == False