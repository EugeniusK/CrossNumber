import ast
import math
from number import prime_arr


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


def num_length(n):
    if 0 <= n < 10:
        return 1
    elif 10 <= n < 100:
        return 2
    elif 100 <= n < 1000:
        return 3
    elif 1000 <= n < 10000:
        return 4
    elif 10000 <= n < 100000:
        return 5
    elif 100000 <= n < 1000000:
        return 6
    elif 1000000 <= n < 10000000:
        return 7
    elif 10000000 <= n < 100000000:
        return 8
    else:
        raise NotImplementedError("Beyond implemented size")
