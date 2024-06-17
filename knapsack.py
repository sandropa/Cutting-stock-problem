import numpy as np
from copy import copy

def knapsack(l, v, L):
    '''
        Pomocna funkcija za generating_columns.
        Rjesava cjelobrojni problem ruksaka. Velicine predmeta su l,
        vrijednosti su v, L je velicina ruksaka. Funkcija vraca par:
        vrijednost funkcije cilja, niz koji predstavlja rjesenje. n je
        broj predmeta.
    '''
    
    n = len(l)

    DP = [[0, np.zeros(n)] for _ in range(L + 1)]

    for i in range(L + 1):
        for j in range(n):
            if l[j] <= i:
                rez_dp = DP[i - l[j]]
                if rez_dp[0] + v[j]  > DP[i][0]:
                    DP[i][0] = rez_dp[0] + v[j]
                    DP[i][1] = copy(rez_dp[1])
                    DP[i][1][j] += 1
    return DP[L]