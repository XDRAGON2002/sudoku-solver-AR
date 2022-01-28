# SUDOKU SOLVING ALGORITHM BY PETER NORVIG
import numpy as np

def CROSS(A, B):
    
    return [a + b for a in A for b in B]
    
digits   = '123456789'
rows     = 'ABCDEFGHI'
cols     = digits
squares  = CROSS(rows, cols)
unitlist = ([CROSS(rows, c) for c in cols] +
        [CROSS(r, cols) for r in rows] +
        [CROSS(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
units = dict((s, [u for u in unitlist if s in u]) 
         for s in squares)
peers = dict((s, set(sum(units[s],[]))-set([s]))
         for s in squares)


def PARSE_GRID(grid):

    values = dict((s, digits) for s in squares)
    for s,d in list(GRID_ASSIGN(grid).items()):
        if d in digits and not ASSIGN(values, s, d):
            return False
    return values

def GRID_ASSIGN(grid):

    chars = [c for c in grid if c in digits or c in '0.']
    return dict(list(zip(squares, chars)))


def ASSIGN(values, s, d):

    other_values = values[s].replace(d, '')
    if all(ELIMINATE(values, s, d2) for d2 in other_values):
        return values
    else:
        return False

def ELIMINATE(values, s, d):

    if d not in values[s]:
        return values
    values[s] = values[s].replace(d,'')
    if len(values[s]) == 0:
        return False
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(ELIMINATE(values, s2, d2) for s2 in peers[s]):
            return False
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False
        elif len(dplaces) == 1:
            if not ASSIGN(values, dplaces[0], d):
                return False
    return values
    
def SOLVE(digits_box):
    grid=""

    for i in range(9):
        for j in range(9):
            box = digits_box[j][i]

            if box!=0:
                grid += str(box)
            else:
                grid = grid + "."
      
    solved = SEARCH(PARSE_GRID(grid))
    if not solved:
        return False
    matrix = []
    for cell in solved:
        matrix.append(int(solved[cell]))
    matrix = np.array(matrix).reshape(9,9).tolist()
    return matrix


def SEARCH(values):

    if values is False:
        return False
    if all(len(values[s]) == 1 for s in squares): 
        return values
    n,s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return SOME(SEARCH(ASSIGN(values.copy(), s, d)) for d in values[s])

def SOME(seq):

    for e in seq:
        if e: return e
    return False

# print(PARSE_GRID("4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......"))
# print(SEARCH(PARSE_GRID("8...1...9.5.8.7.1...4.9.7...6.7.1.2.5.8.6.1.7.1.5.2.9...7.4.6...8.3.9.4.3...5...8")))