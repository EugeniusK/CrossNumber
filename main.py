import math
import json
import time
from functions import *


def count2d(arr):
    total = 0
    for row in arr:
        total += len(row)
    return total


def arrToInt(arr):
    if None in arr or arr == False:
        return False
    return sum([arr[x] * 10 ** (len(arr) - x - 1) for x in range(len(arr))])


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
        # tier 2 - where another value is used in the calculation
        # tier 3 - where the digit sum of another value is used in the calculation
        # tier 4 - where the number of a specific digit in the crossnumber is used

        # tier 1 - check if possible, set
        # tier 2 - calculate based on other value, check if possible, set
        # tier 3 - at the end, calculate digit sum of other value, check if valid
        # tier 4 - at the end, check if valid

        self.clue_pos = {}
        for row in range(self.dim[0]):
            for col in range(self.dim[1]):
                if self.h_clues_pos[row][col] != "x":
                    self.clue_pos[self.h_clues_pos[row][col] + "a"] = (
                        row,
                        col,
                        True,
                    )
                if self.v_clues_pos[row][col] != "x":
                    self.clue_pos[self.v_clues_pos[row][col] + "v"] = (
                        row,
                        col,
                        False,
                    )

        self.all_pos = []
        self.t1_pos = []
        self.t2_pos = []
        self.t4_pos = []

        self.all_possible = dict()

        self.all_possible_count = dict()
        self.t1_possible_count = dict()
        self.t2_possible_count = dict()
        self.t4_possible_count = dict()

        self.t2_description = dict()
        self.t4_description = dict()
        while True:
            try:
                with open(f"{self.name}_crossnumber.json", "r") as f:
                    numbers = json.load(f)  # dictionary of all values
                    for x in self.clue_lengths.keys():
                        if x[2] == True:
                            clue = self.h_clues[self.h_clues_pos[x[0]][x[1]]]
                        elif x[2] == False:
                            clue = self.v_clues[self.v_clues_pos[x[0]][x[1]]]
                        self.all_possible[x] = [
                            n
                            for n in numbers[self.clue_lengths[x][1]]
                            if len(str(n)) == self.clue_lengths[x][0]
                            and str(n)[0] != "0"
                        ]  # initial values possible where same length and no start with zero
                        # modified to remove unnecessary possibilities

                        if "count" in clue:
                            self.t4_pos.append(x)
                            self.t4_possible_count[x] = len(self.all_possible[x])
                            self.t4_description[x] = [clue[0], {}]
                            clue = clue[0:2] + [" ".join(clue[2:])]
                            self.t4_description[x][1]["eval"] = clue[2]
                        elif "dsum" in clue:
                            self.t2_pos.append(x)
                            self.t2_possible_count[x] = len(self.all_possible[x])
                            self.t2_description[x] = [clue[0], {}]
                            clue = clue[0:3] + [" ".join(clue[3:])]
                            self.t2_description[x][1]["eval"] = clue[3]
                            self.t2_description[x][1]["n"] = self.clue_pos[clue[2]]
                            # print(self.all_possible[x])
                            print("23a", self.all_possible[x])

                            print(
                                "15a", self.all_possible[self.t2_description[x][1]["n"]]
                            )
                            print(
                                set(
                                    [
                                        j
                                        for k in [
                                            eval(
                                                self.t2_description[x][1]["eval"],
                                                {},
                                                {"n": sum([int(a) for a in str(n)])},
                                            )
                                            for n in self.all_possible[
                                                self.clue_pos[clue[2]]
                                            ]
                                        ]
                                        for j in k
                                    ]
                                )
                            )  # possible for tier 2 position given the values that dependent can take

                            self.all_possible[x] = list(
                                set(
                                    [
                                        j
                                        for k in [
                                            eval(
                                                self.t2_description[x][1]["eval"],
                                                {},
                                                {"n": sum([int(a) for a in str(n)])},
                                            )
                                            for n in self.all_possible[
                                                self.clue_pos[clue[2]]
                                            ]
                                        ]
                                        for j in k
                                    ]
                                ).intersection(set(self.all_possible[x]))
                            )
                            self.all_possible[self.t2_description[x][1]["n"]] = [
                                b
                                for b in self.all_possible[
                                    self.t2_description[x][1]["n"]
                                ]
                                if eval(
                                    self.t2_description[x][1]["eval"],
                                    {},
                                    {"n": sum([int(a) for a in str(b)])},
                                )[0]
                                in self.all_possible[x]
                            ]

                            # print(
                            #     [
                            #         eval(
                            #             self.t2_description[x][1]["eval"],
                            #             {},
                            #             {"n": sum([int(a) for a in str(n)])},
                            #         )
                            #         for n in self.all_possible[self.clue_pos[clue[2]]]
                            #     ]
                            # )k
                            # raise IndexError
                            print("23a", self.all_possible[x])

                            print(
                                "15a", self.all_possible[self.t2_description[x][1]["n"]]
                            )
                            # raise IndexError
                        elif "sum" in clue:
                            self.t1_pos.append(x)
                            clue_range = eval("".join(clue[2:]))
                            if type(clue_range) == list:
                                possible_sums = list(
                                    range(clue_range[0], clue_range[1] + 1)
                                )
                            else:
                                possible_sums = [clue_range]
                            tmp = [
                                a
                                for a in self.all_possible[x]
                                if sum([int(n) for n in str(a)]) in possible_sums
                            ]
                            self.all_possible[x] = tmp

                            self.t1_possible_count[x] = len(self.all_possible[x])
                        elif "multiple" in clue:
                            self.t1_pos.append(x)
                            clue_range = eval("".join(clue[2:]))
                            if type(clue_range) == list:
                                possible_products = list(
                                    range(clue_range[0], clue_range[1] + 1)
                                )
                            else:
                                possible_products = [clue_range]
                            tmp = [
                                a
                                for a in self.all_possible[x]
                                if (True in [a % n == 0 for n in possible_products])
                            ]
                            self.all_possible[x] = tmp

                            self.t1_possible_count[x] = len(self.all_possible[x])

                        else:
                            self.t1_pos.append(x)
                            self.t1_possible_count[x] = len(self.all_possible[x])

                        self.all_possible_count[x] = len(self.all_possible[x])
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
                with open(f"{self.name}_crossnumber.json", "w") as f:
                    numbers_dict_calculated = dict()
                    for x in self.max_lengths.keys():
                        numbers_dict_calculated[x] = NUMBERS_DICT[x](
                            10 ** self.max_lengths[x]
                        )
                    json.dump(numbers_dict_calculated, f)

        self.all_pos = sorted(self.t1_pos) + self.t2_pos + self.t4_pos
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
            # print("call", self.t4_pos, self.t4_description)
            # print("call", self.t2_pos, self.t2_description)

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

            for pos in self.t4_pos:
                if self.get_value(*pos, self.clue_lengths[pos][0]) not in eval(
                    self.t4_description[pos][1]["eval"], locals()
                ):
                    return False
            for pos in self.t2_pos:
                n = self.get_value(
                    *self.t2_description[pos][1]["n"], self.clue_lengths[pos][0]
                )

                # print(self.get_value(*pos, self.clue_lengths[pos][0]))
                # print(
                #     [
                #         sum([int(n) for n in str(x)])
                #         for x in eval(self.t2_description[pos][1]["eval"], locals())
                #     ]
                # )
                print(
                    time.time() - self.start,
                    math.prod([x + 1 for x in solution]) / self.reduced_count,
                )
                self.display()
                print(self.get_value(*pos, self.clue_lengths[pos][0]))
                print(
                    [
                        sum([int(n) for n in str(x)])
                        for x in eval(self.t2_description[pos][1]["eval"], locals())
                    ]
                )
                if self.get_value(*pos, self.clue_lengths[pos][0]) not in [
                    sum([int(n) for n in str(x)])
                    for x in eval(self.t2_description[pos][1]["eval"], locals())
                ]:
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
                            time.time() - self.start,
                            math.log10(self.reduced_count),
                            math.log10(self.init_count),
                            self.init_count / self.reduced_count,
                        )
                        # self.display()
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


