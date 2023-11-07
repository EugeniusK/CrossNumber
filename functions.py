import math, json


def primes(n):
    prime = [True for i in range(n + 1)]
    p = 2
    while p * p <= n:
        if prime[p] == True:
            for i in range(p * p, n + 1, p):
                prime[i] = False
        p += 1
    c = []

    for p in range(2, n):
        if prime[p]:
            c.append(p)
    return c


prime_arr = primes(1000000)

numbers = dict()
arr = []


def sophiegermain(MAX_SIZE):
    # sophiegermain
    arr = []
    n = 0
    while n < MAX_SIZE:
        if n in prime_arr and 2 * n + 1 in prime_arr:
            arr.append(n)
        n += 1
    arr.remove(0) if 0 in arr else None
    return arr


def tetradic(MAX_SIZE):
    # tetradic
    arr = []
    n = 0
    while n < MAX_SIZE:
        if (
            n in prime_arr
            and set(list(str(n))).intersection({"2", "3", "4", "5", "6", "7", "9"})
            == set()
            and str(n) == str(n)[::-1]
        ):
            arr.append(n)
        n += 1
    arr.remove(0) if 0 in arr else None
    return arr


def quartan(MAX_SIZE):
    # quartan
    arr = []
    n = 0
    while n < MAX_SIZE:
        tmp = 1
        while True:
            if tmp**4 > n:
                break
            if (
                n in prime_arr
                and math.isqrt(math.isqrt(n - tmp**4)) ** 4 + tmp**4 == n
            ):
                arr.append(n)
                break
            tmp += 1
        n += 1
    arr.remove(0) if 0 in arr else None
    return arr


def emirp(MAX_SIZE):
    # emirp
    arr = []
    n = 0
    while n < MAX_SIZE:
        if n in prime_arr and int(str(n)[::-1]) in prime_arr and int(str(n)[::-1]) != n:
            arr.append(n)
        n += 1
    arr.remove(0) if 0 in arr else None
    return arr


