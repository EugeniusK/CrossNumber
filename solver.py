import math
import json
import time
from number import *
import itertools
import ast
from functions import (
    FindTopOperatorOperand,
    FindSqrtArgument,
    FindIdentifiers,
    CountDivisions,
    isqrt,
    dsum,
    prime_factors,
    is_multiple,
    is_factor,
    is_pow,
    is_square,
    num_length,
)
from CrossNumber import RustedBoard


class Board:
    def __init__(self, dim):
        """
        Assumes validated arguments for all
        """
        self.dim = dim
        self.values = [[None for _ in range(self.dim[1])] for _ in range(self.dim[0])]

        # self.solution_index_pos_mapping = solution_index_pos_mapping

    def set_value(self, row, col, horizontal, value):
        if horizontal:
            for idx, digit in enumerate(map(int, str(value))):
                self.values[row][col + idx] = digit
        else:
            for idx, digit in enumerate(map(int, str(value))):
                self.values[row + idx][col] = digit

    def get_value(self, row, col, horizontal, length):
        if horizontal:
            return sum(
                [
                    self.values[row][col + x] * 10 ** (length - x - 1)
                    for x in range(length)
                ]
            )
        else:
            return sum(
                [
                    self.values[row + x][col] * 10 ** (length - x - 1)
                    for x in range(length)
                ]
            )

    def clear(self):
        self.values = [[None for _ in range(self.dim[1])] for _ in range(self.dim[0])]

    def is_possible(self, row, col, horizontal, value):
        if horizontal:
            for x, digit in enumerate(map(int, str(value))):
                if (
                    self.values[row][col + x] != digit
                    and self.values[row][col + x] is not None
                ):
                    return False
        else:
            for x, digit in enumerate(map(int, str(value))):
                if (
                    self.values[row + x][col] != digit
                    and self.values[row + x][col] is not None
                ):
                    return False
        return True

    def safe_up_to_tier_one(self, solution, position, all_pos, pos_all_possible):
        for s in range(position):
            self.set_value(
                *all_pos[s],
                pos_all_possible[all_pos[s]][solution[s]],
            )
            if not self.is_possible(
                *all_pos[s + 1],
                pos_all_possible[all_pos[s + 1]][solution[s + 1]],
            ):
                return False
        self.set_value(
            *all_pos[position],
            pos_all_possible[all_pos[position]][solution[position]],
        )


