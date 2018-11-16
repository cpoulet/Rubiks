from enum import Enum
from utils import binomial
from math import factorial as fact
from collections import defaultdict as ddict
import json

CORNERS = {1:'URF',2:'UFL',3:'ULB',4:'UBR',5:'DFR',6:'DLF',7:'DBL',8:'DRB'}
C_O = 0

class MoveTable:
    FOLDER = 'movetable/'
    MOVES = ['U','R','F','D','L','B']

    def CreateCornersPos():
        FACTS = [factorial(x) for x in reversed(range(1,8))]
        C1 = ['URF','UFL','ULB','UBR','DFR','DLF','DBL','DRB']
        C2 = {'URF':0,'UFL':1,'ULB':2,'UBR':3,'DFR':4,'DLF':5,'DBL':6,'DRB':7}
        
        def encode(li):
            li = [C2[x] for x in li]
            def higherLeft(sub, x):
                return sum([1 if i > x else 0 for i in sub])
            
            def toNum(li):
                n = 0
                for f in FACTS:
                    n += li.pop()*(f)
                return n

            return toNum([higherLeft(li[:i], li[i]) for i in reversed(range(1,8))][::-1])

        def decode(n):

            def toLi(n)
                li = []
                for f in FACTS:
                    r = n // f
                    n = n % f
                    li.append(r)
                return li[::-1]
            
            return toLi(n)

        data = {}
        c = Cube()
        for p in range(40320):
            li = decode(p)
            moves = {}
            for m in MoveTable.MOVES:
                for n in range(4):
                    c.move(m)
                    if n != 3:
                        moves[m] = encode(c.corners)
                    else:
                        data[p] = moves
            break
        print(data)

    def CreateCornersOri():
        
        def encode(li):
            n = 0
            i = 0
            li = li[:-1]
            while li:
                n += li.pop()*(3**i)
                i += 1
            return n

        def decode(n):
            # (0..2186)
            li = []
            for _ in range(7):
                n, r = divmod(n, 3)
                li.append(r)
            return li[::-1] + [(3 - sum(li)) % 3]
        
        data = {}
        c = Cube()
        for p in range(2187):
            c.corners_ori = decode(p)
            moves = {}
            for m in MoveTable.MOVES:
                nb = {}
                for n in range(4):
                    c.move(m)
                    if n != 3:
                        nb[n] = encode(c.corners_ori)
                    else:
                        moves[m] = nb
                        data[p] = moves
        MoveTable._saveData('corner_ori', data)

    def _saveData(name, data):
        with open(MoveTable.FOLDER + name, 'w') as fp:
            json.dump(data, fp)

class Cube:
    def __init__(self):
        self.corners = ['URF','UFL','ULB','UBR','DFR','DLF','DBL','DRB']
        self.corners_ori = [0] * 8
        self.edges = ['UR','UF','UL','UB','DR','DF','DL','DB','FR','FL','BL','BR']
        self.edges_ori = [0] * 12

    def move(self, m):
        getattr(self, m)()

    def _cpy(self):
        return self.corners.copy(), self.corners_ori.copy()

    def U(self):
        corners, corners_ori = self._cpy()

        self.corners[0] = corners[3]
        self.corners[1] = corners[0]
        self.corners[2] = corners[1]
        self.corners[3] = corners[2]

    def R(self):
        corners, corners_ori = self._cpy()

        self.corners[0] = corners[4]
        self.corners[3] = corners[0]
        self.corners[4] = corners[7]
        self.corners[7] = corners[3]

        self.corners_ori[0] = (corners_ori[4] + 2) % 3
        self.corners_ori[3] = (corners_ori[0] + 1) % 3
        self.corners_ori[4] = (corners_ori[7] + 1) % 3
        self.corners_ori[7] = (corners_ori[3] + 2) % 3

    def F(self):
        corners, corners_ori = self._cpy()

        self.corners[0] = corners[1]
        self.corners[1] = corners[5]
        self.corners[4] = corners[0]
        self.corners[5] = corners[4]

        self.corners_ori[0] = (corners_ori[1] + 1) % 3
        self.corners_ori[1] = (corners_ori[5] + 2) % 3
        self.corners_ori[4] = (corners_ori[0] + 2) % 3
        self.corners_ori[5] = (corners_ori[4] + 1) % 3

    def D(self):
        corners, corners_ori = self._cpy()

        self.corners[4] = corners[5]
        self.corners[5] = corners[6]
        self.corners[6] = corners[7]
        self.corners[7] = corners[4]

    def L(self):
        corners, corners_ori = self._cpy()

        self.corners[1] = corners[2]
        self.corners[2] = corners[6]
        self.corners[5] = corners[1]
        self.corners[6] = corners[5]

        self.corners_ori[1] = (corners_ori[2] + 1) % 3
        self.corners_ori[2] = (corners_ori[6] + 2) % 3
        self.corners_ori[5] = (corners_ori[1] + 2) % 3
        self.corners_ori[6] = (corners_ori[5] + 1) % 3

    def B(self):
        corners, corners_ori = self._cpy()

        self.corners[2] = corners[3]
        self.corners[3] = corners[7]
        self.corners[6] = corners[2]
        self.corners[7] = corners[6]

        self.corners_ori[2] = (corners_ori[3] + 1) % 3
        self.corners_ori[3] = (corners_ori[7] + 2) % 3
        self.corners_ori[6] = (corners_ori[2] + 2) % 3
        self.corners_ori[7] = (corners_ori[6] + 1) % 3

def main():
    MoveTable.CreateCornersOri()

if __name__ == '__main__':
    main()
