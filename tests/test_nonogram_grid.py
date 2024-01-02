import pytest
import numpy as np
import pyNonogram.nonogram_grid as nonogram_grid

shape = (5,5)

def test_object_init():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape)

def test_object_init_no_shape():
    with pytest.raises(TypeError):
        nonogram_grid_object = nonogram_grid.NonogramGrid()

def test_object_init_values():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape)
    assert np.all(nonogram_grid_object == 0)

def test_dtype():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape)
    assert nonogram_grid_object.dtype == np.int8

def test_dtype_override():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape, dtype=np.int16)
    assert nonogram_grid_object.dtype == np.int8

def test_fill():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape)
    nonogram_grid_object.fill(1)
    assert np.all(nonogram_grid_object == 1)

def test_set_cell():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape)
    nonogram_grid_object.set_cell(0,0,1)
    assert nonogram_grid_object[0,0] == 1

def test_set_cell_invalid_value():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape)
    with pytest.raises(ValueError):
        nonogram_grid_object.set_cell(0,0,2)

def test_get_cell():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape)
    nonogram_grid_object.set_cell(0,0,1)
    assert nonogram_grid_object.get_cell(0,0) == 1

def test_get_cell_invalid_index():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape)
    with pytest.raises(IndexError):
        nonogram_grid_object.get_cell(20,0)

def test_get_row():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape)
    nonogram_grid_object.set_cell(0,0,1)
    assert np.all(nonogram_grid_object.get_row(0) == [1,0,0,0,0])

def test_get_row_invalid_index():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape)
    with pytest.raises(IndexError):
        nonogram_grid_object.get_row(20)

def test_get_col():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape)
    nonogram_grid_object.set_cell(0,0,1)
    assert np.all(nonogram_grid_object.get_col(0) == [1,0,0,0,0])

def test_get_col_invalid_index():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape)
    with pytest.raises(IndexError):
        nonogram_grid_object.get_col(20)

def test_fill_row():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape)
    nonogram_grid_object.fill_row(0,1)
    assert np.all(nonogram_grid_object.get_row(0) == [1,1,1,1,1])

def test_fill_row_invalid_index():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape)
    with pytest.raises(IndexError):
        nonogram_grid_object.fill_row(20,1)

def test_fill_row_invalid_value():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape)
    with pytest.raises(ValueError):
        nonogram_grid_object.fill_row(0,2)

def test_fill_col():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape)
    nonogram_grid_object.fill_col(0,1)
    assert np.all(nonogram_grid_object.get_col(0) == [1,1,1,1,1])

def test_fill_col_invalid_index():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape)
    with pytest.raises(IndexError):
        nonogram_grid_object.fill_col(20,1)

def test_fill_col_invalid_value():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape)
    with pytest.raises(ValueError):
        nonogram_grid_object.fill_col(0,2)

def test_get_row_segments():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape)
    nonogram_grid_object.fill_row(0,1)
    assert np.all(nonogram_grid_object.get_row_segments(0) == [5])

def test_get_row_segments_multiple():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape)
    nonogram_grid_object.fill_row(0,1)
    nonogram_grid_object.fill_row(1,1)
    assert np.all(nonogram_grid_object.get_row_segments(0) == [5])
    assert np.all(nonogram_grid_object.get_row_segments(1) == [5])

def test_get_row_segments_multiple_2():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape)
    nonogram_grid_object.fill_row(0,1)
    nonogram_grid_object.set_cell(2,0,0)
    assert np.all(nonogram_grid_object.get_row_segments(0) == [2,2])

def test_get_row_segments_empty():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape)
    assert np.all(nonogram_grid_object.get_row_segments(0) == [])

def test_get_row_segments_invalid_index():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape)
    with pytest.raises(IndexError):
        nonogram_grid_object.get_row_segments(20)

def test_get_col_segments():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape)
    nonogram_grid_object.fill_col(0,1)
    assert np.all(nonogram_grid_object.get_col_segments(0) == [5])

def test_get_col_segments_multiple():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape)
    nonogram_grid_object.fill_col(0,1)
    nonogram_grid_object.fill_col(1,1)
    assert np.all(nonogram_grid_object.get_col_segments(0) == [5])
    assert np.all(nonogram_grid_object.get_col_segments(1) == [5])

def test_get_col_segments_multiple_2():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape)
    nonogram_grid_object.fill_col(0,1)
    nonogram_grid_object.set_cell(0,2,0)
    assert np.all(nonogram_grid_object.get_col_segments(0) == [2,2])

def test_get_col_segments_empty():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape)
    assert np.all(nonogram_grid_object.get_col_segments(0) == [])

def test_get_col_segments_invalid_index():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape)
    with pytest.raises(IndexError):
        nonogram_grid_object.get_col_segments(20)

def test_both_get_segments():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape)
    nonogram_grid_object.fill_row(2,1)
    nonogram_grid_object.fill_col(2,1)
    nonogram_grid_object.set_cell(2,2,0)
    assert np.all(nonogram_grid_object.get_row_segments(2) == [2,2])
    assert np.all(nonogram_grid_object.get_col_segments(2) == [2,2])

def test_str():
    nonogram_grid_object = nonogram_grid.NonogramGrid(shape)
    assert str(nonogram_grid_object) == np.zeros(shape, dtype=np.int8).__str__()