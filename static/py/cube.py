try:
    from static.py.unfolded import Unfolded
    from static.py.utils import binomial, rotLeft, rotRight
except ModuleNotFoundError:
    from unfolded import Unfolded
    from utils import binomial, rotLeft, rotRight
from random import choice, getrandbits

class Cube:
    def __init__(self, cp=None, co=None, ep=None, eo=None):
        self.newCube(cp, co, ep, eo)
        
    def newCube(self, cp=None, co=None, ep=None, eo=None):
        # cp : corner position
        # [URF,UFL,ULB,UBR,DFR,DLF,DBL,DRB]
        # [  0,  1,  2,  3,  4,  5,  6,  7]
        self.cp = list(range(8)) if cp is None else cp
        # co : corner orientation
        self.co = [0] * 8 if co is None else co
        # ep : edge position
        # [UR,UF,UL,UB,DR,DF,DL,DB,FR,FL,BL,BR]
        # [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11]
        self.ep = list(range(12)) if ep is None else ep
        # eo : edge orientation
        self.eo = [0]*12 if eo is None else eo

    def reset(self):
        self.newCube()

    def __eq__(self, o):
        return (self.cp == o.cp and self.co == o.co and self.ep == o.ep and self.eo == o.eo)

    def __str__(self):
        return ''.join(['('+str(cp)+','+str(co)+')' for cp, co in zip(self.cp, self.co)]) + '\n' + ''.join(['('+str(ep)+','+str(eo)+')' for ep, eo in zip(self.ep, self.eo)])


    def mix(self, sequence):
        out = sequence[::]
        sequence.reverse()
        while sequence:
            m = sequence.pop()
            if m[-1] == "2":
                sequence.append(m[0])
            elif m[-1] == "'":
                sequence.append(m[0])
                sequence.append(m[0])
            self.move(m[0])
        self.show()
        return out

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
        return self.mix(sequence)

    def show(self):
        u = Unfolded(self.cp, self.co, self.ep, self.eo)
        print(u)
        return u

    def getCo(self):
        # 3**7
        # (0..2186)
        n = 0
        for x in self.co[:-1]:
            n = n * 3 + x
        return n

    def setCo(self, n):
        # 3**7
        # (0..2186)
        for i in range(6, -1, -1):
            self.co[i] = n % 3
            n //= 3
        self.co[-1] = (3 - sum(self.co[:-1])) % 3

    def getEo(self):
        # 2**11
        # (0..2047)
        n = 0
        for x in self.eo[:-1]:
            n = n * 2 + x
        return n

    def setEo(self, n):
        # 2**11
        # (0..2047)
        for i in range(10, -1, -1):
            self.eo[i] = n % 2
            n //= 2
        self.eo[-1] = (2 - sum(self.eo[:-1])) % 2

    def getCp(self):
        # 8!
        # (0..40319)
        perm = self.cp[:]
        n = 0
        for i in range(7, 0, -1):
            k = 0
            while perm[i] != i:
                rotLeft(perm, 0, i)
                k += 1
            n = (i + 1) * n + k
        return n

    def setCp(self, n):
        # 8!
        # (0..40319)
        self.cp = list(range(8))
        for i in range(8):
            k = n % (i + 1)
            n //= (i + 1)
            while k:
                rotRight(self.cp, 0, i)
                k -= 1

    def getSlice(self):
        # UD-Slice : position of edges FR, FL, BL, BR without permutation : 4 parmi 12
        n = 0
        x = 1
        for i in range(11, -1, -1):
            if self.ep[i] in {8,9,10,11}:
                n += binomial(11 - i, x)
                x += 1
        return n

    def setSlice(self, n):
        sliceE = [11,10,9,8]
        otherE = [7,6,5,4,3,2,1,0]
        for i in range(12):
            if n - binomial(11 - i, len(sliceE)) >= 0:
                n -= binomial(11 - i, len(sliceE))
                self.ep[i] = sliceE.pop()
            else:
                self.ep[i] = otherE.pop()

    def getSliceSorted(self):
        # UD-Slice : position of edges FR, FL, BL, BR with permutation
        # 12 * 11 * 10 * 9 = 11880
        # < 11880 in phase 1, < 24 in phase 2, 0 for solved cube
        n = 0
        edge = []
        # n < 495 (4 parmi 12)
        for i in range(11, -1, -1):
            if self.ep[i] in {8,9,10,11}:
                n += binomial(11 - i, len(edge) + 1)
                edge.append(self.ep[i])
        # m < 24 (4!) permutations
        edge = edge[::-1]
        m = 0
        for i in range(3, 0, -1):
            k = 0
            while edge[i] != i + 8:
                rotLeft(edge, 0, i)
                k += 1
            m = (i + 1) * m + k
        return 24*n + m

    def setSliceSorted(self, n):
        sliceE = [8,9,10,11]
        otherE = [7,6,5,4,3,2,1,0]
        m = n % 24
        n = n // 24
        for i in range(1, 4):
            k = m % (i + 1)
            m //= i + 1
            while k > 0:
                rotRight(sliceE, 0, i)
                k -= 1
        sliceE = sliceE[::-1]
        for i in range(12):
            if n - binomial(11 - i, len(sliceE)) >= 0:
                n -= binomial(11 - i, len(sliceE))
                self.ep[i] = sliceE.pop()
            else:
                self.ep[i] = otherE.pop()

    def getUpEdges(self):
        # UpEdges : position of edges UR, UF, UL, UB with permutation
        # 12 * 11 * 10 * 9 = 11880
        # < 11880 in phase 1, < 1656 + 24 in phase 2, 1656 for solved cube
        n = 0
        edge = []
        ep = self.ep[8:] + self.ep[:8]
        # n < 495 (4 parmi 12)
        for i in range(11, -1, -1):
            if ep[i] in {0,1,2,3}:
                n += binomial(11 - i, len(edge) + 1)
                edge.append(ep[i])
        # m < 24 (4!) permutations
        edge = edge[::-1]
        m = 0
        for i in range(3, 0, -1):
            k = 0
            while edge[i] != i:
                rotLeft(edge, 0, i)
                k += 1
            m = (i + 1) * m + k
        return 24*n + m

    def setUpEdges(self, n):
        sliceE = [0,1,2,3]
        otherE = [11,10,9,8,7,6,5,4]
        m = n % 24 # Permutation
        n = n // 24 # Location
        for i in range(1, 4):
            k = m % (i + 1)
            m //= i + 1
            while k > 0:
                rotRight(sliceE, 0, i)
                k -= 1
        sliceE = sliceE[::-1]
        for i in range(12):
            if n - binomial(11 - i, len(sliceE)) >= 0:
                n -= binomial(11 - i, len(sliceE))
                self.ep[i] = sliceE.pop()
            else:
                self.ep[i] = otherE.pop()
        for _ in range(4):
            rotLeft(self.ep, 0, 11)

    def getDownEdges(self):
        # DownEdges : position of edges DR, DF, DL, DB with permutation
        # 12 * 11 * 10 * 9 = 11880
        # < 11880 in phase 1, < 1656 + 24 in phase 2, 1656 for solved cube
        n = 0
        edge = []
        ep = self.ep[8:] + self.ep[:8]
        # n < 495 (4 parmi 12)
        for i in range(11, -1, -1):
            if ep[i] in {4,5,6,7}:
                n += binomial(11 - i, len(edge) + 1)
                edge.append(ep[i])
        # m < 24 (4!) permutations
        edge = edge[::-1]
        m = 0
        for i in range(3, 0, -1):
            k = 0
            while edge[i] != i + 4:
                rotLeft(edge, 0, i)
                k += 1
            m = (i + 1) * m + k
        return 24*n + m

    def setDownEdges(self, n):
        sliceE = [4,5,6,7]
        otherE = [3,2,1,0,11,10,9,8]
        m = n % 24 # Permutation
        n = n // 24 # Location
        for i in range(1, 4):
            k = m % (i + 1)
            m //= i + 1
            while k > 0:
                rotRight(sliceE, 0, i)
                k -= 1
        sliceE = sliceE[::-1]
        for i in range(12):
            if n - binomial(11 - i, len(sliceE)) >= 0:
                n -= binomial(11 - i, len(sliceE))
                self.ep[i] = sliceE.pop()
            else:
                self.ep[i] = otherE.pop()
        for _ in range(4):
            rotLeft(self.ep, 0, 11)

    def getUDEdges(self):
        # UpDownEdges : position of edges UR,UF,UL,UB,DR,DF,DL and DB with permutation
        # 8! = 40320
        ep = self.ep[:8]
        n = 0
        for i in range(7,0,-1):
            k = 0
            while i != ep[i]:
                rotLeft(ep, 0, i)
                k += 1
            n = (i + 1) * n + k
        return n

    def setUDEdges(self, n):
        self.ep[:8] = range(8)
        for i in range(8):
            k = n % (i + 1)
            n //= (i + 1)
            while k:
                rotRight(self.ep, 0, i)
                k -= 1

    def toUnfolded(self):
        return Unfolded(self.cp, self.co, self.ep, self.eo)

    def show(self):
        print(self.toUnfolded())

    def move(self, m):
        getattr(self, m)()

    def _cpy(self):
        return self.cp.copy(), self.co.copy(), self.ep.copy(), self.eo.copy()

    def U(self):
        cp, co, ep, eo = self._cpy()

        self.cp[0] = cp[3]
        self.cp[1] = cp[0]
        self.cp[2] = cp[1]
        self.cp[3] = cp[2]

        self.co[0] = co[3]
        self.co[1] = co[0]
        self.co[2] = co[1]
        self.co[3] = co[2]

        self.ep[0] = ep[3]
        self.ep[1] = ep[0]
        self.ep[2] = ep[1]
        self.ep[3] = ep[2]

        self.eo[0] = eo[3]
        self.eo[1] = eo[0]
        self.eo[2] = eo[1]
        self.eo[3] = eo[2]

    def R(self):
        cp, co, ep, eo = self._cpy()

        self.cp[0] = cp[4]
        self.cp[3] = cp[0]
        self.cp[4] = cp[7]
        self.cp[7] = cp[3]

        self.co[0] = (co[4] + 2) % 3
        self.co[3] = (co[0] + 1) % 3
        self.co[4] = (co[7] + 1) % 3
        self.co[7] = (co[3] + 2) % 3

        self.ep[0] = ep[8]
        self.ep[4] = ep[11]
        self.ep[8] = ep[4]
        self.ep[11] = ep[0]

        self.eo[0] = eo[8]
        self.eo[4] = eo[11]
        self.eo[8] = eo[4]
        self.eo[11] = eo[0]

    def F(self):
        cp, co, ep, eo = self._cpy()

        self.cp[0] = cp[1]
        self.cp[1] = cp[5]
        self.cp[4] = cp[0]
        self.cp[5] = cp[4]

        self.co[0] = (co[1] + 1) % 3
        self.co[1] = (co[5] + 2) % 3
        self.co[4] = (co[0] + 2) % 3
        self.co[5] = (co[4] + 1) % 3

        self.ep[1] = ep[9]
        self.ep[5] = ep[8]
        self.ep[8] = ep[1]
        self.ep[9] = ep[5]

        self.eo[1] = (eo[9] + 1) % 2
        self.eo[5] = (eo[8] + 1) % 2
        self.eo[8] = (eo[1] + 1) % 2
        self.eo[9] = (eo[5] + 1) % 2

    def D(self):
        cp, co, ep, eo = self._cpy()

        self.cp[4] = cp[5]
        self.cp[5] = cp[6]
        self.cp[6] = cp[7]
        self.cp[7] = cp[4]

        self.co[4] = co[5]
        self.co[5] = co[6]
        self.co[6] = co[7]
        self.co[7] = co[4]

        self.ep[4] = ep[5]
        self.ep[5] = ep[6]
        self.ep[6] = ep[7]
        self.ep[7] = ep[4]

        self.eo[4] = eo[5]
        self.eo[5] = eo[6]
        self.eo[6] = eo[7]
        self.eo[7] = eo[4]

    def L(self):
        cp, co, ep, eo = self._cpy()

        self.cp[1] = cp[2]
        self.cp[2] = cp[6]
        self.cp[5] = cp[1]
        self.cp[6] = cp[5]

        self.co[1] = (co[2] + 1) % 3
        self.co[2] = (co[6] + 2) % 3
        self.co[5] = (co[1] + 2) % 3
        self.co[6] = (co[5] + 1) % 3

        self.ep[2] = ep[10]
        self.ep[6] = ep[9]
        self.ep[9] = ep[2]
        self.ep[10] = ep[6]

        self.eo[2] = eo[10]
        self.eo[6] = eo[9]
        self.eo[9] = eo[2]
        self.eo[10] = eo[6]

    def B(self):
        cp, co, ep, eo = self._cpy()

        self.cp[2] = cp[3]
        self.cp[3] = cp[7]
        self.cp[6] = cp[2]
        self.cp[7] = cp[6]

        self.co[2] = (co[3] + 1) % 3
        self.co[3] = (co[7] + 2) % 3
        self.co[6] = (co[2] + 2) % 3
        self.co[7] = (co[6] + 1) % 3

        self.ep[3] = ep[11]
        self.ep[7] = ep[10]
        self.ep[10] = ep[3]
        self.ep[11] = ep[7]

        self.eo[3] = (eo[11] + 1) % 2
        self.eo[7] = (eo[10] + 1) % 2
        self.eo[10] = (eo[3] + 1) % 2
        self.eo[11] = (eo[7] + 1) % 2

def main():
    #MoveTable.CreateCornersOri()
    c = Cube()
    c.randmix(5)

if __name__ == '__main__':
    main()
