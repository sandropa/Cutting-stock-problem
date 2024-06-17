import numpy as np
import time
from tqdm import tqdm

'''
    Funkcije koje evaluiraju algoritme za razlicite inpute, i vracaju matricu koja 
    predstavlja performanse tih algoritama kako se inputi mijenjaju.
'''

def evaluiraj_algoritme(funkcije, d_max, L, n, broj_iter=10, broj_ponavljanja=1, L_step=0, n_step=0, d_step=0):
    '''
        a vektor n cijelih broj izmedju 1 i 100
        L je cijeli broj

        L se povecava (ako L povecam i isto toliko i a povecam, nisam nista uradio)
        n se povecava
        d_max takodjer ima smisla da se povecava

        (parametri L_step, n_step, d_step)

        ne raisea nista, samo returna None i prije toga printa primjer na kojem su dali razlicite rezultate,
        i koji su
    '''
    mat = np.zeros((len(funkcije), broj_iter, broj_ponavljanja)) 
    # mat[x, y, z] predstavlja mjerenja funkcije x, u trenutku y, po z-ti put

    for i in tqdm(range(broj_iter)):
        for j in range(broj_ponavljanja):
            a = np.random.randint(1, 101, size=n)
            d = np.random.randint(1, d_max + 1, size=n)
            rez_funkcije = None
            for k, f in enumerate(funkcije):
                pocetak = time.time()
                rez = f(a=a, d=d, L=L)
                kraj = time.time()
                vrijeme = (kraj - pocetak)
                if rez_funkcije is None:
                    rez_funkcije = rez

                if abs(rez - rez_funkcije) > 0.000001:
                    print("Neka funkcija daje nepravilan rezultat!!!")
                    print("Podaci o iteraciji: ")
                    print("- iteracija: ", i)
                    print("- ponavaljanje: ", j)
                    print("- funkcija: ", k)
                    print("- rez prije: ", rez_funkcije)
                    print("- rez ove funkcije: ", rez)
                    print("Podaci o inputu u funkcije:")
                    print("- a: ", a)
                    print("- d: ", d)
                    print("- L: ", L)
                    return mat
                mat[k, i, j] = vrijeme
            np.save("trenutni_rezultati.npy", mat)
        L += L_step
        n += n_step
        d_max += d_step
    return mat


# TO DO: Dodati funkciju koja vraca i razliku u "optimalnom" rjesenju. (ovo ima smisla za aproksimativne algoritme
# kao sto je generating columns)