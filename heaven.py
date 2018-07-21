#!/usr/bin/env python3

from collections import deque

def solve(grid, simulate=False):
    # Find the dimensions.
    N, M = len(grid), len(grid[0])
    # Find the starts.
    Q = deque((0, cell, i, j)
              for (i, row) in enumerate(grid)
              for (j, cell) in enumerate(row) if cell in '+-')
    #  fill.
    heaven = None
    day = 0
    while Q:
        t, cell, i, j = Q.popleft()
        assert t >= day
        if t > day:
            if simulate:
                print(day)
                for row in grid: print("".join(row))
            day = t
        if heaven is not None and t > heaven: break
        if grid[i][j] == '.' or t == 0:
            grid[i][j] = cell
            for di, dj in [(0,1), (1,0), (0,-1), (-1,0)]:
                if 0 <= i+di < N and 0 <= j+dj < M and \
                   grid[i+di][j+dj] not in ['X', cell]:
                    Q.append((t+1, cell, i+di, j+dj))
        elif grid[i][j] != cell:
            heaven = t
            grid[i][j] = '*'
    return heaven, grid

if __name__ == "__main__":
    import sys
    source = sys.argv[1]
    with open(source, "rt") as f:
        grid = [list(line.strip()) for line in f]
    t, grid = solve(grid)
    print(t if t is not None else "heaven is upon us!")
    for row in grid: print("".join(row))
