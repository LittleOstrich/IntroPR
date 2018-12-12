'''
Created on 18 Oct 2017

@author: Benjamin
'''
from scipy.signal import chirp
import functools as ft
import numpy as np
import matplotlib.pyplot as plt


def createChirpSignal(samplingrate, duration, freqfrom, freqto, linear):
    sr = np.linspace(0, 1, num=samplingrate)    
    if linear:
        K = (freqto - freqfrom) / duration
        phase = 2 * np.pi * ((freqfrom + 0.5 * K * sr) * sr)
        return np.sin(np.array(phase))
    else: 
        K = (freqto / freqfrom) ** (1. / duration)
        phase = (2 * np.pi * freqfrom) * (K ** sr - 1) / np.log(K)
        return np.sin(np.array(phase))        

def testLinearChirp(): 
    A = createChirpSignal(200, 1, 1, 10, True)
    plt.plot(np.linspace(0, 1, num=200), A)
    plt.show()
    

def testExponentialChirp(): 
    A = createChirpSignal(200, 1, 1, 10, False)
    plt.plot(np.linspace(0, 1, num=200), A)
    plt.show() 
