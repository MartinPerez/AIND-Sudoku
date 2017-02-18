import itertools
from collections import Counter

digits = '123456789'
rows = 'ABCDEFGHI'
cols = '123456789'
square_cols = ('123', '456', '789')
square_rows = ('ABC', 'DEF', 'GHI')


def _cross(A, B):
    """Cross product of elements in A and elements in B."""
    return [s + t for s in A for t in B]


boxes = _cross(rows, cols)
row_units = [_cross(r, cols) for r in rows]
column_units = [_cross(rows, c) for c in cols]
square_units = [_cross(rs, cs) for rs in square_rows for cs in square_cols]
diagonal_units = [[r + c for r, c in zip(rows, cols)]]
diagonal_units += [[r + c for r, c in zip(rows, reversed(cols))]]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(itertools.chain(*units['A1'])) - set([s])) for s in boxes)

assignments = []


def _assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def boxes_with_n_values(values, n, unit=None):
    """Get boxes with n possible values

    Parameters
    ----------
    values : dict,
        sudoku in dictionary form
    n : int,
        number of possible values

    Returns
    -------
    boxes : list of str,
        boxes that contain exactly n possible values
    """
    if unit is None:
        unit = values
    boxes = [box for box in unit if len(values[box]) == n]
    return boxes


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.

    Parameters
    ----------
    grid : str,
        A grid in string form.

    Returns
    -------
    grid_dict :  dict with str as Key and str as Value,
        A grid in dictionary form. Keys are the boxes, e.g., 'A1'.
        Values are the value in each box, e.g., '8'.
        If a box has no value, then its value will be set to '123456789'.
    """
    chars = []
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    grid_dict = dict(zip(boxes, chars))
    return grid_dict


def display(values):
    """
    Display the values as a 2-D grid.

    Parameters
    ----------
    values : dict
        The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF':
            print(line)
    print


def identical_siblings(values, n):
    """Eliminate values using the identical_siblings strategy.
    When n boxes in a unit contain only the same n possible digits.
    Then we eliminate those n digits from all other boxes in that unit.

    Parameters
    ----------
    values : dict,
        Input sudoku in dictionary form.
    n : int,
        length of identical values

    Returns
    -------
    values: dict,
        Resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        boxes_with_n = boxes_with_n_values(values, n, unit)
        n_values = [values[box] for box in boxes_with_n]
        for v in [v for v in set(n_values) if n_values.count(v) == n]:
            non_siblings = [box for box in unit if v != values[box]]
            for digit in v:
                for box in [b for b in non_siblings if digit in values[b]]:
                    new_value = values[box].replace(digit, '')
                    _assign_value(values, box, new_value)
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    When two boxes in a unit contain only the same two possible digits.
    Then we eliminate those two digits from all other boxes in that unit.

    Parameters
    ----------
    values : dict,
        Input sudoku in dictionary form.

    Returns
    -------
    values: dict,
        Resulting sudoku in dictionary form.
    """
    values = identical_siblings(values, 2)
    return values


def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with only one value,
    eliminate this value from the values of all its peers.

    Parameters
    ----------
    values : dict,
        Input sudoku in dictionary form.

    Returns
    -------
    values: dict,
        Resulting sudoku in dictionary form.
    """
    values = identical_siblings(values, 1)
    return values


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Parameters
    ----------
    values : dict,
        Input sudoku in dictionary form.

    Returns
    -------
    values: dict,
        Resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        # A digit must appear only once in the unit
        # only_one will contain the only box that contains the digit
        # Every digit must appear at least once in the unit
        only_one = dict([(digit, '') for digit in digits])
        for box in unit:
            for digit in values[box]:
                # Digit was discarded already if two boxes contained it
                if digit in only_one:
                    if only_one[digit] == '':
                        only_one[digit] = box
                    else:
                        # Eliminate digit if one box had it
                        del only_one[digit]
        for digit in only_one:
            # We do not rewrite box values that have already unique digit
            try:
                if len(values[only_one[digit]]) > 1:
                    _assign_value(values, only_one[digit], digit)
            except:
                print(unit)
                print([values[box] for box in unit])
                print(only_one)
                raise Exception()

    return values


def reduce_puzzle(values):
    """
    Iterate diverse strategies. If at some point, there is a box
    with no available values, return False. If the sudoku is solved, return
    the sudoku. If after an iteration of both functions, the sudoku remains
    the same, return the sudoku. Current strategies employed are:
    elimination, chains and only_choice.

    Parameters
    ----------
    values : dict,
        Input sudoku in dictionary form.

    Returns
    -------
    values: dict,
        Reduced sudoku in dictionary form. (values modified in place)
    """
    stalled = False
    while not stalled:
        solved_values_before = len(boxes_with_n_values(values, 1))
        for n_val in range(4):
            values = identical_siblings(values, n_val)
        values = only_choice(values)
        solved_values_after = len(boxes_with_n_values(values, 1))
        stalled = solved_values_before == solved_values_after
        if len(boxes_with_n_values(values, 0)):
            return False
    return values


def search(values):
    """Using depth-first search and propagation, create a search tree to
    solve the sudoku.

    Parameters
    ----------
    values : dict,
        Input sudoku in dictionary form.

    Returns
    -------
    new_values: dict,
        Solved sudoku in dictionary form.
    """
    # First, reduce the puzzle
    values = reduce_puzzle(values)
    # If reduction leads to a dead end we return False
    if not values:
        return False
    # Choose one of the unfilled squares with the fewest possibilities
    fewest = (float('inf'), '')
    for box in values:
        n_pos = len(values[box])
        if n_pos > 1 and n_pos < fewest[0]:
            fewest = (n_pos, box)
            if n_pos == 2:
                break
    # if we dont find any box with more than 1 value we solved the sudoku!
    if fewest[0] == float('inf'):
        return values
    # Create new possible sudokus from the box values. if one of them is
    # solved we return the resulting sudoku.
    for digit in values[fewest[1]]:
        new_values = dict(values)
        new_values[fewest[1]] = digit
        new_values = search(new_values)
        if new_values:
            return new_values
    # If no solution found after trying all posibilities we return False
    return False


def solve(grid):
    """
    Find the solution to a Sudoku grid.

    Parameters
    ----------
        grid : string,
            A string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4.
            ..4....8....52.............3'
    Returns
    -------
        solution : dict or False,
        The dictionary representation of the final sudoku grid if a solution
        is found. Otherwise False.
    """
    # get grid in dictionary form
    values = grid_values(grid)
    # search solution
    solution = search(values)
    return solution


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except NameError:  # Closing the pygame screen on linux gives this error
        pass
    except Exception as ex:
        print(type(ex).__name__)
        print('We could not visualize your board due to a pygame issue.'
              ' Not a problem! It is not a requirement.')
