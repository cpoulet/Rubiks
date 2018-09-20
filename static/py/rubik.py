#!/usr/bin/env python3

import numpy as np
import sys
import re
from random import getrandbits, choice

Orange  = lambda s : "\033[1;48;5;208m" + s + "\033[1;0m"
White   = lambda s : "\033[1;30;107m" + s + "\033[1;0m"
Green   = lambda s : "\033[1;48;5;46m" + s + "\033[1;0m"
Red     = lambda s : "\033[1;48;5;196m" + s + "\033[1;0m"
Blue    = lambda s : "\033[1;48;5;4m" + s + "\033[1;0m"
Yellow  = lambda s : "\033[1;30;48;5;226m" + s + "\033[1;0m"

class Cube:

    def __init__(self):
        self.cube = np.arange(54).reshape(6,3,3)
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

    def swap4(a, b, c, d, k):
        if k == 1:
            return d.tolist(), a.tolist(), b.tolist(), c.tolist()
        else:
            return b.tolist(), c.tolist(), d.tolist(), a.tolist()

    def U(self, k=1):
        self.cube[4,:,:] = np.rot90(self.cube[4,:,:], -k)
        self.cube[:4,0,:] = np.roll(self.cube[:4,0,:], -k, axis=0)

    def D(self, k=1):
        self.cube[5,:,:] = np.rot90(self.cube[5,:,:], -k)
        self.cube[:4,2,:] = np.roll(self.cube[:4,2,:], k, axis=0)

    def L(self, k=1):
        self.cube[3,:,:] = np.rot90(self.cube[3,:,:], -k)
        self.cube[0,:,0], self.cube[5,2,:], self.cube[2,:,2], self.cube[4,0,:] = Cube.swap4(self.cube[0,:,0], self.cube[5,2,::-1], self.cube[2,:,2], self.cube[4,0,::-1], k)

    def R(self, k=1):
        self.cube[1,:,:] = np.rot90(self.cube[1,:,:], -k)
        self.cube[0,:,2], self.cube[4,2,:], self.cube[2,:,0], self.cube[5,0,:] = Cube.swap4(self.cube[0,::-1,2], self.cube[4,2,:], self.cube[2,::-1,0], self.cube[5,0,:], k)

    def F(self, k=1):
        self.cube[0,:,:] = np.rot90(self.cube[0,:,:], -k)
        self.cube[1,:,0], self.cube[5,:,0], self.cube[3,:,2], self.cube[4,:,0] = Cube.swap4(self.cube[1,:,0], self.cube[5,:,0], self.cube[3,:,2], self.cube[4,:,0], k)

    def B(self, k=1):
        self.cube[2,:,:] = np.rot90(self.cube[2,:,:], -k)
        self.cube[1,:,2], self.cube[4,:,2], self.cube[3,:,0], self.cube[5,:,2] = Cube.swap4(self.cube[1,:,2], self.cube[4,::-1,2], self.cube[3,::-1,0], self.cube[5,:,2], k)

    def __repr__(self):

#           36 37 38
#           39 40 41
#           42 43 44 
#   0  1  2  9 10 11 18 19 20 27 28 29
#   3  4  5 12 13 14 21 22 23 30 31 32
#   6  7  8 15 16 17 24 25 26 33 34 35
#           45 46 47
#           48 49 50
#           51 52 53

        def color(li):
            s = ''
            for i in li:
                if cube[i] < 9:
                    s += Orange('{:2d}'.format(cube[i]))
                elif 9 <= cube[i] and cube[i] < 18:
                    s += Green('{:2d}'.format(cube[i]))
                elif 18 <= cube[i] and cube[i] < 27:
                    s += Red('{:2d}'.format(cube[i]))
                elif 27 <= cube[i] and cube[i] < 36:
                    s += Blue('{:2d}'.format(cube[i]))
                elif 36 <= cube[i] and cube[i] < 45:
                    s += White('{:2d}'.format(cube[i]))
                elif 45 <= cube[i]:
                    s += Yellow('{:2d}'.format(cube[i]))
                s += ' '
            return s

        cube = self.cube.reshape(54)
        s = ' '*10 + color([36, 37, 38])
        s += '\n' + ' '*10 + color([39, 40, 41])
        s += '\n' + ' '*10 + color([42, 43, 44])
        s += '\n' + ' ' + color([0, 1, 2, 9, 10, 11, 18, 19, 20, 27, 28, 29])
        s += '\n' + ' ' + color([3, 4, 5, 12, 13, 14, 21, 22, 23, 30, 31, 32])
        s += '\n' + ' ' + color([6, 7, 8, 15, 16, 17, 24, 25, 26, 33, 34, 35])
        s += '\n' + ' '*10 + color([45, 46, 47])
        s += '\n' + ' '*10 + color([48, 49, 50])
        s += '\n' + ' '*10 + color([51, 52, 53])
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
    #r.mix(argv[1])

if __name__ == "__main__":
    C = Cube()
#    try:
#	    main(sys.argv)
#    except Exception as e:
#        print('Error : ' + str(e))
