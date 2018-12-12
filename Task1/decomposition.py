'''
Created on 18 Oct 2017

@author: Benjamin
'''
import functools as ft
import numpy as np
import matplotlib.pyplot as plt

def createTriangleSignal(samples, frequency, kMax):
    s = np.linspace(0, 1, samples)
    for i in range(0, samples):
        l = 0
        for j in range(0, kMax):
            a = (8.0 / (np.pi ** 2)) * (-1) ** j * np.sin(2 * np.pi * (2 * j + 1) * frequency * s[i]) / (2 * j + 1) ** 2
            l = l + a
        s[i] = float(l)
        # print(s[i])
    plt.plot(np.linspace(0, 1, samples), s)
    plt.show()   
    
def createSquareSignal(samples, frequency, kMax):
    s = np.linspace(0, 1, samples)
    for i in range(0, samples):
        l = 0
        for j in range(1, kMax):
            a = (4.0 / np.pi) * np.sin(2 * np.pi * (2 * j - 1) * frequency * s[i]) / (2 * j - 1)
            l = l + a
        s[i] = float(l)
        # print(s[i])
    plt.plot(np.linspace(0, 1, samples), s)
    plt.show()    

    
    
def createSawtoothSignal(samples, frequency, kMax, amplitude):
    s = np.linspace(0, 1, samples)
    for i in range(0, samples):
        l = amplitude / 2
        for j in range(1, kMax):
            a = (amplitude / np.pi) * np.sin(2 * np.pi * j * frequency * s[i]) / j
            l = l - a
        s[i] = float(l)
        # print(s[i])
    plt.plot(np.linspace(0, 1, samples), s)
    plt.show()    
