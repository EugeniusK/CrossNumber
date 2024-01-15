from _ast import FloorDiv
import math
import json
import time
from typing import Any
from functions import *
import itertools
import ast
import multiprocessing


def isqrt(n):
    return math.isqrt(n)


def dsum(n):
    return sum([int(x) for x in str(n)])


def prime_factors(n):
    arr = []
    for x in prime_arr:
        if n % x == 0:
            arr.append(x)
        if x > n:
            break
    return arr


def is_multiple(a, n):
    """
    Returns values in arr that are multiples of n
    Args:
        "arr" (list or int)
        "n" (int)
    """
    return [x for x in a if x % n == 0]


def is_factor(a, n):
    """
    Returns values in arr that are factors of n
    Args:
        "arr" (list or int)
        "n" (int)
    """
    return [x for x in a if n % x == 0]


def is_pow(a, n, length, base):
    """
    Base indiciates whether or not n is base or exponent

    n ** 2 vs 2 ** n
    """
    arr = []
    if base:
        p = 0
        while n**p < 10**length:
            if n**p in a:
                arr.append(n**p)
            p += 1
    else:
        base = 0
        while base**n < 10**length:
            if base**n in a:
                arr.append(base**n)
            base += 1
    return arr


def is_square(n):
    return math.isqrt(n) ** 2 == n


class FindTopOperatorOperand(ast.NodeVisitor):
    def __init__(self):
        self.operands = ()

    def visit_BinOp(self, node):
        left = node.left
        right = node.right
        if self.operands == ():
            self.operands = (node.op, left, right)

    def clear(self):
        self.operands = ()


class FindSqrtArgument(ast.NodeVisitor):
    def __init__(self):
        self.arguments = []

    def visit_Call(self, node):
        # if node.func.attr == "isqrt":
        if isinstance(node.func, ast.Name):  # function with name
            if node.func.id in ["sqrt", "isqrt"]:
                # print(ast.dump(node), node.func.id)
                self.arguments.append(ast.unparse(node.args))

        elif isinstance(node.func, ast.Attribute):
            if node.func.attr in ["sqrt", "isqrt"]:
                # print(ast.dump(node), node.func.attr)
                self.arguments.append(ast.unparse(node.args))

    def clear(self):
        self.arguments = []


class FindIdentifiers(ast.NodeVisitor):
    def __init__(self):
        self.identifiers = []

    def visit_Name(self, node):
        self.identifiers.append(node.id)

    def clear(self):
        self.identifiers = []


class CountDivisions(ast.NodeVisitor):
    def __init__(self):
        self.divisions = 0

    def visit_Div(self, _):
        self.divisions += 1

    def visit_FloorDiv(self, _):
        self.divisions += 1


class CrossNumber:
    def __init__(self, input_board: dict) -> None:
        self.start = time.time()
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

    def set_value(self, row, col, horizontal, value):
        if horizontal:
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
        number_length = self.clue_lengths[(row, col, horizontal)]
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
                self.pos_all_possible[self.all_pos[s]][solution[s]],
            )
            if not self.is_possible(
                *self.all_pos[s + 1],
                self.pos_all_possible[self.all_pos[s + 1]][solution[s + 1]],
            ):
                return False
        self.set_value(
            *self.all_pos[position],
            self.pos_all_possible[self.all_pos[position]][solution[position]],
        )
        if position == len(self.pos_all_possible.keys()) - 1:
            for count in list(self.t2_count_used.keys()):
                self.t2_count_used[count] = sum(
                    [x.count(int(count[1])) for x in self.values]
                )
            for verbose_pos in list(self.t2_access_used.keys()):
                self.t2_access_used[verbose_pos] = self.get_value(
                    *self.verbose_pos_pos_mapping[verbose_pos],
                    self.clue_lengths[self.verbose_pos_pos_mapping[verbose_pos]],
                )
            for d_verbose_pos in list(self.t2_dsum_used.keys()):
                self.t2_dsum_used[d_verbose_pos] = dsum(
                    self.get_value(
                        *self.verbose_pos_pos_mapping[d_verbose_pos[1:]],
                        self.clue_lengths[
                            self.verbose_pos_pos_mapping[d_verbose_pos[1:]]
                        ],
                    )
                )
            for pos in self.t2_pos:
                if self.get_value(*pos, self.clue_lengths[pos]) not in eval(
                    self.t2_description[pos],
                    self.t2_count_used | self.t2_access_used | self.t2_dsum_used,
                ):
                    return False
        return True

    def backtrace(self, current_solution=None, limited=False):
        number_all = len(self.all_pos)
        if current_solution is None:
            solution = [None for _ in range(number_all)]
            solution[0] = 0
            pos = 0
        else:
            solution = current_solution
            pos = solution.index(None) - 1

        def backtrace_from(position):
            while True:
                if self.safe_up_to(solution, position):
                    if position > self.max_position:
                        print(
                            position,
                            round(time.time() - self.start, 2),
                            sum(
                                [
                                    (solution[n] + 1)
                                    * math.prod(
                                        list(self.all_possible_count.values())[n + 2 :]
                                    )
                                    for n in range(number_all)
                                    if solution[n] is not None
                                ]
                            )
                            / math.prod(list(self.all_possible_count.values())),
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

        self.start = time.time()
        solution = backtrace_from(pos)
        self.clear()
        return solution

    def solve(self, threaded=False, solution=None):
        if not threaded:
            solution = self.backtrace()
            self.clear()
            for idx, val in enumerate(solution):
                self.set_value(
                    *self.all_pos[idx],
                    self.pos_all_possible[self.all_pos[idx]][val],
                )
            self.display(solution)

            raise IndexError
        else:
            pool = multiprocessing.Pool()

            raise IndexError

    def display(self, solution=None):
        """
        Outputs a graphical view of the board to STDIO
        """
        if solution is None:
            solution = [0] * len(self.all_pos)
        for row in range(self.dim[0]):
            val = []
            for col in range(self.dim[1]):
                if self.values[row][col] is not None:
                    val.append(" " + str(self.values[row][col]) + " ")
                elif self.board_layout[row][col] != -1:
                    val.append("   ")
                else:
                    val.append("\u2588\u2588\u2588")
            print("\u2503".join(val))
            if row != self.dim[0] - 1:
                print("\u254B".join(["\u2501\u2501\u2501" for _ in range(self.dim[1])]))
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
        print("time     ", round(time.time() - self.start, 2), "seconds")
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
        print(n0, n1, n2, n3, n4, n5, n6, n7, n8, n9)
        print(solution)


if __name__ == "__main__":
    print("hi")
