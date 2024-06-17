import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from tqdm import tqdm
from time import time
from branch_and_bound import csp_scipy_integrality
from generating_columns import csp_generating_columns
import math
from crtanje import crtaj


def cg_vs_scipy(d_max, L, n, broj_iter=10, broj_ponavljanja=1, L_step=0, n_step=0, d_step=0):
    '''
        Modifikovana funkcija iz evaluiraj_algoritme.py
        a vektor n cijelih broj izmedju 1 i 100
        L je cijeli broj

        L se povecava (ako L povecam i isto toliko i a povecam, nisam nista uradio)
        n se povecava
        d_max takodjer ima smisla da se povecava

        (parametri L_step, n_step, d_step)

        ne raisea nista, samo returna None i prije toga printa primjer na kojem su dali razlicite rezultate,
        i koji su
    '''

    mat = np.zeros((2, broj_iter, broj_ponavljanja))
    donje_granice = []
    postignute_fun = [] 
    stvarne_fun = []
    # mat[x, y, z] predstavlja mjerenja funkcije x, u trenutku y, po z-ti put

    for i in tqdm(range(broj_iter)):
        for j in range(broj_ponavljanja):
            a = np.random.randint(1, 101, size=n)
            d = np.random.randint(1, d_max + 1, size=n)

            pocetak = time()
            rez_cg = csp_generating_columns(a=a, d=d, L=L)
            kraj = time()
            mat[0, i, j] = kraj - pocetak

            pocetak = time()
            rez_scipy = csp_scipy_integrality(a=a, d=d, L=L)
            kraj = time()
            mat[1, i, j] = kraj - pocetak

            donje_granice.append(rez_cg[0])
            postignute_fun.append(rez_cg[1])
            stvarne_fun.append(rez_scipy)
    
        L += L_step
        n += n_step
        d_max += d_step
    return mat, donje_granice, postignute_fun, stvarne_fun

#------------------------------------------------------------------------------------------


def nacrtaj_cg_fun_razliku(d_max=50, L=150, n=7, broj_ponavljanja=30):
    rezultat_mjerenja = cg_vs_scipy(
        d_max=d_max, 
        L=L,
        n=n,
        broj_iter=1,
        broj_ponavljanja=broj_ponavljanja,
        n_step=0,
        L_step=0
    )

    donje = np.array(rezultat_mjerenja[1])
    postignute = np.array(rezultat_mjerenja[2])
    stvarne = np.array(rezultat_mjerenja[3])

    indeksi = np.argsort(stvarne)
    stvarne = stvarne[indeksi]
    postignute = postignute[indeksi]
    donje = donje[indeksi]

    plt.plot(stvarne, label="Optimalne vrijednosti")
    plt.plot(donje, label="Donje granice koje je dao column generation")
    plt.plot(postignute, label="Vrijednost koju nam je dao column generation")
    plt.legend()
    plt.show()