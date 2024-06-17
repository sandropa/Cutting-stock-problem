import numpy as np
from scipy.optimize import linprog
from knapsack import knapsack


def csp_generating_columns(a, d, L):
    '''
        Rjesava cutting stock problem metodom generating columns.
        Pocinje sa baznim kolonama takvim da se u svakom cuttingu koristi maksimalan broj jedne od duzina a.
        Zatim iterativno dodajemo kolone dok god knapsack daje kolone koje ce povecati vrijednost funkcije cilja za csp.
        Da bismo izracunali gradijent za dodavanje neke kolone, koristimo skalarni proizvod dualnih vrijednosti i te kolone.
        Ovo nam daje knapsack problem.  
    ''' 
    n = len(a)

    # min reduced cost racunamo kao min(1 - dualne_var * nova_kolona)

    # inicializacija baznih kolona
    kolone = []
    for i in range(n):
        nova_kol = np.zeros(n)
        nova_kol[i] += L // a[i]
        if nova_kol[i] == 0:
            print("Problem nema rjesenja: a[i] > L!")
            return
        kolone.append(nova_kol)
    A = np.column_stack(kolone)
    
    # inicijalizacija koeficijenata funkcije cilja
    c = np.ones(n)

    # linprog b = -d

    primal = linprog(c = c, A_ub = -A, b_ub = -d)
    # dualni_problem = linprog(c = d, A_ub = -A.T, b_ub = -c)
    # ne moramo odvojeno rjesavati dualni, mozemo iz linprog za primal 
    # izvuci dualne varijable, pogledati https://docs.scipy.org/doc/scipy-1.12.0/reference/generated/scipy.optimize.linprog.html
    
    x = primal.x
    fun = primal.fun
    dualne = primal.ineqlin.marginals

    # print(A, x, fun)
    # print("-------------------------------------------------------------")

    while True:
        rez_knapsack = knapsack(l = a, L = L, v = -dualne) # -dualne jer knapsack maksimizuje a mi hocemo minimizaciju
        # - rez_knapsack[1] @ dualne == rez_knapsack

        reduced_cost = 1 - rez_knapsack[0] 

        if reduced_cost >= 0:
            break

        A = np.column_stack((A, rez_knapsack[1]))
        c = np.append(c, 1)
        primal = linprog(c = c, A_ub = -A, b_ub = -d)

        x = primal.x
        if x[-1] < 0.00000001:
            break # ako smo dodali kolonu koju cemo odma izbacit, upast cemo u beskonacnu petlju
        fun = primal.fun
        dualne = primal.ineqlin.marginals
        A = A[:, x > 0] # python :) ; ova linija koda uklanja kolone koje ne ucestvuju u rjesenju (tj nisu bazne)
        x = x[x > 0] # ova uklanja medju x ovima one koji su bili nula
        c = np.ones(A.shape[1])
        # print(A, x, fun) # mozda bolje formatirati ovaj rezultat
        # print("-------------------------------------------------------------")

    # return A, x, fun # ako bi zeljeli ove cjelobrojne vrijednosti
    # ipak, nama za mjerenje performansi i da validiramo da je dobro rjesenje treba samo
    # fun i x, i fun kad x zaokruzimo

    donja_granica = fun
    x = np.ceil(x)
    postignuta_fun = np.sum(x)

    return donja_granica, postignuta_fun, x, A


def csp_fun_gen_columns(a, d, L):
    '''
        Jedna od funkcija koja mjeri performanse ocekuje da ova funkcija returna samo fun.
        Zato pravimo ovu funkciju.
    '''
    return csp_generating_columns(a, d, L)[1] # na mjestu 1 je postignuta vrijednost funkcije cilja
