import numpy as np
from scipy.optimize import linprog
import math

'''
    Ovdje je implementacija funkcije koja rjesava cutting stock
    problem koristenjem branch and bound algoritma. Za fomulaciju
    cjelobrojnog programa koristimo onu fomulaciju sa cutting konfiguracijama.
    Implementirane su i pomocne funkcije koje generisu cutting konfiguracije
    i funkcija koja formulise cjelobrojni program. Funkcije se mogu lagano
    modifikovati tako da ne vracaju samo vrijednost konacne
    funkcije cilja, vec i vektor x koji je rjesenje i govori
    koje konfiguracije smo koristili.
'''

def cutting_konfiguracije(a, L, n, skup_konfiguracija, ti, tl, trenutna):
    '''
        Funkcija koja generise sve cutting konfiguracije. Podrazumijeva
        da je vektor a sortiran od najveceg do najmanjeg broja.
        Na pocetku joj proslijedjujemo prazan skup konfiguracija,
        kojeg ona modifikuje. Funkcija ne vraca nista.
    '''
    element_dodan = False # trenutna treba biti tuple
    for i in range(ti, n):
        if a[i] <= tl:
            element_dodan = True
            nova = trenutna[:i] + (trenutna[i] + 1,) + trenutna[i + 1:]
            cutting_konfiguracije(a, L, n, skup_konfiguracija, i, tl - a[i], nova)
    if not element_dodan:
        skup_konfiguracija.add(trenutna)


def cp_csp(a, d, L):
    '''
        Funkcija koja pravi matricu A koja predstavlja cjelobrojni program koji odgovara
        CSP problemu. Ova formulacija se zasniva na pravljenju svih mogucih validnih
        (i ujedno maksimalnih) konfiguracija cutova.
        Ne podrazumijeva da je a sortiran od najveceg do najmanjeg.
        Vraca: c, A_ub, b_ub (kao u scipy.optimize.linprog)
    '''
    # Sortirajmo a i d
    a = np.array(a)
    d = np.array(d)
    indeksi = np.argsort(-a)
    a = a[indeksi]
    d = d[indeksi]
    #----------------------
    S = set() 
    cutting_konfiguracije(a, L, len(a), S, 0, L, len(a)*(0,))

    # kolona predstavlja jedan cutting

    # Odredimo prvo c koje cemo vracati (funkcija cilja)
    # funkcija cilja je samo suma svih x-ova, dakle:
    c = np.ones(len(S))

    # ogranicenja b su d:  A x >= d
    b_ub = np.array(d)

    A_ub = (np.array(list(S))).T

    return c, A_ub, b_ub


def niz_cijelih(x):
    '''
        Pomocna funkcija za branch_and_bound.
        Vraca true ako je x niz cijelih brojeva, inace False.
    '''
    for xi in x:
        if abs(round(xi) - xi) > 1e-6:
            return False
    return True


def indeks_od_xi(x):
    '''
        Pomocna funkcija za branch_and_bound
        Vraca i-ti element iz x po nekom kriteriju.
        Na primjer, onaj koji je najdalje od tog da bude
        cijeli broj. Zbog numericke stabilnosti???
    '''
    ti = 0
    for i in range(len(x)):
        if abs(round(x[i])-x[i]) > abs(round(x[ti])-x[ti]):
            ti = i
    return ti


def branch_and_bound(c, A, b, tx, tfun): # Vraca double-ove, inicijalizacija je: tx = [[0]], tfun = [float('inf')]
    '''
        Vraca lp.x, lp.fun
        Podrazumijeva da saljemo linearan program koji IMA rjesenja.
        Ovo je okej jer ovu funkciju koristimo za cutting stock problem.
        Kao i scipy.optimize.linprog, trazi minimum funkcije.

        tx je lista sa jednim elementom! 
        (a taj jedan element je np ndarray)

        tx i tfun su shared state

        n je sirina matrice (len(x), tj len(c))

        Za rjesavanje linearnih relaksacija koristimo linprog funkciju
        iz scipy.optimize. 
    '''
    rez = linprog(c, A, b, method='highs') # probati highs-ipm i highs-ds
    # Provjerimo prvo da li ovo ima rjesenja!!!
    if not rez.success:
        return tx[0], tfun[0]

    # Prvo provjeravamo da li je relaksirano rjesenje
    # gore od t (trenutno najbolje)
    if rez.fun > tfun[0]: # rez.fun moze biti None!!??
        return tx[0], tfun[0]

    # Ako smo dobili sve cijele brojeve kao rjesenje, provjeravamo
    # da li je to bolje od tx i tfun, potencijalno updatujemo 
    # tx, tfun te ih returnamo
    if niz_cijelih(rez.x):
        if rez.fun < tfun[0]:
            tfun[0] = rez.fun
            tx[0] = rez.x
        return tx[0], tfun[0]

    # Ako postoji neki xi koji nije cijeli, radimo branching.
    # (i rj lin relaksacije nije bilo gore od trenutno
    # najboljeg rjesenja) Dakle, racunamo x1, fun1 i x2, fun2
    # rekurzivno. Ta rekurzija takodjer koristi isti shared
    # state kao do sada.

    i = indeks_od_xi(rez.x)
    
    # >=
    novi_red2 = np.zeros(len(c))
    novi_red2[i] = -1
    A2 = np.append(A, [novi_red2], axis=0)
    b2 = np.append(b, -math.ceil(rez.x[i]))
    branch_and_bound(c, A2, b2, tx, tfun)

    # <= 
    novi_red1 = np.zeros(len(c))
    novi_red1[i] = 1
    A1 = np.append(A, [novi_red1], axis=0)
    b1 = np.append(b, math.floor(rez.x[i]))
    branch_and_bound(c, A1, b1, tx, tfun)

    # Kako koriste isti shared state, dovoljno je:
    return tx[0], tfun[0]


def csp_branch_and_bound(a, d, L):
    '''
        Glavna funkcija koja koristi branch and bound za rjesavanje
        cutting stock problema. 
    ''' 

    trojka = cp_csp(a, d, L)
    TX = [[0]]
    TFUN = [float('inf')]
    rjesenje = branch_and_bound(trojka[0], -trojka[1], -trojka[2], TX, TFUN)
    return rjesenje[1]


def csp_scipy_integrality(a, d, L):
    '''
        Funkcija koja koristi scipy.optimize.linprog funkciju za 
        rjesavanje cutting stock problema koji je formulisan kao 
        cjelobrojni program sa onim cutting konfiguracijama. 
        Mislim da i linprog radi neku vrsu branch and bounda,
        ali mozemo ocekivati da je to dosta optimizovano, pa bi ova
        funkcija trebala imati bolje performanse od funkcije
        CSP_branch_and_bound.
    '''
    trojka = cp_csp(a, d, L)
    rjesenje = linprog(trojka[0], -trojka[1], -trojka[2], integrality=1)
    return rjesenje.fun