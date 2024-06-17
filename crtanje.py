import numpy as np
from matplotlib import pyplot as plt

def crtaj(mat, imena_funkcija=None, log_skala=False, figsize=None):
    '''
    mat[x, y, z] predstavlja mjerenja funkcije x, u trenutku y, po z-ti put
    crta medijane i kvartile
    '''
    xs = range(mat.shape[1])
    
    if figsize:
        plt.figure(figsize=figsize)
    if log_skala:
        plt.yscale('log')
    
    for i, funk_mjerenja in enumerate(mat):
        mediane = np.median(funk_mjerenja, axis=1)
        q25 = np.percentile(funk_mjerenja, 25, axis=1)
        q75 = np.percentile(funk_mjerenja, 75, axis=1)
        
        plt.plot(xs, mediane, label=f'Algoritam {i + 1}' if imena_funkcija is None else imena_funkcija[i])
        plt.fill_between(xs, q25, q75, alpha=0.2)

    plt.legend()
    plt.show()