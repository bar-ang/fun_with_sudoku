import sys
import random
from copy import deepcopy
from math import sqrt
import re

class Sudoku:
    def __init__(self, sudoku):
        size = len(sudoku)
        self._sudoku = sudoku
        self._fixed = [[True if val else False for val in row] for row in sudoku]

    def read_file(filename):
        with open(filename, "r") as file:
            content = file.read()

        content = re.sub(r"[\s\t\n]+", " ", content)
        content = re.sub(r"[^\d\s]+", "", content)
        content = content.strip().split(" ")
        size = int(sqrt(len(content)))
        if size ** 2 < len(content):
            size += 1
        su = [[0] * size for i in range(size)]
        for i, c in enumerate(content):
            su[i // size][i % size] = int(c)
        return Sudoku(su)

    @property
    def size(self):
        return len(self._sudoku)

    @property
    def part_size(self):
        part_size = int(sqrt(self.size))
        if part_size ** 2 != self.size:
            return None
        return part_size

    def solutions(self, *, i=0, j=0):
        if i == self.size:
            return self.solutions(i=0, j=j+1)

        if j == self.size:
            return [deepcopy(self)]

        sols = []
        if self._sudoku[i][j] == 0:
            for t in range(1, self.size + 1):
                self._sudoku[i][j] = t
                if self.check_position(i, j):
                    sols += self.solutions(i=i+1, j=j)
                    if len(sols) >= 20:
                        return sols
                self._sudoku[i][j] = 0
        else:
            sols += self.solutions(i=i+1, j=j)
            if len(sols) >= 20:
                return sols
        return sols

    def check_position(self, i, j):
        val = self._sudoku[i][j]
        for r in range(self.size):
            if (r != j and self._sudoku[i][r] == val) or (r != i and self._sudoku[r][j] == val):
                return False

        part_size = self.part_size
        if part_size:
            rx = part_size * (i // part_size)
            ry = part_size * (j // part_size)
            for x in range(part_size):
                for y in range(part_size):
                    if self._sudoku[rx+x][ry+y] == val and not (rx+x==i and ry+y==j):
                        return False

        return True

    def __str__(self):
        t = ""
        part_size = self.part_size
        for i, row in enumerate(self._sudoku):
            for j, val in enumerate(row):
                s = "%s " % (val if val else "_")
                if self._fixed[i][j]:
                    s = "\033[33m%s\033[0m" % s
                t += s
                if part_size and j % part_size == part_size - 1:
                    t += "  "
            t += "\n"
            if part_size and i % part_size == part_size - 1:
                t += "\n"
        return t

class SudokuMaker(Sudoku):
    

def random_sudoku(size=9, num_fixed=8):
    su = Sudoku([[0] * size for i in range(size)])
    for i in range(num_fixed):
        while True:
            x = random.randint(0, 8)
            y = random.randint(0, 8)
            v = random.randint(1, 9)
            if su._sudoku[x][y]:
                continue
            su._sudoku[x][y] = v
            if not su.check_position(x, y):
                su._sudoku[x][y] = 0
                continue
            break
    return Sudoku(su._sudoku)

def main():
    sudoku = Sudoku.read_file("sudoku.txt")
    print("Solving Sudoku:")
    print(sudoku)
    sols = sudoku.solutions()
    if len(sols) == 0:
        print("There is no solution :(")
    else:
        print("There are%s %s solutions" % (" more than" if len(sols) >= 20 else "" ,len(sols)))
        for i, sol in enumerate(sols):
            print("solution #%s:" % (i+1))
            print(sol)

main()