class CrossNumberSolver:
    def __init__(self, input_board: dict) -> None:
        self.start = time.perf_counter()
        self.name = input_board["name"]
        """Preprocessing of crossnumber
        
        Note:
            input_board has various fields and must follow a specific structure

            "name" (str): name of the crossnumber as referred to on PDF
            "dimensions" (dict): dimensions using "height" (int) and "width" (int) attributes
            "across clues" (dict): clues are identified by number (as on PDF) + "a"
            "down clues" (dict): clues are identified by number (as on PDF) + "d"

            individual clues are initially represented by

            "type" (str): broad classification of the clue - integer if unsure
            "eval" (str, optional): any condition given as a valid Python expression
            "multiple" (str, optional): a condition where the number must be a multiple of a constant or other numbers
                given as a valid Python expression
            "sum" (str, optional): a condition where the sum of the digits of the number must be a multiple of a constant or other numbers
                given as a valid Python expression
            "hint" (str, optional): hint for the given clue as on PDF

            then additional information added as needed by the program

            "pos" (tuple of (int, int, bool)): position of the clue 
            
        Args:
            input_board (dict): information about the crossnumber
        """

        if input_board.get("board layout") is None:
            raise AttributeError("Missing board layout data")
        else:
            if not isinstance(input_board.get("board layout"), list):
                raise AttributeError("Board layout data should be a 2D array")
            elif isinstance(input_board.get("board layout"), list) and not isinstance(
                input_board.get("board layout")[0], list
            ):
                raise AttributeError("Board layout data should be a 2D array")

        if input_board.get("dimensions") is None:
            raise AttributeError("Missing board dimensions")
        else:
            if not isinstance(input_board.get("dimensions"), dict):
                raise AttributeError("Board dimensions should be as a dict")
            else:
                if (
                    "height" not in input_board.get("dimensions").keys()
                    or "width" not in input_board.get("dimensions").keys()
                ):
                    raise AttributeError(
                        f"Board dimensions are missing {' and '.join([attr for attr in ['height', 'width'] if attr not in input_board.get('dimensions').keys()])}"
                    )

        if len(input_board.get("board layout")) != input_board.get("dimensions").get(
            "height"
        ):
            raise ValueError("Board height is incorrect")
        elif False in [
            True if len(row) == input_board.get("dimensions").get("width") else False
            for row in input_board.get("board layout")
        ]:
            raise ValueError("Board width is incorrect")
        self.dim = (
            input_board["dimensions"]["height"],
            input_board["dimensions"]["width"],
        )
        self.board_layout = input_board["board layout"]
        # provides a mapping from verbose position to exact position
        # example: 15a -> (0,0,True)
        # (row, col, horizontal?): (int, int, bool)
        self.verbose_pos_pos_mapping = dict()
        pos_verbose_pos_mapping = dict()
        for row in range(self.dim[0]):
            for col in range(self.dim[1]):
                if input_board["board layout"][row][col] > 0:
                    if (
                        str(input_board["board layout"][row][col]) + "a"
                        in input_board["across clues"].keys()
                    ):
                        self.verbose_pos_pos_mapping[
                            str(input_board["board layout"][row][col]) + "a"
                        ] = (row, col, True)
                        pos_verbose_pos_mapping[(row, col, True)] = (
                            str(input_board["board layout"][row][col]) + "a"
                        )
                    if (
                        str(input_board["board layout"][row][col]) + "d"
                        in input_board["down clues"].keys()
                    ):
                        self.verbose_pos_pos_mapping[
                            str(input_board["board layout"][row][col]) + "d"
                        ] = (row, col, False)
                        pos_verbose_pos_mapping[(row, col, False)] = (
                            str(input_board["board layout"][row][col]) + "d"
                        )

        # numbers in the cross number
        self.values = [[None for _ in range(self.dim[1])] for _ in range(self.dim[0])]

        # determine the length of nubmers in the crossnumber
        # and the type of nubmers it accepts
        # (row, col, horizontal?): length (int)
        verbose_pos_clue_lengths = dict()
        # (row, col, horziontal?): type of clue (str)
        verbose_pos_clue_type = dict()

        for verbose_pos, pos in self.verbose_pos_pos_mapping.items():
            verbose_pos_clue_lengths[verbose_pos] = 0
            length = 1
            if pos[2]:
                while (
                    pos[1] + length < self.dim[1]
                    and input_board["board layout"][pos[0]][pos[1] + length] != -1
                ):
                    length += 1
                verbose_pos_clue_lengths[verbose_pos] = length
                verbose_pos_clue_type[verbose_pos] = input_board["across clues"][
                    verbose_pos
                ]["type"]
            else:
                while (
                    pos[0] + length < self.dim[0]
                    and input_board["board layout"][pos[0] + length][pos[1]] != -1
                ):
                    length += 1
                verbose_pos_clue_lengths[verbose_pos] = length
                verbose_pos_clue_type[verbose_pos] = input_board["down clues"][
                    verbose_pos
                ]["type"]

        self.all_clues = input_board["across clues"] | input_board["down clues"]
        self.pos_all_possible = dict()
        while True:
            try:
                with open(
                    f"json/{self.name}_crossnumber.json", "r", encoding="utf8"
                ) as f:
                    numbers_possible = json.load(f)  # dictionary of all values
                    for verbose_pos, clue in (self.all_clues).items():
                        if self.all_clues[verbose_pos]["type"] not in NUMBERS_DICT:
                            raise KeyError(f"{clue['type']} is not a valid clue")
                        # only assign numbers that have same length as required on crossnumber
                        self.pos_all_possible[
                            self.verbose_pos_pos_mapping[verbose_pos]
                        ] = [
                            n
                            for n in numbers_possible[clue["type"]]
                            if 10 ** (verbose_pos_clue_lengths[verbose_pos] - 1)
                            <= n
                            < 10 ** verbose_pos_clue_lengths[verbose_pos]
                        ]
                break
            except FileNotFoundError:
                max_length = dict()
                for verbose_pos, length in verbose_pos_clue_lengths.items():
                    if max_length.get(self.all_clues[verbose_pos]["type"]) is None:
                        max_length[self.all_clues[verbose_pos]["type"]] = length
                    else:
                        max_length[self.all_clues[verbose_pos]["type"]] = max(
                            max_length[self.all_clues[verbose_pos]["type"]], length
                        )
                with open(
                    f"json/{self.name}_crossnumber.json", "w", encoding="utf8"
                ) as f:
                    numbers_dict_calculated = dict()
                    for clue, length in max_length.items():
                        numbers_dict_calculated[clue] = NUMBERS_DICT[clue](10**length)
                    json.dump(numbers_dict_calculated, f)

        self.count = dict()
        self.count["init"] = math.prod([len(x) for x in self.pos_all_possible.values()])
        print("init     ", round(math.log10(self.count["init"]), 2))

        # tier 1 - there are fixed possibilities
        # tier 2 - there are varying possibilities based on other factors beyond the number
        self.all_pos = self.verbose_pos_pos_mapping.keys()
        self.all_id_access_dsum_count = (
            ["a" + v for v in self.all_pos]
            + ["d" + v for v in self.all_pos]
            + ["n" + str(n) for n in range(10)]
        )

        self.t1_pos = []
        self.t2_pos = []
        self.t2_description = dict()

        self.t2_access_used = dict()
        self.t2_count_used = dict()
        self.t2_dsum_used = dict()

        find_operator_operand = FindTopOperatorOperand()
        find_sqrt_argument = FindSqrtArgument()
        find_identifiers = FindIdentifiers()
        for verbose, clue in (
            input_board["across clues"] | input_board["down clues"]
        ).items():
            pos = self.verbose_pos_pos_mapping[verbose]
            if clue.get("eval") is None:
                self.t1_pos.append(pos)
            else:
                self.t2_pos.append(pos)
                if clue["eval"].get("expr") is not None:
                    expr = clue["eval"]["expr"]
                elif clue["eval"].get("dsum") is not None:
                    expr = clue["eval"]["dsum"]
                elif clue["eval"].get("multiple") is not None:
                    expr = clue["eval"]["multiple"]

                if expr[0] != "[" and expr[-1] != "]":
                    expr = "[" + expr + "]"
                for verbose_pos in sorted(self.all_pos)[::-1]:
                    length = len(verbose_pos)
                    access_indexes = [
                        n
                        for n in range(len(expr) - length + 1)
                        if (expr[n : n + length] == verbose_pos)
                        and (
                            (
                                n > 0
                                and not expr[n - 1].isnumeric()
                                and expr[n - 1] != "d"
                            )
                            or n == 0
                        )
                    ]
                    idx = expr.find(verbose_pos)
                    added = 0
                    # insert "a" before some identifiers as 15a is invalid
                    # prevents same identifier twice - 5a, 15a
                    for idx in access_indexes:
                        expr = expr[: idx + added] + "a" + expr[added + idx :]
                        added += 1

                    if added != 0:
                        self.t2_access_used["a" + verbose_pos] = 0
                    if expr.find("d" + verbose_pos) != -1:
                        self.t2_dsum_used["d" + verbose_pos] = 0
                for n in range(10):
                    if "n" + str(n) in expr:
                        self.t2_count_used["n" + str(n)] = 0

                # using the expr, tries to find whether number is a multiple of something
                # or another expr is divisible by something
                # for example, 15a = 15d * 15 -> 15a is a multiple of 15
                # ALGORITHMIC DETERMINATION OF STUFF
                if clue["eval"].get("expr") is not None:
                    self.t2_description[pos] = expr
                elif clue["eval"].get("dsum") is not None:
                    clue_length = verbose_pos_clue_lengths[verbose]
                    self.t2_description[
                        pos
                    ] = f"[x for x in range({10 ** (clue_length-1)}, {10** clue_length}) if dsum(x) in {expr}]"
                elif clue["eval"].get("multiple") is not None:
                    clue_length = verbose_pos_clue_lengths[verbose]
                    self.t2_description[
                        pos
                    ] = f"[x for x in range({10 ** (clue_length-1)}, {10** clue_length}) if True in [x % ex == 0 for ex in {expr}]]"

            if clue.get("multiple") is not None:
                find_identifiers.visit(ast.parse(clue["multiple"]))
                if len(find_identifiers.identifiers) == 0:
                    if isinstance(eval(clue["multiple"]), list):  # multiple arguments
                        argument_arr = eval(clue["multiple"])
                        if len(argument_arr) == 2:
                            if argument_arr[0] is None:
                                arr = list(range(0, argument_arr[1] + 1))
                            elif argument_arr[1] is None:
                                arr = list(
                                    range(
                                        argument_arr[0],
                                        10 ** verbose_pos_clue_lengths[verbose],
                                    )
                                )
                            elif isinstance(argument_arr[0], int) and isinstance(
                                argument_arr[1], int
                            ):
                                arr = list(range(argument_arr[0], argument_arr[1] + 1))
                    elif isinstance(eval(clue["multiple"]), int):
                        self.pos_all_possible[pos] = is_multiple(
                            self.pos_all_possible[pos], eval(clue["multiple"])
                        )
                find_identifiers.clear()

            if clue.get("dsum") is not None:
                find_identifiers.visit(ast.parse(clue["dsum"]))
                if len(find_identifiers.identifiers) == 0:
                    if isinstance(eval(clue["dsum"]), list):  # multiple arguments
                        argument_arr = eval(clue["dsum"])
                        if len(argument_arr) == 2:
                            if argument_arr[0] is None:
                                arr = list(range(0, argument_arr[1] + 1))
                            elif argument_arr[1] is None:
                                arr = list(
                                    range(
                                        argument_arr[0],
                                        10 ** verbose_pos_clue_lengths[verbose],
                                    )
                                )
                            elif isinstance(argument_arr[0], int) and isinstance(
                                argument_arr[1], int
                            ):
                                arr = list(range(argument_arr[0], argument_arr[1] + 1))
                            self.pos_all_possible[pos] = [
                                x for x in self.pos_all_possible[pos] if dsum(x) in arr
                            ]
                    elif isinstance(eval(clue["dsum"]), int):
                        self.pos_all_possible[pos] = [
                            x
                            for x in self.pos_all_possible[pos]
                            if dsum(x) == eval(clue["dsum"])
                        ]
                find_identifiers.clear()
        # raise IndexError
        self.unfiltered_expr = []
        for pos, expr in self.t2_description.items():
            find_operator_operand.visit(ast.parse(expr))
            find_sqrt_argument.visit(ast.parse(expr))
            # returns (operator, left operand, right operand, index of constant)
            # top operand
            operands = find_operator_operand.operands
            sqrt_arguments = find_sqrt_argument.arguments
            find_operator_operand.clear()
            find_sqrt_argument.clear()

            # only one operand in expression
            if operands:
                if isinstance(operands[0], ast.Mult):
                    self.unfiltered_expr.append(
                        (operands[0], pos, operands[1], operands[2])
                    )
                elif isinstance(operands[0], (ast.Div, ast.FloorDiv)):
                    self.unfiltered_expr.append(
                        (operands[0], pos, operands[1], operands[2])
                    )
                elif isinstance(operands[0], ast.Pow):
                    self.unfiltered_expr.append(
                        (operands[0], pos, operands[1], operands[2])
                    )
            if sqrt_arguments:
                for argument in sqrt_arguments:
                    find_identifiers.visit(ast.parse(argument))
                    if (
                        len(find_identifiers.identifiers) == 1
                        and find_identifiers.identifiers[0][0] == "a"
                    ):
                        pos = self.verbose_pos_pos_mapping[
                            find_identifiers.identifiers[0][1:]
                        ]
                        verbose_pos = find_identifiers.identifiers[0][1:]
                        self.pos_all_possible[pos] = [
                            x
                            for x in self.pos_all_possible[pos]
                            if is_square(eval(argument, {"a" + verbose_pos: x}))
                        ]
                    find_identifiers.clear()

        for expr in self.unfiltered_expr:
            if (
                isinstance(expr[2], ast.Name)
                and isinstance(expr[3], ast.Constant)
                and expr[2].id in self.all_id_access_dsum_count
            ):
                if isinstance(expr[0], ast.Mult):
                    self.pos_all_possible[expr[1]] = is_multiple(
                        self.pos_all_possible[expr[1]], expr[3].value
                    )
                elif isinstance(expr[0], (ast.FloorDiv, ast.Div)):
                    self.pos_all_possible[
                        self.verbose_pos_pos_mapping[expr[2].id[1:]]
                    ] = is_multiple(
                        self.pos_all_possible[
                            self.verbose_pos_pos_mapping[expr[2].id[1:]]
                        ],
                        expr[3].value,
                    )
                elif isinstance(expr[0], ast.Pow):
                    self.pos_all_possible[expr[1]] = is_pow(
                        self.pos_all_possible[expr[1]],
                        expr[3].value,
                        verbose_pos_clue_lengths[pos_verbose_pos_mapping[expr[1]]],
                        False,
                    )
            elif (
                isinstance(expr[2], ast.Constant)
                and isinstance(expr[3], ast.Name)
                and expr[3].id in self.all_id_access_dsum_count
            ):
                if isinstance(expr[0], ast.Mult):
                    self.pos_all_possible[expr[1]] = is_multiple(
                        self.pos_all_possible[expr[1]], expr[2].value
                    )
                elif isinstance(expr[0], (ast.FloorDiv, ast.Div)):
                    self.pos_all_possible[expr[1]] = is_factor(
                        self.pos_all_possible[expr[1]],
                        expr[2].value,
                    )
                elif isinstance(expr[0], ast.Pow):
                    self.pos_all_possible[expr[1]] = is_pow(
                        self.pos_all_possible[expr[1]],
                        expr[2].value,
                        verbose_pos_clue_lengths[pos_verbose_pos_mapping[expr[1]]],
                        True,
                    )
        self.all_pos = sorted(self.t1_pos) + self.t2_pos

        self.all_possible_count = {
            x: len(self.pos_all_possible[x]) for x in self.all_pos
        }
        self.overlap_digits_optimise(verbose_pos_clue_lengths)

        self.board = RustedBoard(*self.dim)
        # self.board = Board(self.dim)

    def overlap_digits_optimise(self, verbose_pos_clue_lengths):
        all_possible_digits = [
            [[] for _ in range(self.dim[1])] for _ in range(self.dim[0])
        ]

        for verbose_pos, length in verbose_pos_clue_lengths.items():
            pos = self.verbose_pos_pos_mapping[verbose_pos]
            for l in range(length):
                possible_digits = set()
                for possible_value in self.pos_all_possible[pos]:
                    possible_digits.add(int(str(possible_value)[l]))
                if pos[2]:
                    all_possible_digits[pos[0]][pos[1] + l].append(possible_digits)
                else:
                    all_possible_digits[pos[0] + l][pos[1]].append(possible_digits)

        for row in range(self.dim[0]):
            for col in range(self.dim[1]):
                if len(all_possible_digits[row][col]) != 0:
                    all_possible_digits[row][col] = list(
                        set.intersection(*all_possible_digits[row][col])
                    )

        for verbose_pos, length in verbose_pos_clue_lengths.items():
            pos = self.verbose_pos_pos_mapping[verbose_pos]
            to_remove = []
            for possible_value in self.pos_all_possible[pos]:
                valid = True
                if pos[2]:
                    for l in range(length):
                        if (
                            int(str(possible_value)[l])
                            not in all_possible_digits[pos[0]][pos[1] + l]
                        ):
                            valid = False
                            break
                else:
                    for l in range(length):
                        if (
                            int(str(possible_value)[l])
                            not in all_possible_digits[pos[0] + l][pos[1]]
                        ):
                            valid = False
                            break

                if not valid:
                    to_remove.append(possible_value)

            for value in to_remove:
                self.pos_all_possible[pos].remove(value)

        self.all_pos = sorted(self.t1_pos) + self.t2_pos

        self.all_possible_count = {
            x: len(self.pos_all_possible[x]) for x in self.all_pos
        }
        self.count["reduced"] = math.prod(self.all_possible_count.values())
        self.clue_lengths = {
            self.verbose_pos_pos_mapping[verbose_pos]: length
            for verbose_pos, length in verbose_pos_clue_lengths.items()
        }
        self.max_position = 0
        print("reduced  ", round(math.log10(self.count["reduced"]), 2))

    def safe_up_to(self, solution, position):
        if (
            self.board.safe_up_to_tier_one(
                solution, position, self.all_pos, self.pos_all_possible
            )
            is False
        ):
            return False
        if position == len(self.pos_all_possible.keys()) - 1:
            if isinstance(self.board, RustedBoard):
                self.t2_count_used = {
                    "n" + str(digit): c
                    for digit, c in zip(range(10), self.board.get_digit_count())
                }
                self.t2_access_used = {
                    position: value
                    for position, value in zip(
                        list(self.t2_access_used.keys()),
                        self.board.get_value_multiple(
                            [
                                self.verbose_pos_pos_mapping[verbose]
                                + [
                                    self.clue_lengths[
                                        self.verbose_pos_pos_mapping[verbose]
                                    ]
                                ]
                                for verbose in list(self.t2_access_used.keys())
                            ]
                        ),
                    )
                }
                self.t2_dsum_used = {
                    position: value
                    for position, value in zip(
                        list(self.t2_dsum_used.keys()),
                        self.board.get_dsum_multiple(
                            [
                                tuple(
                                    [
                                        *self.verbose_pos_pos_mapping[verbose[1:]],
                                        self.clue_lengths[
                                            self.verbose_pos_pos_mapping[verbose[1:]]
                                        ],
                                    ]
                                )
                                for verbose in list(self.t2_dsum_used.keys())
                            ]
                        ),
                    )
                }
            elif isinstance(self.board, Board):
                for c in list(self.t2_count_used.keys()):
                    self.t2_count_used[c] = sum(
                        [x.count(int(c[1])) for x in self.board.values]
                    )
                for verbose_pos in list(self.t2_access_used.keys()):
                    self.t2_access_used[verbose_pos] = self.board.get_value(
                        *self.verbose_pos_pos_mapping[verbose_pos],
                        self.clue_lengths[self.verbose_pos_pos_mapping[verbose_pos]],
                    )
                for d_verbose_pos in list(self.t2_dsum_used.keys()):
                    self.t2_dsum_used[d_verbose_pos] = dsum(
                        self.board.get_value(
                            *self.verbose_pos_pos_mapping[d_verbose_pos[1:]],
                            self.clue_lengths[
                                self.verbose_pos_pos_mapping[d_verbose_pos[1:]]
                            ],
                        )
                    )
            for pos in self.t2_pos:
                if self.board.get_value(*pos, self.clue_lengths[pos]) not in eval(
                    self.t2_description[pos],
                    self.t2_count_used | self.t2_access_used | self.t2_dsum_used,
                ):
                    return False
        return True

    def backtrace(self, current_solution=None):
        number_all = len(self.all_pos)
        if current_solution is None:
            solution = [-1 for _ in range(number_all)]
            solution[0] = 0
            pos = 0
        else:
            solution = current_solution
            try:
                pos = solution.index(-1) - 1
            except:
                pos = len(solution) - 1

        def backtrace_from(position):
            c = 0

            while True:
                c += 1
                if self.safe_up_to(solution, position):
                    if position > self.max_position:
                        self.max_position = position
                    if position == number_all - 1:
                        print(c)

                        return solution
                    position += 1
                    solution[position] = 0
                else:
                    while (
                        solution[position]
                        == self.all_possible_count[self.all_pos[position]] - 1
                    ):
                        solution[position] = -1
                        position -= 1
                    if position < 0:
                        break
                    solution[position] += 1
                    self.board.clear()
            return None

        self.start = time.perf_counter()
        solution = backtrace_from(pos)
        self.board.clear()
        return solution

    def solve(self, threaded=False, solution=None):
        if isinstance(self.board, RustedBoard):
            solution = self.board.backtrace(
                [],
                self.all_pos,
                self.pos_all_possible,
                self.all_possible_count,
            )
            while not self.safe_up_to(solution, len(self.all_pos) - 1):
                solution[-1] += 1
                solution = self.board.backtrace(
                    solution,
                    self.all_pos,
                    self.pos_all_possible,
                    self.all_possible_count,
                )
            self.display(solution)
        else:
            solution = self.backtrace(solution)
            self.board.clear()
            for idx, val in enumerate(solution):
                self.board.set_value(
                    *self.all_pos[idx],
                    self.pos_all_possible[self.all_pos[idx]][val],
                )
            self.display(solution)

    def display(self, solution=None):
        """
        Outputs a graphical view of the board to STDIO
        """
        if solution is None:
            solution = [0] * len(self.all_pos)

        if isinstance(self.board, Board):
            values = self.board.values
        elif isinstance(self.board, RustedBoard):
            values = [
                self.board.values[x * self.dim[1] : (x + 1) * self.dim[1]]
                for x in range(self.dim[0])
            ]
        else:
            raise NotImplementedError("Missing class")
        for row in range(self.dim[0]):
            val = []
            for col in range(self.dim[1]):
                if values[row][col] is not None and values[row][col] != 255:
                    val.append(" " + str(values[row][col]) + " ")
                elif self.board_layout[row][col] != -1:
                    val.append("   ")
                else:
                    val.append("\u2588\u2588\u2588")
            print("\u2503".join(val))
            if row != self.dim[0] - 1:
                print("\u254B".join(["\u2501\u2501\u2501" for _ in range(self.dim[1])]))

        if isinstance(self.board, RustedBoard):
            c = self.board.get_digit_count()
        else:
            c = [sum([x.count(n) for x in self.board.values]) for n in range(10)]
        print("init     ", round(math.log10(self.count["init"]), 2))
        print("reduced  ", round(math.log10(self.count["reduced"]), 2))
        print(
            "factor of",
            round(
                (self.count["init"] / self.count["reduced"])
                / 10
                ** math.floor(math.log10(self.count["init"] / self.count["reduced"])),
                2,
            )
            * 10 ** math.floor(math.log10(self.count["init"] / self.count["reduced"])),
        )
        print("time     ", round(time.perf_counter() - self.start, 2), "seconds")
        print(
            "searched ",
            round(
                sum(
                    [
                        (solution[n] + 1)
                        * math.prod(list(self.all_possible_count.values())[n + 2 :])
                        for n in range(len(self.all_pos))
                        if solution[n] is not None
                    ]
                )
                / math.prod(list(self.all_possible_count.values())),
                3,
            )
            * 100,
            "percent",
        )
        print(solution)

        print(" ".join([str(d) for d in c]))


if __name__ == "__main__":
    print("hi")
