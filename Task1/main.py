'''
Created on 18 Oct 2017

@author: Benjamin
'''

import calculation
import chirp
import decomposition

class Main(object):

    def __init__(self, params):
        print("Hello World!")

def main():
    print("Hello world, corrector! Feel free to uncomment!")
    
    # calculation.pqsolver(0,1) # throw assertion error, only floats allowed 
    # print(calculation.pqsolver(1,0))
    # print(calculation.pqsolver(1,0))
    # chirp.testLinearChirp()
    # chirp.testExponentialChirp()
    
    # decomposition.createTriangleSignal(200, 2, 10000)
    # decomposition.createSquareSignal(200, 2, 10000)
    # decomposition.createSawtoothSignal(200, 2, 10000, 1)

    
    

if __name__ == "__main__": main()
