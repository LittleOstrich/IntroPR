'''
Created on 13 Dec 2018

@author: Benjamin
'''

from PalmprintAlignment import preProcessing
import cv2 as cv2
import functools as ft
import math as math
import matplotlib.pyplot as plt
import numpy as np

k = 8
samplingSize = 100

img1 = cv2.imread('Hand1.jpg', cv2.IMREAD_GRAYSCALE)

preProcessing(img1)
plt.imshow(img1, 'gray')

