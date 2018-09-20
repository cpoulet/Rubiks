#!/usr/bin/env python3

import numpy as np
import sys
import re
from random import getrandbits, choice

class Cube:

#         18 19 20
#       9 10 11 23
#    0  1  2 14 26
#    3  4  5 17
#    6  7  8

#    ORIENTATION FFS

    CROSS = [7,15,16,17,25]
    SIDE  = [3,4,5,6,7,8,12,13,14,15,16,17,21,22,23,24,25,26]

    def __init__(self):
        self.cube = np.arange(27).reshape(3,3,3)
        print('Starting...\n')
        print(self)

    def mix(self, sequence):
        print('\n...mixing...\n')
        while sequence:
            m = sequence.pop()
            if m[-1] == "2":
                sequence.append(m[0])
            k = 1 if m[-1] != "'" else -1
            getattr(self, m[0])(k)
        print(self)

    def randmix(self, n):
        li = ['F','R','U', 'B', 'L', 'D']
        sequence = []
        while (len(sequence) < n):
            m = choice(li)
            m = m if getrandbits(1) else m + "'"
            if sequence and sequence[-1] == m:
                sequence[-1] = m[0] + '2'
            else:
                sequence.append(m)
        self.mix(sequence)

    def U(self, k):
        self.cube[:,0,:] = np.rot90(self.cube[:,0,:], k)

    def D(self, k):
        self.cube[:,2,:] = np.rot90(self.cube[:,2,:], -k)

    def L(self, k):
        self.cube[:,:,0] = np.rot90(self.cube[:,:,0], -k)

    def R(self, k):
        self.cube[:,:,2] = np.rot90(self.cube[:,:,2], k)

    def F(self, k):
        self.cube[0,:,:] = np.rot90(self.cube[0,:,:], -k)

    def B(self, k):
        self.cube[2,:,:] = np.rot90(self.cube[2,:,:], k)

    def __repr__(self):
        cube = self.cube.reshape(27)
        s = ' '*6 + '{:2d} {:2d} {:2d}'.format(cube[18], cube[19], cube[20])
        s += '\n' + ' '*3 + '{:2d} {:2d} {:2d} {:2d}'.format(cube[9], cube[10], cube[11], cube[23])
        s += '\n' + '{:2d} {:2d} {:2d} {:2d} {:2d}'.format(cube[0], cube[1], cube[2], cube[14], cube[26])
        s += '\n' + '{:2d} {:2d} {:2d} {:2d}'.format(cube[3], cube[4], cube[5], cube[17])
        s += '\n' + '{:2d} {:2d} {:2d}'.format(cube[6], cube[7], cube[8])
        return s

    def __str__(self):
        return self.__repr__()

class RubikSolver:

    def __init__(self):
        self.sequence = []
        self.cube = Cube()

    def mix(self, sequence):
        for x in sequence.split():
            if re.match(r'^[FRUBLD][2\']?$', x):
                self.sequence.append(x)
            else:
                raise Exception('Parsing Error')
        self.cube.mix(self.sequence[::-1]);

def main(argv):
    if len(argv) != 2:
        raise Exception('Only one argument is needed.')
    r = RubikSolver()
    r.mix(argv[1])

if __name__ == "__main__":
    try:
	    main(sys.argv)
    except Exception as e:
        print('Error : ' + str(e))
