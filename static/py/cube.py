from enum import Enum
from utils import binomial
from math import factorial as fact
from collections import defaultdict as ddict
import json

e_C = Enum('Corners', 'URF UFL ULB UBR DFR DLF DBL DRB')
e_E = Enum('Edges', 'FR FU FL FD UR UL DL DR BR BU BL BD')

H = {'U','D','F2','R2','B2','L2'}

CORNERS = {1:'URF',2:'UFL',3:'ULB',4:'UBR',5:'DFR',6:'DLF',7:'DBL',8:'DRB'}
C_O = 0


def getCorners_Pos(li):
    return [CORNERS[c] for c in li]

EDGES = {1:'UR',2:'UF',3:'UL',4:'UB',5:'DR',6:'DF',7:'DL',8:'DB',9:'FR',10:'FL',11:'BL',12:'BR'}
E_O = 0

def getEdges_Ori(n):
    # initial = 0
    # 2.2^10 = 2048
    # (0..2047)
    ori = []
    for _ in range(11):
        n, r = divmod(n, 2)
        ori.append(r)
    return ori[::-1] + [sum(ori) % 2]

def getEdges_Pos(li):
    return [EDGES[e] for e in li]

class MoveTable:
    FOLDER = 'movetable/'
    MOVES = ['U','R','F','D','L','B']

    def CreateCornersPos():
        data = {}
        c = Cube()
        for p in range(40320):
            li = getC_O(p)
            moves = {}
            for m in MoveTable.MOVES:
                for n in range(4):
                    c.move(m)
                    if n != 3:
                        moves[m] = invC_O(c.corners_ori)
                    else:
                        data[p] = moves
            break
        print(data)

    def CreateCornersOri():
        
        def invC_O(li):
            n = 0
            i = 0
            li = li[:-1]
            while li:
                n += li.pop()*(3**i)
                i += 1
            return n

        def getC_O(n):
            # (0..2186)
            li = []
            for _ in range(7):
                n, r = divmod(n, 3)
                li.append(r)
            return li[::-1] + [(3 - sum(li)) % 3]
        
        data = {}
        c = Cube()
        for p in range(2187):
            c.corners_ori = getC_O(p)
            moves = {}
            for m in MoveTable.MOVES:
                nb = {}
                for n in range(4):
                    c.move(m)
                    if n != 3:
                        nb[n] = invC_O(c.corners_ori)
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
