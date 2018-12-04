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

def main():
    return

if __name__ == '__main__':
    main()