# board_yuichiro = CrossNumber(
#     "yuichiro",
#     """11111x1x111x
#         1x11x1111x11
#         11x1111x111x
#         x111xx111x1x
#         11x1111x1111
#         111x1xx1x1x1
#         1x111x111111
#         111x111xx1x1
#         x1x11x1x1111
#         1111x1111x1x
#         x1x111xx1111
#         1111x11111x1""",
#     """1xxxxxxx5xxx
#         xx7xx8xxxx9x
#         10xx12xxxx13xxx
#         x14xxxx15xxxxx
#         16xx17xxxx19xxx
#         22xxxxxxxxxxx
#         xx25xxx26xxxxx
#         27xxx29xxxxxxx
#         xxx30xxxx31xxx
#         33xxxx34xxxxxx
#         xxx35xxxx36xxx
#         39xxxx40xxxxxx""",
#     """1x2.3xx4x5x6x
#         xxxxx8xxxxxx
#         x11xxxxxxxxxx
#         xxxxxxxxxxxx
#         16xxx18xxxx20x21
#         xx23xxxx24xxxx
#         xxxxxx26xxxxx
#         x28xxxxxxxxxx
#         xxx30xxxx31x32x
#         xxxxx34xxxxxx
#         xxxxxxxxx37x38
#         xxxxxxxxxxxx""",
#     """1. pronic
#         5. trimorphic
#         7. decagonal
#         8. pentagonal
#         9. triangle
#         10. padovan
#         12. vampire
#         13. lucas
#         14. untouchable
#         15. hexagonal
#         16. trimorphic
#         17. pentagonal
#         19. pronic
#         22. pronic
#         25. super3
#         26. kaprekar
#         27. padovan
#         29. sophiegermain
#         30. sophiegermain
#         31. perrin
#         33. lucas
#         34. octahedral
#         35. hexagonal
#         36. hexagonal
#         39. icosahedral
#         40. icosahedral""",
#     """1. super3
#         2. tribonacci
#         3. keith
#         4. icosahedral
#         5. hexagonal
#         6. pentagonal
#         8. integer count [int(((n7-2)*n**2-(n7-4)*n)/2) for n in range(100)]
#         11. octahedral count [int((n1-1)*(2*(n1-1)**2 + 1)/3)]
#         16. super4
#         18. A053873
#         20. strobogrammatic
#         21. pentagonal
#         23. trimorphic
#         24. triangle count [int(n0*(n0+1)/2)]
#         26. tetradic
#         28. pentagonal
#         30. octahedral
#         31. quartan
#         32. perrin
#         34. pentagonal
#         37. emirp
#         38. tetrahedral""",
# )
# board_yuichiro.backtrace()


