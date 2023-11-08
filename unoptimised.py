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
        name: str,
        grid_outline: str,
        h_clues_pos: str,
        v_clues_pos: str,
        h_clues: str,
        v_clues: str,
    ):
        self.start = time.time()
        self.name = name
        """
        ### Arugments
        grid_outline: a multi-line string that represents spaces with 1s
        h_clues_pos
        v_clues_pos: a multi-line string that represents location of clues - use . to separate single digit numbers
        ### Attributes
        self.grid_outline: 2D array of 1s and 0s where 1 indicates the presence of number

        self.h_clues_pos: utility array - number or 'x' depending of hint present
        self.v_clues_pos: utility array

        self.h_clues: dict of hint number (as str) and details [category, parameters (optional)]
        self.v_clues: dict of hint number (as str) and details [category, parameters (optional)]

        self.tier_one_lengths: dict of hint number (as str)
        self.h_tier_one_clues: 2D array of (func, tuple) and 0s - tuple used to encode any required values

        self.v_tier_one_clues: 2D array of (func, tuple) and 0s - tuple used to encode any required values

        """
        self.grid_outline = [
            [int(x) if x.isnumeric() else 0 for x in row.strip()]
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
        # lengths of tier 1 functions to self.tier_one_lengths - (row, col, horizontal): (length, clue)
        self.tier_one_lengths = dict()
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
                    self.tier_one_lengths[(row, col, True)] = (
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
                    self.tier_one_lengths[(row, col, False)] = (
                        number_length,
                        *self.v_clues[self.v_clues_pos[row][col]],
                    )
        self.number_tier_one = len(self.tier_one_lengths.keys())
        self.all_children_possible = dict()
        self.all_children_possible_count = dict()
        self.all_children_pos = list(self.tier_one_lengths.keys())
        while True:
            try:
                with open(f"{self.name}_crossnumber.json", "r") as f:
                    numbers = json.load(f)
                    for x in self.tier_one_lengths.keys():
                        self.all_children_possible[x] = [
                            n
                            for n in numbers[self.tier_one_lengths[x][1]]
                            if len(str(n)) == self.tier_one_lengths[x][0]
                        ]
                        self.all_children_possible_count[x] = len(
                            self.all_children_possible[x]
                        )
                break
            except IOError:
                self.max_lengths = dict()
                for x in self.tier_one_lengths.keys():
                    if self.max_lengths.get(self.tier_one_lengths[x][1]) == None:
                        self.max_lengths[
                            self.tier_one_lengths[x][1]
                        ] = self.tier_one_lengths[x][0]
                    else:
                        self.max_lengths[self.tier_one_lengths[x][1]] = max(
                            self.max_lengths[self.tier_one_lengths[x][1]],
                            self.tier_one_lengths[x][0],
                        )
                with open(f"{self.name}_crossnumber.json", "w") as f:
                    numbers_dict_calculated = dict()
                    for x in self.max_lengths.keys():
                        numbers_dict_calculated[x] = NUMBERS_DICT[x](
                            10 ** self.max_lengths[x]
                        )
                    json.dump(numbers_dict_calculated, f)

        self.all_children_pos = sorted(
            self.all_children_pos,
            key=lambda item: self.all_children_possible_count[item],
        )

        self.all_children_possible = dict(
            sorted(
                self.all_children_possible.items(),
                key=lambda item: len(item[1]),
            )
        )
        self.all_children_possible_count = dict(
            sorted(self.all_children_possible_count.items(), key=lambda item: item[1])
        )
        # print(self.all_children_possible_count)

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

    def safe_up_to(self, solution, position):
        self.clear()
        clues_overlapped = set()
        n = 0
        added = False
        for row in range(self.dim[0]):
            for col in range(self.dim[1]):
                if self.grid_outline[row][col] != 0:
                    self.values[row][col] = solution[n]
                    for clue in self.all_clues_per_pos[row][col]:
                        clues_overlapped.add(clue)
                    n += 1
                if n > position:
                    added = True

                    break
            if added:
                break
        # self.display()
        # print(clues_overlapped)
        for clue in clues_overlapped:
            # print(*clue, self.tier_one_lengths[clue][0])
            val = self.get_value(*clue, self.tier_one_lengths[clue][0])
            # print(val)

            if val != -1 and (
                val not in self.all_children_possible[clue]
                or val <= 10 ** (self.tier_one_lengths[clue][0] - 1)
            ):
                return False

        return True

    def backtrace(self):
        num_slots = sum([row.count(1) for row in self.grid_outline])
        solution = [None] * num_slots

        def solve_from(position):
            max_length = 0
            while True:
                if self.safe_up_to(solution, position):
                    if position >= num_slots - 1:
                        # We filled the last slot and everything is okay
                        return solution
                    position += 1
                    if position > max_length:
                        self.display()
                        print(position)
                        max_length = position
                    solution[position] = 0
                else:
                    # Backtrack. We might have to undo several slots, so....
                    while solution[position] == 9:
                        solution[position] = None
                        position -= 1
                    if position < 0:
                        break
                    solution[position] += 1
                print(position, end="", flush=False)
                self.clear()

            # We backtracked beyond the starting point, meaning we could not find
            # a valid value for the first slot, so no solution
            return None

        # With the iterative solution, I think you have to begin by priming the
        # solution list with the first value in the first slot.
        solution[0] = 0
        solution = solve_from(0)
        self.clear()
        n = 0
        added = False
        for row in range(self.dim[0]):
            for col in range(self.dim[1]):
                if self.grid_outline[row][col] != 0:
                    self.values[row][col] = solution[n]
                    n += 1
                if n > num_slots:
                    added = True

                    break
            if added:
                break
        self.display()

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


# board = CrossNumber(
#     "test",
#     """11111
#         11111
#         1xxxx""",
#     """1xxxx
#     2xxxx
#     xxxxx""",
#     """1xxx2
#     xxxxx
#     xxxxx""",
#     """1. triangle
#     2. triangle""",
#     """1. integer
#     2. integer""",
# )


# board.values = [[1, 0, 0, 1, 1], [1, 0, 4, 4, 0], [None, None, None, None, None]]

# print(board.is_possible(0, 0, False, 115))
# board.values = [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, None, None, None, None]]
# print(board.get_value(0, 0, 5, True))
# board.backtrace()


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
         8. integer
         11. octahedral
         16. super4
         18. A053873
         20. strobogrammatic
         21. pentagonal
         23. trimorphic
         24. triangle
         26. tetradic
         28. pentagonal
         30. octahedral
         31. quartan
         32. perrin
         34. pentagonal
         37. emirp
         38. tetrahedral""",
)

board.backtrace()
