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


numbers = dict()
arr = []

MAX_SIZE = 1000000
SMALL_MAX_SIZE = 10000


def prime_numbers():
    # sophiegermain
    arr = []
    n = 0
    prime_arr = primes(2 * MAX_SIZE + 1)
    while n < MAX_SIZE:
        if n in prime_arr and 2 * n + 1 in prime_arr:
            arr.append(n)
        n += 1
    arr.remove(0) if 0 in arr else None
    numbers["sophiegermain"] = sorted(list(set(arr)))

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
    numbers["tetradic"] = arr

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
    numbers["quartan"] = arr

    # emirp
    arr = []
    n = 0
    while n < MAX_SIZE:
        if n in prime_arr and int(str(n)[::-1]) in prime_arr and int(str(n)[::-1]) != n:
            arr.append(n)
        n += 1
    arr.remove(0) if 0 in arr else None
    numbers["emirp"] = sorted(list(set(arr)))


def polygonal_numbers():
    # triangle
    arr = []
    n = 0
    while (n * (n + 1) // 2) < MAX_SIZE:
        arr.append(n * (n + 1) // 2)
        n += 1
    arr.remove(0) if 0 in arr else None
    numbers["triangle"] = sorted(list(set(arr)))

    # square
    arr = []
    n = 0
    while n**2 < MAX_SIZE:
        arr.append(n**2)
        n += 1
    arr.remove(0) if 0 in arr else None
    numbers["square"] = sorted(list(set(arr)))

    # pronic (n by n+1 rectangle)
    arr = []
    n = 0
    while n * (n + 1) < MAX_SIZE:
        arr.append(n * (n + 1))
        n += 1
    arr.remove(0) if 0 in arr else None
    numbers["pronic"] = sorted(list(set(arr)))

    # pentagonal
    arr = []
    n = 0
    while n * (3 * n - 1) // 2 < MAX_SIZE:
        arr.append(n * (3 * n - 1) // 2)
        n += 1
    arr.remove(0) if 0 in arr else None
    numbers["pentagonal"] = sorted(list(set(arr)))

    # hexagonal
    arr = []
    n = 0
    while n * (2 * n - 1) < MAX_SIZE:
        arr.append(n * (2 * n - 1))
        n += 1
    arr.remove(0) if 0 in arr else None
    numbers["hexagonal"] = sorted(list(set(arr)))

    # heptagonal
    arr = []
    n = 0
    while n * (5 * n - 3) // 2 < MAX_SIZE:
        arr.append(n * (5 * n - 3) // 2)
        n += 1
    arr.remove(0) if 0 in arr else None
    numbers["heptagonal"] = sorted(list(set(arr)))

    # octagonal
    arr = []
    n = 0
    while (2 * n + 1) ** 2 < MAX_SIZE:
        arr.append((2 * n + 1) ** 2)
        n += 1
    arr.remove(0) if 0 in arr else None
    numbers["octagonal"] = sorted(list(set(arr)))

    # nonagonal
    arr = []
    n = 0
    while n * (7 * n - 5) // 2 < MAX_SIZE:
        arr.append(n * (7 * n - 5) // 2)
        n += 1
    arr.remove(0) if 0 in arr else None
    numbers["nonagonal"] = sorted(list(set(arr)))

    # decagonal
    arr = []
    n = 0
    while n * (4 * n - 3) < MAX_SIZE:
        arr.append(n * (4 * n - 3))
        n += 1
    arr.remove(0) if 0 in arr else None
    numbers["decagonal"] = sorted(list(set(arr)))

    # hendecagonal
    arr = []
    n = 0
    while n * (9 * n - 7) // 2 < MAX_SIZE:
        arr.append(n * (9 * n - 7) // 2)
        n += 1
    arr.remove(0) if 0 in arr else None
    numbers["hendecagonal"] = sorted(list(set(arr)))

    # dodecagonal
    arr = []
    n = 0
    while 6 * n * (n - 1) + 1 < MAX_SIZE:
        arr.append(6 * n * (n - 1) + 1)
        n += 1
    arr.remove(0) if 0 in arr else None
    numbers["dodecagonal"] = sorted(list(set(arr)))

    # icosahedral
    arr = []
    n = 0
    while 10 * n**2 - 10 * n + 1 < MAX_SIZE:
        arr.append(10 * n**2 - 10 * n + 1)
        n += 1
    arr.remove(0) if 0 in arr else None
    numbers["icosahedral"] = sorted(list(set(arr)))


def polyhedral_numbers():
    # tetrahedral
    arr = []
    n = 0
    while n * (n + 1) * (n + 2) // 6 < MAX_SIZE:
        arr.append(n * (n + 1) * (n + 2) // 6)
        n += 1
    arr.remove(0) if 0 in arr else None
    numbers["tetrahedral"] = sorted(list(set(arr)))

    # octahedral
    arr = []
    n = 0
    while n * (2 * n**2 + 1) // 3 < MAX_SIZE:
        arr.append(n * (2 * n**2 + 1) // 3)
        n += 1
    arr.remove(0) if 0 in arr else None
    numbers["octahedral"] = sorted(list(set(arr)))


def recurrence_numbers():
    # padovan
    arr = [1, 0, 0]
    n = sum(arr[-3:-1])
    while n < MAX_SIZE:
        arr.append(n)
        n = sum(arr[-3:-1])

    numbers["padovan"] = sorted(list(set(arr)))

    # lucas
    arr = [2, 1]
    n = sum(arr[-2:])
    while n < MAX_SIZE:
        arr.append(n)
        n = sum(arr[-2:])

    numbers["lucas"] = sorted(list(set(arr)))

    # perrin
    arr = [3, 0, 2]
    n = sum(arr[-3:-1])
    while n < MAX_SIZE:
        arr.append(n)
        n = sum(arr[-3:-1])

    numbers["perrin"] = sorted(list(set(arr)))

    # tribonacci
    arr = [9, 12, -10]
    n = sum(arr[-3:])
    while n < MAX_SIZE:
        arr.append(n)
        n = sum(arr[-3:])

    numbers["tribonacci"] = sorted(list(set(arr)))

    # keith
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

    numbers["keith"] = arr


def super_numbers():
    # super3
    arr = []
    n = 0
    while n < MAX_SIZE:
        if "333" in str(3 * n**3):
            arr.append(n)
        n += 1
    arr.remove(0) if 0 in arr else None
    numbers["super3"] = sorted(list(set(arr)))

    # super4
    arr = []
    n = 0
    while n < MAX_SIZE:
        if "4444" in str(4 * n**4):
            arr.append(n)
        n += 1
    arr.remove(0) if 0 in arr else None
    numbers["super4"] = sorted(list(set(arr)))


def recreational_numbers():
    # kaprekar
    arr = []
    n = 0
    while n < MAX_SIZE:
        for a in range(0, n // 2 + 1):
            if n**2 == int(str(a) + str(n - a)) or n ** 2 == int(str(n - a) + str(a)):
                arr.append(n)
                break
        n += 1
    arr.remove(0) if 0 in arr else None
    numbers["kaprekar"] = sorted(list(set(arr)))

    # vampire
    arr = []
    n = 1000
    while n < SMALL_MAX_SIZE:
        list_n = sorted(list(str(n)))
        for x in range(1, math.isqrt(n) + 1):
            if n % x == 0 and sorted(list(str(x)) + list(str(n // x))) == list_n:
                arr.append(n)
                break
        n += 1
    arr.remove(0) if 0 in arr else None
    numbers["vampire"] = sorted(list(set(arr)))

    # untouchable
    arr = list(range(1, SMALL_MAX_SIZE + 1))

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

    for x in range(SMALL_MAX_SIZE**2):
        result = sigma(x) - x
        if result in arr:
            arr.remove(result)
    numbers["untouchable"] = sorted(list(set(arr)))

    # trimorphic
    arr = []
    n = 1
    while n < MAX_SIZE:
        if str(n**3)[-len(str(n)) :] == str(n):
            arr.append(n)
        n += 1
    arr.remove(0) if 0 in arr else None
    numbers["trimorphic"] = sorted(list(set(arr)))

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
        for row in [numdef(x, x) for x in range(1, len(str(n)))]
        for item in row
    ]
    arr.remove(0) if 0 in arr else None
    numbers["strobogrammatic"] = sorted(arr)


def generic_numbers():
    # integer
    numbers["integer"] = list(range(1, MAX_SIZE))


prime_numbers()
polygonal_numbers()
polyhedral_numbers()
recurrence_numbers()
super_numbers()
recreational_numbers()
generic_numbers()
print(numbers)
with open("numbers.json", "w") as f:
    json.dump(numbers, f)

"""


# 
arr = []
n = 0
while < MAX_SIZE:
    arr.append()
    n += 1
arr.remove(0) if 0 in arr else None
numbers[""] = sorted(list(set(arr)))

"""
