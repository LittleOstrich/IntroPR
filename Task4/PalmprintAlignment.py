import cv2
from scipy.ndimage import convolve

import numpy as np

# Can one do the exercise with less than 10 magic numbers?
# Magic number count
# binary images: 0 is black, 1 is white


# for debugging 
def myPrint(image, title="myprint"):
    import pylab as plt
    plt.title(title)
    plt.imshow(image, 'gray')
    plt.show()


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
    binary_values = np.count_nonzero(img == 0) + np.count_nonzero(img == 1)
    return binary_values == img.size


def is_in_image(p, width=320, height=240):
    return p[1] >= 0 and p[1] < width and p[0] >= 0 and p[0] < height


def trace(img, width=320, height=240):
    in_image = lambda y, x : x > 0 and x < width and y > 0 and y < height
    params = np.array([[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]])
        
    traced_img = np.zeros((height, width))
    for i in range(height):
        for j in range(width):
            there_is_black = 0
            there_is_white = 0
            for x in params:
                    nbh_x, nbh_y = i + x[0], j + x[1]
                    if in_image(nbh_x, nbh_y):
                        if(img[nbh_x, nbh_y] == 0):
                            there_is_black = 1
                        elif(img[nbh_x, nbh_y] == 1):
                            there_is_white = 1
                        else: 
                            print(img[nbh_x, nbh_y])
                            assert(False)  # we only care about binary images
                    if(there_is_black and there_is_white):
                        traced_img[i, j] = 1
    return traced_img


def get_edges(first_col, height=240):
    l = list()
    for i in range(1, height):
        if(first_col[i - 1] != first_col[i]):
            l.append(i)
    assert(len(l) in [10, 11, 12])  # Magic number number 6
    return l


def getNeighbours(img, pixel, width=320, height=240):
#    params = np.array([[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]])
    params = np.array([[0, -1], [-1, 0], [1, 0], [0, 1]])

    nbs = list()
    for p in params:
        nbs.append([pixel[0] + p[0], pixel[1] + p[1]])
    return nbs


def contains_point(x, lx):
    for t in lx:
        if x[0] == t[0] and x[1] == t[1] : return True
    return False


def is_white(p, img):
    return img[p[0], p[1]] == 1

        
# Todo: cleanse the scepticism that this method does not work...
def flood_crawl(img, y, x, width=320, height=240):
    area = list()
    unchecked = list()
    progress = 0
    unchecked.append((y, x))
    while(progress != len(unchecked)):
        current_pixel = unchecked[progress]
        progress = progress + 1
        area.append(current_pixel)
        nbs = getNeighbours(img, current_pixel)
        for z in nbs:
            # print(z)
            if is_in_image(z):
                if contains_point(z, area) == False:
                    if contains_point(z, unchecked) == False:
                        if is_white(z, img) == False: 
                            unchecked.append(z)
    print(area)
    return area       


# TODO: Make sure the results make sense...
def compute_center_of_area(A):
    X, Y, C = 0., 0., 0.
    for p in A:
        Y = Y + p[0]
        X = X + p[1]
        C = C + 1
    wx = X / C
    wy = Y / C
    print(wx, wy)
    return int(wy), int(wx)


def color_image_white(img, area):
    for p in area:
        img[p[0], p[1]] = 1
    return img


def decide_on_ks(img, width=320, height=240):
    
    edges = get_edges(img[:, 0], height)
    if len(edges) == 12 :
        y1, y2, y3 = edges[1], edges[5], edges[9]
    elif len(edges) == 10:
        y1, y2, y3 = edges[1], edges[5], edges[9]
    else: assert(False)
    # print(edges)

    A1 = flood_crawl(img, y1 + 1, 0) 
    A2 = flood_crawl(img, y2 + 1, 0) 
    A3 = flood_crawl(img, y3 + 1, 0) 
    
    img = color_image_white(img, A1)
    img = color_image_white(img, A2)
    img = color_image_white(img, A3)

    Y1, X1 = compute_center_of_area(A1)
    Y2, X2 = compute_center_of_area(A2)
    Y3, X3 = compute_center_of_area(A3)
    
    img[Y1, X1] = 0
    img[Y2, X2] = 0
    img[Y3, X3] = 0
    myPrint(img)
    
    fc_mp1, fc_mp2, fc_mp3 = [0, 0], [0, 0], [0, 0]
    if len(edges) == 12:
        fc_mp1 = (0 + edges[0]) / 2
        fc_mp2 = (edges[1] + edges[2]) / 2
        fc_mp3 = (edges[2] + edges[3]) / 2
    elif len(edges) == 10:
        fc_mp1 = (edges[0] + edges[1]) / 2
        fc_mp2 = (edges[2] + edges[4]) / 2
        fc_mp3 = (edges[4] + edges[5]) / 2
 
    [mx1, my1 ] = (Y1 - fc_mp1[1]) / (X1 - fc_mp1[0])   
    [mx2, my2 ] = (Y2 - fc_mp2[1]) / (X2 - fc_mp2[0])   
    [mx3, my3 ] = (Y3 - fc_mp3[1]) / (X3 - fc_mp3[0]) 
    
    k1, k2, k3 = [X1, Y1], [X2, Y2], [X3, Y3]
    for i in range(width):
        k1 = [X1, Y1] + i * [mx1, my1]
        if(img[int(np.round(k1[0])), int(np.round(k1[1]))] == 1):
            break
    for i in range(width):
        k2 = [X2, Y2] + i * [mx2, my2]
        if(img[int(np.round(k2[0])), int(np.round(k2[1]))] == 1):
            break
    for i in range(width):
        k3 = [X3, Y3] + i * [mx3, my3]
        if(img[int(np.round(k3[0])), int(np.round(k3[1]))] == 1):
            break
      
    return k1, k2, k3


def preProcessing(img):
    new_width = 320  # magic number number 1
    new_height = 240  # magic number number 2
    binary_map = np.zeros((new_height, new_width))  # usual definition
    # binary images: 0 is black, 1 is white

    # scale image to 320 x 240 px
    resized_image = cv2.resize(img, (new_width, new_height))
    
    # Apply a binary threshold (115 = cutOff)
    cutoff = 115  # magic number number 3
    for i in range(new_height):
        for j in range(new_width):
            if resized_image[i, j] >= cutoff:
                binary_map[i, j] = 1
    assert(is_binary(binary_map))
    # smoothing with gaussean filter
    sigma = 0.2  # magic number number 4
    ksize = 1  # # magic number number 5
    kernel = gauss_kernel(sigma, ksize)
    normalized_kernel = normalize(kernel)
    convolved_img = convolve(binary_map, normalized_kernel).astype(int)
    assert(is_binary(convolved_img))
    
    # find contours, get the largest and draw it
    traced_image = trace(convolved_img)
    # ## Trace the boundary of the holes between fingers.
    # ## Calculate the center of gravity of the holes and decide the key points | k1, k2, and k3.
    k1, k2, k3 = decide_on_ks(traced_image, new_width, new_height)
   
    # how does one find these key points? median-ish? Split the area into two areas, get its center, connect them with a line, 
    # extend the line until it hits the finger? sounds legit.

    # ## Line up k1 and k3 to get the Y-axis of the palmprint coordination system and
    # ## then  make  a  line  through  k2  and  perpendicular  to  Y-axis  to  determine  the
    # ## origin of the palmprint coordination system.

    # ## Rotate the image to place the Y-axis on the vertical direction

    return img
