from solver import CrossNumber

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
    x19xxx20xxxx
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
    xxxxx20xxxx
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
    19. integer [x for x in range(100,1000) if int(str(x)[1]) == 19-n9]
    20. factorial_diff
    21. integer sum 13
    22. cube
    23. integer [d15a]
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

board_yuichiro = CrossNumber(
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
        xxxxx8xxxxxx
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
        8. integer [int(((n7-2)*n**2-(n7-4)*n)/2) for n in range(100)]
        11. octahedral [int((n1-1)*(2*(n1-1)**2 + 1)/3)]
        16. super4
        18. A053873
        20. strobogrammatic
        21. pentagonal
        23. trimorphic
        24. triangle [int(n0*(n0+1)/2)]
        26. tetradic
        28. pentagonal
        30. octahedral
        31. quartan
        32. perrin
        34. pentagonal
        37. emirp
        38. tetrahedral""",
)


# board_liersch_patki = CrossNumber(
#     "liersch_patki",
#     """111x1111x1
#     1x1111x111
#     111xx111x1
#     1x1111x111
#     11x1xx1x11
#     x111x1111x
#     11x111xx11
#     1x11x1x111
#     111x1111x1
#     1x1111x1x1""",
#     """1xxx3xxxxx
#     xx7xxxx8xx
#     9xxxx10xxxx
#     xx11xxxx13xx
#     15xxxxxxx18x
#     x19xxx20xxxx
#     21xx22xxxx23x
#     xx25xxxx26xx
#     27xxx28xxxxx
#     xx29xxxxxxx""",
#     """1x2x3.4x5x6
#     xxxxxxxxxx
#     xxxxxxxxxx
#     xxx12xxxx14x
#     x16xxxx17xxx
#     xxxxx20xxxx
#     21xxxxxxxx24
#     xx25xxxx26xx
#     xxxx28xxxxx
#     xxxxxxxxxx""",
# )
