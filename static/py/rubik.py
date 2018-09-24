#!/usr/bin/env python3

import numpy as np
import json
import sys
import re
from random import getrandbits, choice

Orange  = lambda s : "\033[1;48;5;208m" + s + "\033[1;0m"
White   = lambda s : "\033[1;30;107m" + s + "\033[1;0m"
Green   = lambda s : "\033[1;48;5;46m" + s + "\033[1;0m"
Red     = lambda s : "\033[1;48;5;196m" + s + "\033[1;0m"
Blue    = lambda s : "\033[1;48;5;4m" + s + "\033[1;0m"
Yellow  = lambda s : "\033[1;30;48;5;226m" + s + "\033[1;0m"

class Heuristic:

    def cross(cube):
        goal = [46,16,50,25,52,34,48,7]

        def errors(cube):
            #number of miss-placed face
            n = len(goal)
            for face in goal:
                if cube[face] == face:
                    n -= 1
            return n

        def manhattan(cube):
            return

        return errors(cube)

class State:
    def __init__(self, cube):
        self.cube = cube
        self.parent = None
#        print(self)

    def children(self, prev=False):
        moves = {'F','R','U', 'B', 'L', 'D'}
        antimoves = {'F','R','U', 'B', 'L', 'D'}
        if prev:
            if len(prev) == 1:
                antimoves.discard(prev)
            else:
                moves.discard(prev)
        return [getattr(State, 'get' + move)(self.cube.copy()) for move in moves] + [getattr(State, 'get' + move)(self.cube.copy(), -1) for move in antimoves]

    def goal(self, g):
        cube = self.cube.reshape(54)
        for x in g:
            if cube[x] != x:
                return False
        return True
    
    def __eq__(self, o):
        return self.cube == o.cube

    def __hash__(self):
        return ",".join(map(str, self.cube.reshape(54).tolist()))

#    def __repr__(self):
#        return State.print(self.cube)

    def __str__(self):
        return State.print(self.cube)

    def swap4(a, b, c, d, k):
        if k == 1:
            return d.tolist(), a.tolist(), b.tolist(), c.tolist()
        else:
            return b.tolist(), c.tolist(), d.tolist(), a.tolist()

    def getU(cube, k=1):
        cube[4,:,:] = np.rot90(cube[4,:,:], -k)
        cube[:4,0,:] = np.roll(cube[:4,0,:], -k, axis=0)
        return State(cube)

    def getD(cube, k=1):
        cube[5,:,:] = np.rot90(cube[5,:,:], -k)
        cube[:4,2,:] = np.roll(cube[:4,2,:], k, axis=0)
        return State(cube)

    def getL(cube, k=1):
        cube[3,:,:] = np.rot90(cube[3,:,:], -k)
        cube[0,:,0], cube[5,2,:], cube[2,:,2], cube[4,0,:] = State.swap4(cube[0,:,0], cube[5,2,::-1], cube[2,:,2], cube[4,0,::-1], k)
        return State(cube)

    def getR(cube, k=1):
        cube[1,:,:] = np.rot90(cube[1,:,:], -k)
        cube[0,:,2], cube[4,2,:], cube[2,:,0], cube[5,0,:] = State.swap4(cube[0,::-1,2], cube[4,2,:], cube[2,::-1,0], cube[5,0,:], k)
        return State(cube)

    def getF(cube, k=1):
        cube[0,:,:] = np.rot90(cube[0,:,:], -k)
        cube[1,:,0], cube[5,:,0], cube[3,:,2], cube[4,:,0] = State.swap4(cube[1,:,0], cube[5,:,0], cube[3,:,2], cube[4,:,0], k)
        return State(cube)

    def getB(cube, k=1):
        cube[2,:,:] = np.rot90(cube[2,:,:], -k)
        cube[1,:,2], cube[4,:,2], cube[3,:,0], cube[5,:,2] = State.swap4(cube[1,:,2], cube[4,::-1,2], cube[3,::-1,0], cube[5,:,2], k)
        return State(cube)

    def print(cube):

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

        cube = cube.reshape(54)
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

class Cube:

    def __init__(self):
        self.cube = State(np.arange(54).reshape(6,3,3))
        print('Starting...\n')
        print(self.cube)

    def mix(self, sequence):
        print('\n...mixing...\n')
        sequence.reverse()
        while sequence:
            m = sequence.pop()
            if m[-1] == "2":
                sequence.append(m[0])
            k = 1 if m[-1] != "'" else -1
            getattr(self, m[0])(k)
        print(self.cube)

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
    
    def U(self, k=1):
        self.cube = State.getU(self.cube.cube.copy(), k)

    def D(self, k=1):
        self.cube = State.getD(self.cube.cube.copy(), k)

    def L(self, k=1):
        self.cube = State.getL(self.cube.cube.copy(), k)

    def R(self, k=1):
        self.cube = State.getR(self.cube.cube.copy(), k)

    def F(self, k=1):
        self.cube = State.getF(self.cube.cube.copy(), k)

    def B(self, k=1):
        self.cube = State.getB(self.cube.cube.copy(), k)

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

from queue import PriorityQueue
from collections import deque

class BFS:
    def __init__(self, goal):
        self.goal = goal
        self.states = 0
        
    def process(self, first):
        queue = deque(first)
        while self.queue:
            item = queue.popleft()
            self.states += 1
            for child in item.children():
                child.parent = item
                if child.goal(goal):
                    return child
                queue.append(child)
        return False

def main(argv):
    if len(argv) > 2:
        raise Exception('Only one argument is needed.')
    r = RubikSolver()
    if len(argv) == 2:
        r.mix(argv[1])
    elif len(argv) == 1:
        r.cube.randmix(20)

if __name__ == "__main__":
    try:
        main(sys.argv)
    except Exception as e:
        print('Error : ' + str(e))
