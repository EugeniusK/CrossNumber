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

        self.tier_one_all_children_pos: list of (row, col, horizontal) where all clues are
        self.tier_one_all_children_possibile: dict of (row,col, horizontal): [x1,x2,x3,...]
        self.tier_one_all_children_possible_count: dict of (row, col, horizontal): count
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
        self.tier_one_all_children_possible = dict()
        self.tier_one_all_children_possible_count = dict()
        self.tier_one_all_children_pos = []

        self.tier_three_all_children_possible = dict()
        self.tier_three_all_children_possible_count = dict()
        self.tier_three_all_children_pos = []
        self.tier_three_description = dict()

        self.all_children_pos = []
        self.all_children_possible = dict()
        self.all_children_possible_count = dict()
        while True:
            try:
                with open(f"{self.name}_crossnumber.json", "r") as f:
                    numbers = json.load(f)
                    for x in self.clue_lengths.keys():
                        self.all_children_possible[x] = [
                            n
                            for n in numbers[self.clue_lengths[x][1]]
                            if len(str(n)) == self.clue_lengths[x][0]
                            and str(n)[0] != "0"
                        ]
                        if (
                            x[2] == True
                            and len(self.h_clues[self.h_clues_pos[x[0]][x[1]]]) == 1
                        ) or (
                            x[2] == False
                            and len(self.v_clues[self.v_clues_pos[x[0]][x[1]]]) == 1
                        ):
                            self.tier_one_all_children_pos.append(x)
                            self.tier_one_all_children_possible_count[x] = len(
                                self.all_children_possible[x]
                            )
                        elif (
                            x[2] == True
                            and len(self.h_clues[self.h_clues_pos[x[0]][x[1]]]) != 1
                        ) or (
                            x[2] == False
                            and len(self.v_clues[self.v_clues_pos[x[0]][x[1]]]) != 1
                        ):
                            self.tier_three_all_children_pos.append(x)
                            self.tier_three_all_children_possible_count[x] = len(
                                self.all_children_possible[x]
                            )
                            self.tier_three_description[x] = self.v_clues[
                                self.v_clues_pos[x[0]][x[1]]
                            ]

                        self.all_children_possible_count[x] = len(
                            self.all_children_possible[x]
                        )
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
                with open(f"{self.name}_crossnumber.json", "w") as f:
                    numbers_dict_calculated = dict()
                    for x in self.max_lengths.keys():
                        numbers_dict_calculated[x] = NUMBERS_DICT[x](
                            10 ** self.max_lengths[x]
                        )
                    json.dump(numbers_dict_calculated, f)

        self.all_children_pos = sorted(
            self.tier_one_all_children_pos + self.tier_three_all_children_pos
        )

        self.init_all_children_possible_count = self.all_children_possible_count
        self.possible_digits = [
            [[] for _ in range(self.dim[1])] for x in range(self.dim[0])
        ]
        for clue_pos in self.all_children_pos:
            clue_length = self.clue_lengths[clue_pos][0]
            horizontal = clue_pos[2]
            for x in range(clue_length):
                possible_digits = set()
                for child in self.all_children_possible[clue_pos]:
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

        for clue_pos in self.all_children_pos:
            clue_length = self.clue_lengths[clue_pos][0]
            horizontal = clue_pos[2]
            for possible_val in self.all_children_possible[clue_pos]:
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
                    self.all_children_possible[clue_pos].remove(possible_val)
        self.all_children_possible_count = {
            x: len(self.all_children_possible[x]) for x in self.all_children_pos
        }

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
                *self.all_children_pos[s],
                self.all_children_possible[self.all_children_pos[s]][solution[s]],
            )
            if not self.is_possible(
                *self.all_children_pos[s + 1],
                self.all_children_possible[self.all_children_pos[s + 1]][
                    solution[s + 1]
                ],
            ):
                return False
        self.set_value(
            *self.all_children_pos[position],
            self.all_children_possible[self.all_children_pos[position]][
                solution[position]
            ],
        )
        if position == len(self.clue_lengths.keys()) - 1:
            print("call")
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

            if n0 * (n0 + 1) // 2 == self.get_value(5, 7, False, 2) and (n1 - 1) * (
                2 * (n1 - 1) ** 2 + 1
            ) // 3 == self.get_value(2, 1, False, 4):
                return True
            return False
        return True

    def backtrace(self):
        number_tier_one = len(self.clue_lengths.keys())

        solution = [None] * number_tier_one

        def backtrace_from(position):
            while True:
                if self.safe_up_to(solution, position):
                    if position > self.max_position:
                        print(position)
                        print(time.time() - self.start)
                        self.max_position = position
                        self.display()
                        print(solution)
                        print(self.all_children_pos[position])
                        print(
                            "init", math.prod(self.all_children_possible_count.values())
                        )
                        print(
                            "reduced",
                            math.prod(self.init_all_children_possible_count.values()),
                        )
                        print(
                            "factor of",
                            math.prod(self.init_all_children_possible_count.values())
                            / math.prod(self.all_children_possible_count.values()),
                        )

                    if position >= number_tier_one - 1:
                        return solution
                    position += 1
                    solution[position] = 0
                else:
                    while (
                        solution[position]
                        == self.all_children_possible_count[
                            self.all_children_pos[position]
                        ]
                        - 1
                    ):
                        solution[position] = None
                        position -= 1
                    if position < 0:
                        break
                    solution[position] += 1
            self.display()
            return None

        self.max_position = 0
        solution[0] = 0
        solution = backtrace_from(0)
        self.clear()
        for x in range(len(solution)):
            self.set_value(
                *self.all_children_pos[x],
                self.all_children_possible[self.all_children_pos[x]][solution[x]],
            )
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