board_ryder = CrossNumber(
    "ryder",
    """111x1111x1
    1x1111x111
    111xx111x1
    1x1111x111
    11x1xx1x11
    x111x1111x
    11x111xx11
    1x11x1x111
    111x1111x1
    1x1111x1x1""",
    """1xxx3xxxxx
    xx7xxxx8xx
    9xxxx10xxxx
    xx11xxxx13xx
    15xxxxxxx18x
    xxxxx20xxxx
    21xx22xxxx23x
    xx25xxxx26xx
    27xxx28xxxxx
    xx29xxxxxxx
    """,
    """1x2x3.4x5x6
    xxxxxxxxxx
    xxxxxxxxxx
    xxx12xxxx14x
    x16xxxx17xxx
    x19xxx20xxxx
    21xxxxxxxx24
    xx25xxxx26xx
    xxxx28xxxxx
    xxxxxxxxxx""",
    """1. square
    3. integer multiple 1102
    7. integer sum 9
    8. square
    9. square
    10. square
    11. integer sum 18
    13. cube
    15. prime
    18. prime
    19. integer count [x for x in range(100,1000) if int(str(x)[1]) == n9)
    20. factorial_diff
    21. integer sum 13
    22. cube
    23. integer dsum 15a [n]
    25. product_distinct_prime
    26. square
    27. square
    28. cube
    29. 4th_power""",
    """1. palindrome sum 18
    2. power_2_backwards
    3. product_distinct_prime
    4. power_2
    5. cube
    6. integer multiple 11111
    12. integer multiple 11111
    14. palindrome sum [11, 45]
    16. cube
    17. integer multiple 7
    20. permutation_12345_monotonic_seq_four
    21. integer multiple 2020
    24. 5th_power
    25. cube
    26. palindrome sum 7
    28. integer multiple 3""",
)
board_ryder.backtrace()
