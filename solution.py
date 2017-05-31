# All Questions appear in comments appended with 'Question -'


#  Question - visualization doesn't seem to work at all, I dont even get a popup window. is that an install issue or a code error?
#  Question - python solution.py gives me the error seen in forum post #222074- this seems to indicate it is NOT problematic since I built
#       my code to solve ANY puzzle (or tried to at least), but I'm still not passing any of the tests...??
    # https://discussions.udacity.com/t/is-the-goal-of-the-project-to-solve-any-sudokus-or-only-diagonal-sudokus/241399

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    naked_pairs = []
    naked_pair_values = []
    for key in values.keys():
        if len(values[key]) == 2:
            # Check for naked pair
            for twin in peers[key]:
                if values[key] == values[twin]:
                    # print('found a naked pair:')
                    # print(values[key])
                    # print(values[twin])
                    # print(key)
                    # print(twin)
                    # Means we have found a naked pair
                    # Now remove those numbers from all other peers of (key) and (peer)
                    if [key, twin] in naked_pairs or [twin, key] in naked_pairs:
                        print('duplicate')
                    else: 
                        first_num = values[key][0]
                        second_num = values[key][1]
                        naked_pairs.append([key, twin])
                        naked_pair_values.append([first_num, second_num])
                    # print(naked_pairs)
                    # print(naked_pair_values)
                    # print(len(naked_pairs))
    # print(naked_pairs)
    # print(naked_pair_values)

    # Now go through COLLECTIVE peers of BOTH twins
    # Extremely suboptimal but trying to get concept down first

    # def intersect(a, b):
    #     """ return the intersection of two lists """
    #     return list(set(a) & set(b))


    for i in range(0, len(naked_pairs)):
        for peer in peers[naked_pairs[i][0]]:
            if peer in peers[naked_pairs[i][1]] and peer != naked_pairs[i][1]:
                assign_value(values, peer, values[peer].replace(naked_pair_values[i][0], ''))
                # print(values[peer])
                assign_value(values, peer, values[peer].replace(naked_pair_values[i][1], ''))
        for peer in peers[naked_pairs[i][1]]:
            if peer in peers[naked_pairs[i][0]] and peer != naked_pairs[i][0]:
                assign_value(values, peer, values[peer].replace(naked_pair_values[i][0], ''))
                assign_value(values, peer, values[peer].replace(naked_pair_values[i][1], ''))

    # for i in range(0, len(naked_pairs)):
    #     for peer in peers[naked_pairs[i][0]]:
    #         if peer != naked_pairs[i][1]:
    #             # check(peer, values, 'naked')
    #             # print(peer)
    #             # print(values[peer])
    #             assign_value(values, peer, values[peer].replace(naked_pair_values[i][0], ''))
    #             # print(values[peer])
    #             assign_value(values, peer, values[peer].replace(naked_pair_values[i][1], ''))
    #             # print(values[peer])
    #     for peer in peers[naked_pairs[i][1]]:
    #         if peer != naked_pairs[i][0]:
    #             # check(peer, values, 'naked')
    #             assign_value(values, peer, values[peer].replace(naked_pair_values[i][0], ''))
    #             assign_value(values, peer, values[peer].replace(naked_pair_values[i][1], ''))

    # for peer in peers[key]:
    #     if peer != twin:
    #         # Question- Not sure how to use assign_value with .replace()
    #         assign_value(values,peer,values[peer].replace(first_num,''))
    #         assign_value(values,peer,values[peer].replace(second_num,''))
    #         # values[peer] = values[peer].replace(first_num,'')
    #         # values[peer] = values[peer].replace(second_num,'')
    # for peer in peers[twin]:
    #     if peer != key:
    #         assign_value(values,peer,values[peer].replace(first_num,''))
    #         assign_value(values,peer,values[peer].replace(second_num,''))
    #         # values[peer] = values[peer].replace(first_num,'')
    #         # values[peer] = values[peer].replace(second_num,'')
    return values

def check(peer, values, text):
    if peer == 'E6':
        print('about to change E6')
        print(values[peer])
        print(text)

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

boxes = cross(rows, cols)

diagonals_1 = []
for i in range(0,9):
    diagonals_1.append(rows[i] + cols[i])
diagonals_2 = []
for i in range(0,9):
    diagonals_2.append(rows[8-i] + cols[i])
diagonals =[diagonals_1,diagonals_2]

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

unitlist = row_units + column_units + square_units + diagonals
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    grid_array = []

    for value in grid:
        if value == '.':
            grid_array.append('123456789')
        else:
            grid_array.append(value)

    return dict(zip(boxes, grid_array))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    for key in values.keys():
        if len(values[key]) == 1:
            for peer in peers[key]:
                # check(peer, values, 'eliminate')
                new_value = values[peer].replace(values[key],'')
                assign_value(values, peer, new_value)
                # values[peer] = values[peer].replace(values[key],'')
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                # Question- Is this correct use of assign_value here?
                # check(dplaces[0], values, 'only choice')
                assign_value(values, dplaces[0], digit)
                # values[dplaces[0]] = digit
    return values


def reduce_puzzle(values):
    stalled = False
    test = 0
    # while not stalled:
    while test < 1:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        display(values)
        print('after eliminate')
        # Use the Only Choice Strategy
        values = only_choice(values)
        display(values)
        print('after only-choice')
        # Use the Naked Twins Strategy
        # values = naked_twins(values)
        display(values)
        print('after naked_twins')
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            print('about to return false')
            return False
        test += 1
    return values

def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))


if __name__ == '__main__':
    # diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    diag_sudoku_grid = '......8.68.........7..863.....8............8..8.5.9...1.8..............8.....8.4.'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
