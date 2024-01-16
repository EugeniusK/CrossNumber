from boards import *

board_yuichiro.solve()
# board_yuichiro.solve(
#     threaded=False,
#     solution=[
#         0,
#         0,
#         2,
#         0,
#         1,
#         4,
#         2,
#         4,
#         1,
#         29,
#         4,
#         0,
#         3,
#         2,
#         13,
#         4,
#         2,
#         1,
#         3,
#         1,
#         7,
#         31,
#         4,
#         3,
#         2,
#         0,
#         0,
#         1,
#         2,
#         18,
#         None,
#         None,
#         None,
#         None,
#         None,
#         None,
#         None,
#         None,
#         None,
#         None,
#         None,
#         None,
#         None,
#         None,
#         None,
#         None,
#         None,
#         None,
#     ],
# )
board_ryder.backtrace()
# board_liersch_patki.backtrace()
# [0, 0, 2, 0, 1, 4, 2, 4, 1, 29, 4, 0, 3, 2, 13, 4, 2, 1, 3, 1, 7, 31, 4, 3, 2, 0, 0, 1, 2, 19, 0, 3, 1, 3, 2, 1,0,0,0,0,0,0, 0,0,0,0,0,0]


tmp = [
    0,
    0,
    2,
    0,
    1,
    4,
    2,
    4,
    1,
    29,
    4,
    0,
    3,
    2,
    13,
    4,
    2,
    1,
    3,
    1,
    7,
    31,
    4,
    3,
]
# count_arr = list(self.all_possible_count.values())
#             product_arr = [
#                 math.prod(count_arr[0:x]) for x in range(2, len(self.all_pos))
#             ]
#             print(product_arr, len(count_arr))
#             n = 0
#             while n < len(product_arr):
#                 if product_arr[n] > 100:
#                     break
#                 n += 1
#             print(n)

#             init_solutions = []
#             for t in itertools.product(*[range(x) for x in count_arr[0 : n + 1]]):
#                 init_solutions.append([*t] + [None] * (len(self.all_pos) - n - 1))
#             print(len(init_solutions[0]), len(self.all_pos))

#             with Pool(processes=2) as pool:
#                 # print "[0, 1, 4,..., 81]"
#                 it = pool.map(
#                     self.backtrace,
#                     zip(init_solutions, [True] * len(init_solutions)),
#                 )
#                 print(list(it))
