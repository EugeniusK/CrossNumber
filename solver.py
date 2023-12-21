import math
import json
import time
from functions import *


def count2d(arr):
    total = 0
    for row in arr:
        total += len(row)
    return total


class CrossNumber:
    def __init__(
        self,
        cross_number_name: str,
        grid_outline: str,
        h_clues_pos: str,
        v_clues_pos: str,
        h_clues: str,
        v_clues: str,
    ):
        self.start = time.time()
        self.name = cross_number_name
        """
        ### Arugments

        cross_number_name: name of the crossnumber - used for .json filename
        grid_outline: a multi-line string that represents open spaces with 1s and closed spaces with 2s
        h_clues_pos: a multi-line string that represents location of horizontal clues using numbers and "x" - use . to separate single digit numbers
        v_clues_pos: a multi-line string that represents location of vertical clues using numbers and "x" - use . to separate single digit numbers
        h_clues: a multi-line string that uses "number. keyword" to represent each horizontal clue
        h_clues: a multi-line string that uses "number. keyword" to represent each vertical clue

        ### Attributes
        self.dim: dimensions of crossnumber
        self.values: 2D array of all the digits in crossnumber - None for no digit

        self.grid_outline: 2D array of boolean indicates the presence of digit

        self.h_clues_pos: utility array - number or 'x' depending of hint present
        self.v_clues_pos: utility array

        self.h_clues: dict of hint number (as str) and details [category, parameters (optional)]
        self.v_clues: dict of hint number (as str) and details [category, parameters (optional)]

        self.clue_lengths: dict of hint number (as str)
        self.all_clues_per_pos: clues that are linked to each square

        self.t1_pos: list of (row, col, horizontal) where all clues are
        self.t1_possibile: dict of (row,col, horizontal): [x1,x2,x3,...]
        self.t1_possible_count: dict of (row, col, horizontal): count
        """
        self.grid_outline = [
            [1 if x.isnumeric() else 0 for x in row.strip()]
            for row in grid_outline.split("\n")
        ]
        # arrays that use numbers and 'x' to indicate location of clues
        self.h_clues_pos = []
        self.v_clues_pos = []
        for row in h_clues_pos.splitlines():
            new_row = []
            tmp = ""
            for c in row.strip():
                if c == ".":
                    new_row.append("".join(tmp))
                    tmp = ""
                elif c != "x":
                    tmp += c
                else:
                    if tmp != "":
                        new_row.append("".join(tmp))
                    new_row.append("x")
                    tmp = ""
            if tmp != "":
                new_row.append("".join(tmp))
            self.h_clues_pos.append(new_row)
        for row in v_clues_pos.splitlines():
            new_row = []
            tmp = ""
            for c in row.strip():
                if c == ".":
                    new_row.append("".join(tmp))
                    tmp = ""
                elif c != "x":
                    tmp += c
                else:
                    if tmp != "":
                        new_row.append("".join(tmp))
                    new_row.append("x")
                    tmp = ""
            if tmp != "":
                new_row.append("".join(tmp))
            self.v_clues_pos.append(new_row)
        # dict that stores clue number and clue itself - 1: 'prime'
        self.h_clues = dict()
        self.v_clues = dict()

        for h_clue in h_clues.split("\n"):
            self.h_clues[h_clue.split()[0][:-1]] = h_clue.split()[1:]
        for v_clue in v_clues.split("\n"):
            self.v_clues[v_clue.split()[0][:-1]] = v_clue.split()[1:]
        # dimensions of array
        self.dim = (
            len(self.grid_outline),
            count2d(self.grid_outline) // len(self.grid_outline),
        )
        # values in the array
        self.values = [[None for _ in range(self.dim[1])] for _ in range(self.dim[0])]
        # lengths of tier 1 functions to self.clue_lengths - (row, col, horizontal): (length, clue)
        self.clue_lengths = dict()
        # which clues affect the value
        self.all_clues_per_pos = [
            [[] for _ in range(self.dim[1])] for _ in range(self.dim[0])
        ]
        for row in range(self.dim[0]):
            for col in range(self.dim[1]):
                if self.h_clues_pos[row][col].isnumeric():
                    number_length = 0
                    tmp_col = col

                    while tmp_col < self.dim[1]:
                        if self.grid_outline[row][tmp_col] == 1:
                            self.all_clues_per_pos[row][tmp_col].append(
                                (row, col, True)
                            )
                            number_length += 1
                            tmp_col += 1
                        else:
                            break
                    self.clue_lengths[(row, col, True)] = (
                        number_length,
                        *self.h_clues[self.h_clues_pos[row][col]],
                    )
                if self.v_clues_pos[row][col].isnumeric():
                    number_length = 0
                    tmp_row = row

                    while tmp_row < self.dim[0]:
                        if self.grid_outline[tmp_row][col] == 1:
                            self.all_clues_per_pos[tmp_row][col].append(
                                (row, col, False)
                            )
                            number_length += 1
                            tmp_row += 1
                        else:
                            break
                    self.clue_lengths[(row, col, False)] = (
                        number_length,
                        *self.v_clues[self.v_clues_pos[row][col]],
                    )

        # tier 1 - where there is a fixed number of possible - such as "A triangle number"
        # tier 2 - everytihng else - relies on other value or the number of occurences of a specific digit

        # tier 1 - check if possible, set
        # tier 2 - at the end, check if valid

        self.clue_pos = {}
        self.clue_pos_all = []

        for row in range(self.dim[0]):
            for col in range(self.dim[1]):
                if self.h_clues_pos[row][col] != "x":
                    self.clue_pos[self.h_clues_pos[row][col] + "a"] = (
                        row,
                        col,
                        True,
                    )
                    self.clue_pos_all.append(self.h_clues_pos[row][col] + "a")
                if self.v_clues_pos[row][col] != "x":
                    self.clue_pos[self.v_clues_pos[row][col] + "v"] = (
                        row,
                        col,
                        False,
                    )
                    self.clue_pos_all.append(self.v_clues_pos[row][col] + "v")

        self.all_pos = []
        self.t1_pos = []
        self.t2_pos = []

        self.all_possible = dict()

        self.all_possible_count = dict()
        self.t1_possible_count = dict()
        self.t2_possible_count = dict()

        self.t2_description = dict()
        self.t2_access_used = dict()
        self.t2_count_used = dict()
        self.t2_dsum_used = dict()

        while True:
            try:
                with open(f"json/{self.name}_crossnumber.json", "r") as f:
                    numbers = json.load(f)  # dictionary of all values
                    for x in self.clue_lengths.keys():
                        # initial values possible where same length and no start with zero
                        # modified to remove unnecessary possibilities
                        if x[2] == True:
                            clue = self.h_clues[self.h_clues_pos[x[0]][x[1]]]
                        elif x[2] == False:
                            clue = self.v_clues[self.v_clues_pos[x[0]][x[1]]]
                        self.all_possible[x] = [
                            n
                            for n in numbers[self.clue_lengths[x][1]]
                            if len(str(n)) == self.clue_lengths[x][0]
                            and str(n)[0] != "0"
                        ]
                        if "sum" in clue or "multiple" in clue or len(clue) == 1:
                            self.t1_pos.append(x)
                            if len(clue) != 1:
                                # extract range, if any, from the clue
                                clue_range = eval("".join(clue[2:]))
                                if type(clue_range) == list:
                                    possible_values = list(
                                        range(clue_range[0], clue_range[1] + 1)
                                    )
                                else:
                                    possible_values = [clue_range]

                                if "sum" in clue:
                                    self.all_possible[x] = [
                                        a
                                        for a in self.all_possible[x]
                                        if sum([int(n) for n in str(a)])
                                        in possible_values
                                    ]
                                elif "multiple" in clue:
                                    self.all_possible[x] = [
                                        a
                                        for a in self.all_possible[x]
                                        if (
                                            True
                                            in [a % n == 0 for n in possible_values]
                                        )
                                    ]
                            self.t1_possible_count[x] = len(self.all_possible[x])

                        else:
                            self.t2_pos.append(x)
                            self.t2_possible_count[x] = len(self.all_possible[x])
                            self.t2_description[x] = [clue[0], " ".join(clue[1:])]
                            for pos in self.clue_pos_all:
                                if pos in self.t2_description[x][1]:
                                    self.t2_dsum_used["d" + pos] = None
                                    self.t2_access_used[pos] = None

                            for count in range(10):
                                if "n" + str(count) in self.t2_description[x][1]:
                                    self.t2_count_used["n" + str(count)] = None
                        self.all_possible_count[x] = len(self.all_possible[x])
                # raise IndexError

                break
            except IOError:
                self.max_lengths = dict()
                for x in self.clue_lengths.keys():
                    if self.max_lengths.get(self.clue_lengths[x][1]) == None:
                        self.max_lengths[self.clue_lengths[x][1]] = self.clue_lengths[
                            x
                        ][0]
                    else:
                        self.max_lengths[self.clue_lengths[x][1]] = max(
                            self.max_lengths[self.clue_lengths[x][1]],
                            self.clue_lengths[x][0],
                        )

                numbers_dict_calculated = dict()
                for x in self.max_lengths.keys():
                    numbers_dict_calculated[x] = NUMBERS_DICT[x](
                        10 ** self.max_lengths[x]
                    )
                with open(f"json/{self.name}_crossnumber.json", "w") as f:
                    numbers_dict_calculated = dict()
                    for x in self.max_lengths.keys():
                        numbers_dict_calculated[x] = NUMBERS_DICT[x](
                            10 ** self.max_lengths[x]
                        )
                    json.dump(numbers_dict_calculated, f)

        self.all_pos = sorted(self.t1_pos) + self.t2_pos
        """
        Removes impossible candidates from list of possible values
        - by looking at the intersection of digits from all clues
        """

        self.init_count = math.prod(self.all_possible_count.values())
        self.possible_digits = [
            [[] for _ in range(self.dim[1])] for x in range(self.dim[0])
        ]
        for clue_pos in self.all_pos:
            clue_length = self.clue_lengths[clue_pos][0]
            horizontal = clue_pos[2]
            for x in range(clue_length):
                possible_digits = set()
                for child in self.all_possible[clue_pos]:
                    possible_digits.add(int(str(child)[x]))
                if horizontal:
                    self.possible_digits[clue_pos[0]][clue_pos[1] + x].append(
                        possible_digits
                    )
                else:
                    self.possible_digits[clue_pos[0] + x][clue_pos[1]].append(
                        possible_digits
                    )

        for row in range(self.dim[0]):
            for col in range(self.dim[1]):
                if len(self.possible_digits[row][col]) != 0:
                    self.possible_digits[row][col] = list(
                        set.intersection(*self.possible_digits[row][col])
                    )

        for clue_pos in self.all_pos:
            clue_length = self.clue_lengths[clue_pos][0]
            horizontal = clue_pos[2]
            for possible_val in self.all_possible[clue_pos]:
                valid = True
                for x in range(clue_length):
                    if horizontal:
                        if (
                            int(str(possible_val)[x])
                            not in self.possible_digits[clue_pos[0]][clue_pos[1] + x]
                        ):
                            valid = False
                    else:
                        if (
                            int(str(possible_val)[x])
                            not in self.possible_digits[clue_pos[0] + x][clue_pos[1]]
                        ):
                            valid = False

                if not valid:
                    self.all_possible[clue_pos].remove(possible_val)

        self.all_possible_count = {x: len(self.all_possible[x]) for x in self.all_pos}
        self.reduced_count = math.prod(self.all_possible_count.values())

    def set_value(self, row, col, horizontal, value):
        if horizontal == True:
            for x in range(len(str(value))):
                self.values[row][col + x] = int(str(value)[x])
        else:
            for x in range(len(str(value))):
                self.values[row + x][col] = int(str(value)[x])

    def get_value(self, row, col, horizontal, length):
        value = []
        digits = []
        if horizontal == True:
            digits = [self.values[row][col + x] for x in range(length)]
            if None in digits:
                return -1

        else:
            digits = [self.values[row + x][col] for x in range(length)]
            if None in digits:
                return -1
        value = [digits[x] * 10 ** (length - x - 1) for x in range(length)]
        return sum(value)

    def clear(self):
        self.values = [[None for _ in range(self.dim[1])] for _ in range(self.dim[0])]

    def is_possible(self, row, col, horizontal, value):
        filled_in = []
        filled_index = []
        str_value = str(value)
        number_length = self.clue_lengths[(row, col, horizontal)][0]
        if horizontal == True:
            for x in range(number_length):
                filled_in.append(self.values[row][col + x])
                if self.values[row][col + x] != None:
                    filled_index.append(x)
        else:
            for x in range(number_length):
                filled_in.append(self.values[row + x][col])
                if self.values[row + x][col] != None:
                    filled_index.append(x)

        return False not in [
            str_value[idx] == str(filled_in[idx]) for idx in filled_index
        ]

    def safe_up_to(self, solution, position):
        self.clear()
        for s in range(position):
            self.set_value(
                *self.all_pos[s],
                self.all_possible[self.all_pos[s]][solution[s]],
            )
            if not self.is_possible(
                *self.all_pos[s + 1],
                self.all_possible[self.all_pos[s + 1]][solution[s + 1]],
            ):
                return False
        self.set_value(
            *self.all_pos[position],
            self.all_possible[self.all_pos[position]][solution[position]],
        )
        if position == len(self.clue_lengths.keys()) - 1:
            for count in list(self.t2_count_used.keys()):
                self.t2_count_used[count] = sum(
                    [x.count(int(count[1])) for x in self.values]
                )
            for pos in list(self.t2_access_used.keys()):
                self.t2_access_used[pos] = self.get_value(
                    *self.clue_pos[pos],
                    self.clue_lengths[self.clue_pos[pos]][0],
                )
                self.t2_dsum_used["d" + pos] = sum(
                    [
                        int(x)
                        for x in str(
                            self.get_value(
                                *self.clue_pos[pos],
                                self.clue_lengths[self.clue_pos[pos]][0],
                            )
                        )
                    ]
                )
            for pos in self.t2_pos:
                if self.get_value(*pos, self.clue_lengths[pos][0]) not in eval(
                    self.t2_description[pos][1],
                    self.t2_count_used | self.t2_access_used | self.t2_dsum_used,
                ):
                    return False
        return True

    def backtrace(self):
        number_all = len(self.all_pos)

        solution = [None] * number_all

        def backtrace_from(position):
            while True:
                if self.safe_up_to(solution, position):
                    if position > self.max_position:
                        print(
                            f"{position}/{number_all}",
                            round(time.time() - self.start, 2),
                            round(
                                (
                                    sum(
                                        [
                                            solution[x]
                                            * math.prod(
                                                list(self.all_possible_count.values())[
                                                    x + 1 :
                                                ]
                                            )
                                            for x in range(number_all)
                                            if solution[x] != None
                                        ]
                                    )
                                    + 1
                                )
                                / self.reduced_count,
                                4,
                            ),
                        )
                        self.max_position = position
                    if position >= number_all - 1:
                        return solution
                    position += 1
                    solution[position] = 0
                else:
                    while (
                        solution[position]
                        == self.all_possible_count[self.all_pos[position]] - 1
                    ):
                        solution[position] = None
                        position -= 1
                    if position < 0:
                        break
                    solution[position] += 1
            return None

        self.max_position = 0
        solution[0] = 0
        solution = backtrace_from(0)
        self.clear()
        for x in range(len(solution)):
            self.set_value(
                *self.all_pos[x],
                self.all_possible[self.all_pos[x]][solution[x]],
            )
        self.display()
        n0 = sum([x.count(0) for x in self.values])
        n1 = sum([x.count(1) for x in self.values])
        n2 = sum([x.count(2) for x in self.values])
        n3 = sum([x.count(3) for x in self.values])
        n4 = sum([x.count(4) for x in self.values])
        n5 = sum([x.count(5) for x in self.values])
        n6 = sum([x.count(6) for x in self.values])
        n7 = sum([x.count(7) for x in self.values])
        n8 = sum([x.count(8) for x in self.values])
        n9 = sum([x.count(9) for x in self.values])
        print("init     ", math.log10(self.reduced_count))
        print("reduced  ", math.log10(self.init_count))
        print("factor of", self.init_count / self.reduced_count)
        print("time     ", time.time() - self.start, "seconds")

        print(n0, n1, n2, n3, n4, n5, n6, n7, n8, n9)

    def display(self):
        for row in range(len(self.values)):
            val = []
            for x in range(len(self.values[row])):
                if self.values[row][x] != None:
                    val.append(" " + str(self.values[row][x]) + " ")
                elif self.grid_outline[row][x] == 1:
                    val.append("   ")
                else:
                    val.append("\u2588\u2588\u2588")
            print("\u2503".join(val))
            if row != self.dim[0] - 1:
                print("\u254B".join(["\u2501\u2501\u2501" for _ in range(self.dim[1])]))


if __name__ == "__main__":
    print("hi")
