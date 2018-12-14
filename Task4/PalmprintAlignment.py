import cv2
from notebook.tests.selenium.utils import new_window
from scipy.ndimage import convolve

import numpy as np

# Can one do the exercise with less than 10 magic numbers?
# Magic number count


def normalize(matrix):
    s = 0
    width = len(matrix)
    height = len(matrix[0])
    for i in range(width):
        for j in range(height):
            s = s + matrix[i, j]
    normalized_matrix = matrix / s
    return normalized_matrix


def gauss_kernel(sigma, ksize):
    k = ksize
    kernel = np.zeros((2 * k + 1, 2 * k + 1))
    f1 = 2 * sigma * sigma
    f2 = 1.0 / (np.pi * f1)
    for i in range(1, 2 * k + 2):
        for j in range(1, 2 * k + 2):
            x = -1 * (((i - (k + 1)) ** 2) + (j - (k + 1)) ** 2) / (f1)
            kernel[i - 1, j - 1] = f2 * np.exp(x)
    return kernel


def is_binary(img, width=320, height=240):
    for i in range(width):
        for j in range(height):
                if(img[i, j] == 0 or img[i, j] == 1):
                    return False
    return True


def is_in_image(x, y, width=320, height=240):
    return x > 0 and x < width and y > 0 and y < height


def trace(img, width=320, height=240):
    in_image = lambda x, y: x > 0 and x < width and y > 0 and y < height
    params = np.array([[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]])
        
    traced_img = np.zeros((width, height))
    for i in range(width):
        for j in range(height):
            there_is_black = 0
            there_is_white = 0
            for x in params:
                    nbh_x, nbh_y = i + x[0], j + x[1]
                    if in_image(nbh_x, nbh_y):
                        if(img[nbh_x, nbh_y] == 0):
                            there_is_black = 1
                        elif(img[nbh_x, nbh_y] == 0):
                            there_is_white = 1
                        else: assert(False)  # we only care about binary images
                    if(there_is_black and there_is_white):
                        traced_img[i, j] = 1
    return traced_img


def get_edges(first_col, height=240):
    l = list()
    for i in range(1, height):
        if(first_col[i - 1] != first_col[i]):
            l.append(i)
    assert(len(l) == 4 or len(l) == 5)  # Magic number number 6
    return l


def getNeighbours(img, x, y, width=320, height=240):
    params = np.array([[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]])
    nbs = list()
    for p in params:
        if is_in_image(x + p[0], y + p[1]): 
            if(img[x + p[0], y + p[1]] == 1): continue
            else: nbs.add(p)
    return nbs

        
# Todo: cleanse the scepticism that this method does not work...
def flood_crawl(img, x, y, width=320, height=240):
    area = list()
    img_copy = img[:, :]
    unchecked = list()
    progress = 0
    unchecked.append(x)
    while(progress != len(unchecked)):
        current_pixel = list.index(progress)
        progress = progress + 1
        nx, ny = current_pixel[0], current_pixel[1]
        img_copy[nx, ny] = 1
        area.append([nx, ny])
        nbs = getNeighbours(img_copy, nx, ny)
        for z in nbs:
            unchecked.append(z)
    return area       


def give_me_the_areas(img, width=320, height=240):
    
    edges = get_edges(img[0, :], height)
    
    # yes, we the square brackets
    [y1, y2, y3] = [0, edges[1], edges[3]] if len(edges) == 4 else [edges[0], edges[2], edges[4]]  
    A1 = flood_crawl(img, 0, y1 + 1) 
    A2 = flood_crawl(img, 0, y2 + 1) 
    A3 = flood_crawl(img, 0, y3 + 1) 
    

def preProcessing(img):

    new_width = 320  # magic number number 1
    new_height = 240  # magic number number 2
    binary_map = np.zeros((new_width, new_height))
    
    # scale image to 320 x 240 px
    cv2.resize(img, (new_width, new_height))
    
    # Apply a binary threshold (115 = cutOff)
    cutoff = 115  # magic number number 3
    for i in range(new_width):
        for j in range(new_height):
            if img[i, j] >= cutoff:
                binary_map = 1
    assert(is_binary(binary_map))
    
    # smoothing with gaussean filter
    sigma = 0.2  # magic number number 4
    ksize = 1  # # magic number number 5
    kernel = gauss_kernel(sigma, ksize)
    normalized_kernel = normalize(kernel)
    convolved_img = convolve(binary_map, normalized_kernel).astype(int)
    assert(is_binary(convolved_img))
    
    # find contours, get the largest and draw it
    traced_image = trace(img)

    # ## Trace the boundary of the holes between fingers.
    # Just give me the interesting areas...
    A1, A2, A3 = give_me_the_areas(img, new_width, new_height)
    # ## Calculate the center of gravity of the holes and decide the key points | k1, k2, and k3.

    # ## Line up k1 and k3 to get the Y-axis of the palmprint coordination system and
    # ## then  make  a  line  through  k2  and  perpendicular  to  Y-axis  to  determine  the
    # ## origin of the palmprint coordination system.

    # ## Rotate the image to place the Y-axis on the vertical direction

    return img
