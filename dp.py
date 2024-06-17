import numpy as np
import math

'''
    Ove funkcije NE rade na nekim primjerima. Idejno bi trebale
    da su uredu, i na nekim primjerima daju tacan rezultat.
    U slucaju da hocemo da koristimo ove funkcije, prvo moramo
    skontati zasto nekad ne daju tacan rezultat. Posto nisu kljucne
    za projekat, zasad su ostavljene ovako neispravne.
'''

def _cspdp(a, d, L, n, DP, tl, ti):
    if d in DP:
        return DP[d]
    
    napravljen_potez = False
    min_rez = float('inf')
    for i in range(ti, n):
        if a[i] <= tl and d[i] >= 1:
            napravljen_potez = True
            d_novi = d[:i] + (d[i] - 1,) + d[i + 1:]
            t_rez = _cspdp(a, d_novi, L, n, DP, tl - a[i], i)
            
            if t_rez < min_rez:
                min_rez = t_rez
    
    if napravljen_potez:
        DP[d] = min_rez
        return min_rez
    else:
        rez = 1 + _cspdp(a, d, L, n, DP, L, 0)
        DP[d] = rez
        return rez


def cutting_stock_dp(a, d, L):
    assert len(a) == len(d)
    a = np.array(a)
    d = np.array(d)
    sortirani_indeksi = np.argsort(-a)
    a = a[sortirani_indeksi]
    d = d[sortirani_indeksi]
    n = len(a)
    if n == 0:
        return 0
    sortirani_indeksi = np.argsort(-a)
    a = tuple(a[sortirani_indeksi])
    d = tuple(d[sortirani_indeksi])
    assert a[0] <= L
    DP = {n*(0,) : 0}
    
    return _cspdp(a, d, L, n, DP, 0, 0)