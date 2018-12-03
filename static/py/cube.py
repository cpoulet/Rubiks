from utils import binomial, rotLeft, rotRight, pick
from math import factorial as fact

class Unfolded:

    W = "\033[1;30;107m  \033[1;0m"
    G = "\033[1;48;5;46m  \033[1;0m"
    O = "\033[1;48;5;208m  \033[1;0m"
    Y = "\033[1;30;48;5;226m  \033[1;0m"
    B = "\033[1;48;5;4m  \033[1;0m"
    R = "\033[1;48;5;196m  \033[1;0m"
    Colors = ['W', 'G', 'O', 'Y', 'B', 'R']
    
    # [URF,UFL,ULB,UBR,DFR,DLF,DBL,DRB]
    Corners = [[8,9,20],[6,18,38],[0,36,47],[2,45,11],[29,26,15],[27,44,24],[33,53,42],[35,17,51]]
    CColors = [[0,1,2],[0,2,4],[0,4,5],[0,5,1],[3,2,1],[3,4,2],[3,5,4],[3,1,5]]
    
    # [UR,UF,UL,UB,DR,DF,DL,DB,FR,FL,BL,BR]
    Edges = [[5,10],[7,19],[3,37],[1,46],[32,16],[28,25],[30,43],[34,52],[23,12],[21,41],[50,39],[48,14]]
    EColors = [[0,1],[0,2],[0,4],[0,5],[3,1],[3,2],[3,4],[3,5],[2,1],[2,4],[5,4],[5,1]]

    def __init__(self, cp, co, ep, eo):
        self.c = [x // 9 for x in range(54)]
        for i, c in enumerate(zip(cp, co)):
            for k in range(3):
                self.c[Unfolded.Corners[i][(c[1]+k) % 3]] = Unfolded.CColors[c[0]][k]
        for i, e in enumerate(zip(ep, eo)):
            for k in range(2):
                self.c[Unfolded.Edges[i][(e[1]+k) % 2]] = Unfolded.EColors[e[0]][k]

    def toStr(self):
        s = ''
        for x in self.c:
            s += Unfolded.Colors[x]
        return s

    def __str__(self):
        s = self.toStr()
        c = lambda x : getattr(self, x[0]) + getattr(self, x[1]) + getattr(self, x[2])
        o  = ' '*9 + c(s[:3]) + '\n'
        o += ' '*9 + c(s[3:6]) + '\n'
        o += ' '*9 + c(s[6:9]) + '\n\n'
        o += ' ' + c(s[36:39]) + '  ' + c(s[18:21]) + '  ' \
                + c(s[9:12]) + '  ' + c(s[45:48]) + '\n'
        o += ' ' + c(s[39:42]) + '  ' + c(s[21:24]) + '  ' \
                + c(s[12:15]) + '  ' + c(s[48:51]) + '\n'
        o += ' ' + c(s[42:45]) + '  ' + c(s[24:27]) + '  ' \
                + c(s[15:18]) + '  ' + c(s[51:54]) + '\n\n'
        o += ' '*9 + c(s[27:30]) + '\n'
        o += ' '*9 + c(s[30:33]) + '\n'
        o += ' '*9 + c(s[33:36]) + '\n'
        return o

class Cube:
    def __init__(self, cp=None, co=None, ep=None, eo=None):
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

    def __eq__(self, o):
        return (self.cp == o.cp and self.co == o.co and self.ep == o.ep and self.eo == o.eo)

    def __str__(self):
        return ''.join(['('+str(cp)+','+str(co)+')' for cp, co in zip(self.cp, self.co)]) + '\n' + ''.join(['('+str(ep)+','+str(eo)+')' for ep, eo in zip(self.ep, self.eo)])

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
        # < 11880 in phase 1, < 24 in phase 2, 0 for solved cube
        n = 0
        x = 1
        edge = []
        # n < 495 (4 parmi 12)
        for i in range(11, -1, -1):
            if self.ep[i] in {8,9,10,11}:
                n += binomial(11 - i, x)
                edge.append(self.ep[i])
                x += 1
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

        self.ep[0] = ep[3]
        self.ep[1] = ep[0]
        self.ep[2] = ep[1]
        self.ep[3] = ep[2]

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

        self.ep[4] = ep[7]
        self.ep[5] = ep[4]
        self.ep[6] = ep[5]
        self.ep[7] = ep[6]

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
    print('hi')

if __name__ == '__main__':
    main()
