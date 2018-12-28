import numpy as np


def computeFourier(img, u, v, width, height):
    res = 0
    f1 = (1.*u) / width 
    f2 = (1.*v) / height
    for m in range(width):
        for n in range(height):
            res = res + np.exp(-2j * np.pi * (m * f1 + n * f2))
    return res


def calcuateFourierParameters(img, k, sampling_steps):
    # TODO: calculate the fourier parameters
    height = len(img)
    width = len(img[0])
    
    fourier_transformed_image = np.shape((width, height))
    
    for u in range(height):
        for v in range(width):
            fourier_transformed_image[u, v] = computeFourier(img, u, v, width, height)
    # fft + magnitude

    # polar coordinate transformation
    def polar(r, theta):
        # calculation returning x,y in cartesian coordinates

        return 0, 0
    
    # energy calculations
    
    # ring like
    R = np.zeros(k, float)

    # fan like
    Theta_i = np.zeros(k, float)

    return R, Theta_i
