from time import time
import numpy as np
from branch_and_bound import csp_branch_and_bound, csp_scipy_integrality
from generating_columns import csp_generating_columns

L = 110
a = np.array([20, 45, 50, 55, 75])
d = np.array([48, 35, 24, 10, 8])

#--------------------------------------------------------------

p = time()
rezultat = csp_branch_and_bound(L=L, a=a, d=d)
k = time()

print(f"Moj branch and bound: vrijeme {k-p}, rez {rezultat}")

#--------------------------------------------------------------

p = time()
rezultat = csp_scipy_integrality(L=L, a=a, d=d)
k = time()

print(f"Scipy integrality: vrijeme {k-p}, rez {rezultat}")

#--------------------------------------------------------------

p = time()
rezultat = csp_generating_columns(L=L, a=a, d=d)
k = time()

print(f"Generating columns: vrijeme {k-p}, rez {rezultat}")

#--------------------------------------------------------------