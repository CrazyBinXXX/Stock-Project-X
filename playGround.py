import collections
import numpy as np

def solve(matrix):
    n = len(matrix)
    m = len(matrix[0])
    zhengsums = {}
    fansums = {}
    for i in range(n):
        for j in range(m):
            diff = i - j
            thesum = i + j
            if diff in zhengsums:
                zhengsums[diff] += matrix[i][j]
            else:
                zhengsums[diff] = matrix[i][j]
            if thesum in fansums:
                fansums[thesum] += matrix[i][j]
            else:
                fansums[thesum] = matrix[i][j]
    ret = 0
    score_map = [[0] * m] * n
    for i in range(n):
        for j in range(m):
            score = zhengsums[i - j] + fansums[i + j] - matrix[i][j]
            if score > ret:
                ret = score
            score_map[i][j] = score
    a_max = 0
    b_max = 0
    for i in range(n):
        for j in range(m):
            # a situation
            if (i + j) % 2 == 0:
                score = score_map[i][j]
                if score > a_max:
                    a_max = score
            else:
                score = score_map[i][j]
                if score > b_max:
                    b_max = score
    ret = a_max + b_max
    return ret