def triangle(MAX_SIZE):
    # triangle
    arr = []
    n = 0
    while (n * (n + 1) // 2) < MAX_SIZE:
        arr.append(n * (n + 1) // 2)
        n += 1
    arr.remove(0) if 0 in arr else None
    return arr


def square(MAX_SIZE):
    # square
    arr = []
    n = 0
    while n**2 < MAX_SIZE:
        arr.append(n**2)
        n += 1
    arr.remove(0) if 0 in arr else None
    return arr


def pronic(MAX_SIZE):
    # pronic (n by n+1 rectangle)
    arr = []
    n = 0
    while n * (n + 1) < MAX_SIZE:
        arr.append(n * (n + 1))
        n += 1
    arr.remove(0) if 0 in arr else None
    return arr


def pentagonal(MAX_SIZE):
    # pentagonal
    arr = []
    n = 0
    while n * (3 * n - 1) // 2 < MAX_SIZE:
        arr.append(n * (3 * n - 1) // 2)
        n += 1
    arr.remove(0) if 0 in arr else None
    return arr


def hexagonal(MAX_SIZE):
    # hexagonal
    arr = []
    n = 0
    while n * (2 * n - 1) < MAX_SIZE:
        arr.append(n * (2 * n - 1))
        n += 1
    arr.remove(0) if 0 in arr else None
    return arr


def heptagonal(MAX_SIZE):
    # heptagonal
    arr = []
    n = 0
    while n * (5 * n - 3) // 2 < MAX_SIZE:
        arr.append(n * (5 * n - 3) // 2)
        n += 1
    arr.remove(0) if 0 in arr else None
    return arr


def octagonal(MAX_SIZE):
    # octagonal
    arr = []
    n = 0
    while (2 * n + 1) ** 2 < MAX_SIZE:
        arr.append((2 * n + 1) ** 2)
        n += 1
    arr.remove(0) if 0 in arr else None
    return arr


def nonagonal(MAX_SIZE):
    # nonagonal
    arr = []
    n = 0
    while n * (7 * n - 5) // 2 < MAX_SIZE:
        arr.append(n * (7 * n - 5) // 2)
        n += 1
    arr.remove(0) if 0 in arr else None
    return arr


def decagonal(MAX_SIZE):
    # decagonal
    arr = []
    n = 0
    while n * (4 * n - 3) < MAX_SIZE:
        arr.append(n * (4 * n - 3))
        n += 1
    arr.remove(0) if 0 in arr else None
    return arr


def hendecagonal(MAX_SIZE):
    # hendecagonal
    arr = []
    n = 0
    while n * (9 * n - 7) // 2 < MAX_SIZE:
        arr.append(n * (9 * n - 7) // 2)
        n += 1
    arr.remove(0) if 0 in arr else None
    return arr


def dodecagonal(MAX_SIZE):
    # dodecagonal
    arr = []
    n = 0
    while 6 * n * (n - 1) + 1 < MAX_SIZE:
        arr.append(6 * n * (n - 1) + 1)
        n += 1
    arr.remove(0) if 0 in arr else None
    return arr


def icosahedral(MAX_SIZE):
    # icosahedral
    arr = []
    n = 0
    while 10 * n**2 - 10 * n + 1 < MAX_SIZE:
        arr.append(10 * n**2 - 10 * n + 1)
        n += 1
    arr.remove(0) if 0 in arr else None
    return arr


def tetrahedral(MAX_SIZE):
    # tetrahedral
    arr = []
    n = 0
    while n * (n + 1) * (n + 2) // 6 < MAX_SIZE:
        arr.append(n * (n + 1) * (n + 2) // 6)
        n += 1
    arr.remove(0) if 0 in arr else None
    return arr


def octahedral(MAX_SIZE):
    # octahedral
    arr = []
    n = 0
    while n * (2 * n**2 + 1) // 3 < MAX_SIZE:
        arr.append(n * (2 * n**2 + 1) // 3)
        n += 1
    arr.remove(0) if 0 in arr else None
    return arr


def padovan(MAX_SIZE):
    # padovan
    arr = [1, 0, 0]
    n = sum(arr[-3:-1])
    while n < MAX_SIZE:
        arr.append(n)
        n = sum(arr[-3:-1])

    return sorted(list(set(arr)))


def lucas(MAX_SIZE):
    arr = [2, 1]
    n = sum(arr[-2:])
    while n < MAX_SIZE:
        arr.append(n)
        n = sum(arr[-2:])

    return sorted(list(set(arr)))


def perrin(MAX_SIZE):
    arr = [3, 0, 2]
    n = sum(arr[-3:-1])
    while n < MAX_SIZE:
        arr.append(n)
        n = sum(arr[-3:-1])

    return sorted(list(set(arr)))


def tribonacci(MAX_SIZE):
    arr = [9, 12, -10]
    n = sum(arr[-3:])
    while n < MAX_SIZE:
        arr.append(n)
        n = sum(arr[-3:])

    return sorted(list(set(arr)))


def keith(MAX_SIZE):
    arr = []
    n = 10
    while n < MAX_SIZE:
        tmp_arr = [int(x) for x in str(n)]
        len_n = len(str(n))
        while tmp_arr[-1] < n:
            tmp_arr.append(sum(tmp_arr[-len_n:]))
        if n in tmp_arr:
            arr.append(n)
        n += 1

    return arr


def super3(MAX_SIZE):
    # super3
    arr = []
    n = 0
    while n < MAX_SIZE:
        if "333" in str(3 * n**3):
            arr.append(n)
        n += 1
    arr.remove(0) if 0 in arr else None
    return sorted(list(set(arr)))


def super4(MAX_SIZE):
    arr = []
    n = 0
    while n < MAX_SIZE:
        if "4444" in str(4 * n**4):
            arr.append(n)
        n += 1
    arr.remove(0) if 0 in arr else None
    return sorted(list(set(arr)))


def kaprekar(MAX_SIZE):
    # kaprekar
    arr = []
    n = 0

    def iskaprekar(n):
        # taken from geeksforgeeks
        if n == 1:
            return True

        # Count number of digits in square
        sq_n = n * n
        count_digits = 1
        while not sq_n == 0:
            count_digits = count_digits + 1
            sq_n = sq_n // 10

        sq_n = n * n  # Recompute square as it was changed

        # Split the square at different points and see if sum
        # of any pair of splitted numbers is equal to n.
        r_digits = 0
        while r_digits < count_digits:
            r_digits = r_digits + 1
            eq_parts = (int)(math.pow(10, r_digits))

            # To avoid numbers like 10, 100, 1000 (These are not
            # Kaprekar numbers
            if eq_parts == n:
                continue

            # Find sum of current parts and compare with n

            sum = sq_n // eq_parts + sq_n % eq_parts
            if sum == n:
                return True

        # compare with original number
        return False

    while n < MAX_SIZE:
        if iskaprekar(n):
            arr.append(n)
        n += 1
    arr.remove(0) if 0 in arr else None
    return sorted(list(set(arr)))


def vampire(MAX_SIZE):
    # vampire
    arr = []
    n = 1000
    while n < MAX_SIZE:
        list_n = sorted(list(str(n)))
        for x in range(1, math.isqrt(n) + 1):
            if n % x == 0 and sorted(list(str(x)) + list(str(n // x))) == list_n:
                arr.append(n)
                break
        n += 1
    arr.remove(0) if 0 in arr else None
    return sorted(list(set(arr)))


def untouchable(MAX_SIZE):
    # untouchable
    arr = list(range(1, MAX_SIZE + 1))

    def sigma(n):
        """
        Sum of divisors
        """
        divisors = []
        for x in range(1, math.isqrt(n) + 1):
            if n % x == 0:
                divisors.append(x)
                divisors.append(n // x)
        return sum(list(set(divisors)))

    for x in range(MAX_SIZE**2):
        result = sigma(x) - x
        if result in arr:
            arr.remove(result)
    return sorted(list(set(arr)))


def trimorphic(MAX_SIZE):
    arr = []
    n = 1
    while n < MAX_SIZE:
        if str(n**3)[-len(str(n)) :] == str(n):
            arr.append(n)
        n += 1
    arr.remove(0) if 0 in arr else None
    return sorted(list(set(arr)))


def strobogrammatic(MAX_SIZE):
    # strobogrammatic
    arr = []

    def numdef(n, length):
        if n == 0:
            return [""]
        if n == 1:
            return ["1", "0", "8"]

        middles = numdef(n - 2, length)
        result = []

        for middle in middles:
            if n != length:
                result.append("0" + middle + "0")

            result.append("8" + middle + "8")
            result.append("1" + middle + "1")
            result.append("9" + middle + "6")
            result.append("6" + middle + "9")
        return result

    arr = [
        int(item)
        for row in [numdef(x, x) for x in range(1, len(str(MAX_SIZE)))]
        for item in row
    ]
    arr.remove(0) if 0 in arr else None
    return sorted(arr)


def integer(MAX_SIZE):
    return list(range(1, MAX_SIZE))


NUMBERS_DICT = {
    "triangle": triangle,
    "square": square,
    "pronic": pronic,
    "pentagonal": pentagonal,
    "hexagonal": hexagonal,
    "heptagonal": heptagonal,
    "octagonal": octagonal,
    "nonagonal": nonagonal,
    "decagonal": decagonal,
    "dodecagonal": dodecagonal,
    "icosahedral": icosahedral,
    "tetrahedral": tetrahedral,
    "octahedral": octahedral,
    "padovan": padovan,
    "lucas": lucas,
    "perrin": perrin,
    "tribonacci": tribonacci,
    "keith": keith,
    "super3": super3,
    "super4": super4,
    "kaprekar": kaprekar,
    "vampire": vampire,
    "untouchable": untouchable,
    "strobogrammatic": strobogrammatic,
    "trimorphic": trimorphic,
    "integer": integer,
    "sophiegermain": sophiegermain,
    "tetradic": tetradic,
    "quartan": quartan,
    "emirp": emirp,
}
if __name__ == "__main__":
    print("main")
    print(untouchable(1000))