test = False
if test:
    board = CrossNumber(
        "test",
        """11111x1x111x
            1x11x1111x11
            11x1111x111x
            x111xx111x1x
            11x1111x1111
            111x1xx1x1x1
            1x111x111111
            111x111xx1x1
            x1x11x1x1111
            1111x1111x1x
            x1x111xx1111
            1111x11111x1""",
        """1xxxxxxx5xxx
            xx7xx8xxxx9x
            10xx12xxxx13xxx
            x14xxxx15xxxxx
            16xx17xxxx19xxx
            22xxxxxxxxxxx
            xx25xxx26xxxxx
            27xxx29xxxxxxx
            xxx30xxxx31xxx
            33xxxx34xxxxxx
            xxx35xxxx36xxx
            39xxxx40xxxxxx""",
        """1x2.3xx4x5x6x
            xxxxxxxxxxxx
            x11xxxxxxxxxx
            xxxxxxxxxxxx
            16xxx18xxxx20x21
            xx23xxxx24xxxx
            xxxxxx26xxxxx
            x28xxxxxxxxxx
            xxx30xxxx31x32x
            xxxxx34xxxxxx
            xxxxxxxxx37x38
            xxxxxxxxxxxx""",
        """1. integer
            5. integer
            7. integer
            8. integer
            9. integer
            10. integer
            12. integer
            13. integer
            14. integer
            15. integer
            16. integer
            17. integer
            19. integer
            22. integer
            25. integer
            26. integer
            27. integer
            29. integer
            30. integer
            31. integer
            33. integer
            34. integer
            35. integer
            36. integer
            39. integer
            40. integer""",
        """1. integer
            2. integer
            3. integer
            4. integer
            5. integer
            6. integer
            8. integer
            11. integer
            16. integer
            18. integer
            20. integer
            21. integer
            23. integer
            24. integer
            26. integer
            28. integer
            30. integer
            31. integer
            32. integer
            34. integer
            37. integer
            38. integer""",
    )
    board.display()
    # # print(board.is_possible(0, 0, False, 115))
    # # board.values = [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, None, None, None, None]]
    # # print(board.get_value(0, 0, 5, True))
    # board.backtrace()
    board.set_value(0, 0, True, 12345)
    board.display()
    print(board.is_possible(0, 2, False, 214))

else:
    board = CrossNumber(
        "yuichiro",
        """11111x1x111x
            1x11x1111x11
            11x1111x111x
            x111xx111x1x
            11x1111x1111
            111x1xx1x1x1
            1x111x111111
            111x111xx1x1
            x1x11x1x1111
            1111x1111x1x
            x1x111xx1111
            1111x11111x1""",
        """1xxxxxxx5xxx
            xx7xx8xxxx9x
            10xx12xxxx13xxx
            x14xxxx15xxxxx
            16xx17xxxx19xxx
            22xxxxxxxxxxx
            xx25xxx26xxxxx
            27xxx29xxxxxxx
            xxx30xxxx31xxx
            33xxxx34xxxxxx
            xxx35xxxx36xxx
            39xxxx40xxxxxx""",
        """1x2.3xx4x5x6x
            xxxxxxxxxxxx
            x11xxxxxxxxxx
            xxxxxxxxxxxx
            16xxx18xxxx20x21
            xx23xxxx24xxxx
            xxxxxx26xxxxx
            x28xxxxxxxxxx
            xxx30xxxx31x32x
            xxxxx34xxxxxx
            xxxxxxxxx37x38
            xxxxxxxxxxxx""",
        """1. pronic
            5. trimorphic
            7. decagonal
            8. pentagonal
            9. triangle
            10. padovan
            12. vampire
            13. lucas
            14. untouchable
            15. hexagonal
            16. trimorphic
            17. pentagonal
            19. pronic
            22. pronic
            25. super3
            26. kaprekar
            27. padovan
            29. sophiegermain
            30. sophiegermain
            31. perrin
            33. lucas
            34. octahedral
            35. hexagonal
            36. hexagonal
            39. icosahedral
            40. icosahedral""",
        """1. super3
            2. tribonacci
            3. keith
            4. icosahedral
            5. hexagonal
            6. pentagonal
            11. octahedral count 1
            16. super4
            18. A053873
            20. strobogrammatic
            21. pentagonal
            23. trimorphic
            24. triangle count 0 start 1
            26. tetradic
            28. pentagonal
            30. octahedral
            31. quartan
            32. perrin
            34. pentagonal
            37. emirp
            38. tetrahedral""",
    )
    board.display()
    # print(board.all_children_pos)
    # print(
    #     [
    #         True if x in board.tier_one_all_children_pos else False
    #         for x in board.all_children_pos
    #     ]
    # )
    # print(board.all_children_possible)
    board.backtrace()
