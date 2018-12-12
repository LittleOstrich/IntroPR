import numpy as np

def computeGeometricCloseness(i, j, x, y,sigma_d):
    #TODO: Compute the geometric closeness
    
    
    return 0
    
def computeEuclidianDistance(i, j, x, y):
    #TODO: Compute the euclidian distance
    
    
    return 0
   
def computeIntensityDistance(img, i, j, x, y):
    #TODO: Compute the intensity difference (absolute value)
    
    
    return  0

def computePhotometricDistance(img, i, j, x, y,sigma_r):
    #TODO: Compute the photometric distance
    
    return 0

def bilateralFilterHelper (img, x, y, width, sigma_d, sigma_r):
    # Compute the bilateral filtered image. Do not filter at the image boundaries!
    # Use the functions defined above
    # Hint: if (filterRunsOverBoundary) do this - else: apply algorithm
    
           
    return 0

def bilateralFilter(img, width, sigma_d, sigma_r):
    
    result = img[:]
    
    for  i in range(0,img.shape[1],1):
        for j in range(0,img.shape[0],1):    
                 
            result[j,i] = bilateralFilterHelper(img, i, j,width, sigma_d, sigma_r)
            
    return result
   
        