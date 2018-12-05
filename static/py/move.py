try:
    from static.py.cube import Cube
except ModuleNotFoundError:
    from cube import Cube
from os import path, makedirs
import array

CORNERS = {1:'URF',2:'UFL',3:'ULB',4:'UBR',5:'DFR',6:'DLF',7:'DBL',8:'DRB'}
C_O = 0

class MoveTable:
    FOLDER = 'movetable/'
    MOVES = ['U','R','F','D','L','B']
    N_MOVES = 18

    def CreateCpTable():
        fname = 'cpTable'
        N_CP = 40320
        data = MoveTable._loadData(fname, N_CP*MoveTable.N_MOVES)
        if data != None:
            return data
        c = Cube()
        data = array.array('H', [0 for x in range(N_CP * MoveTable.N_MOVES)])
        for i in range(N_CP):
            c.setCp(i)
            for j, m in enumerate(MoveTable.MOVES):
                for k in range(4):
                    c.move(m)
                    if k != 3:
                        data[i * MoveTable.N_MOVES + j * 3 + k] = c.getCp()
        MoveTable._saveData(fname, data)
        return data

    # Table of Corner Orientation. co < 2187 in phase 1 co = 0 in phase 2.
    def CreateCoTable():
        fname = 'coTable'
        N_CO = 2187
        data = MoveTable._loadData(fname, N_CO*MoveTable.N_MOVES)
        if data != None:
            return data
        c = Cube()
        data = array.array('H', [0 for x in range(N_CO * MoveTable.N_MOVES)])
        for i in range(N_CO):
            c.setCo(i)
            for j, m in enumerate(MoveTable.MOVES):
                for k in range(4):
                    c.move(m)
                    if k != 3:
                        data[i * MoveTable.N_MOVES + j * 3 + k] = c.getCo()
        MoveTable._saveData(fname, data)
        return data

    # Table of Edges Orientation. co < 2048 in phase 1 co = 0 in phase 2.
    def CreateEoTable():
        fname = 'eoTable'
        N_EO = 2048
        data = MoveTable._loadData(fname, N_EO*MoveTable.N_MOVES)
        if data != None:
            return data
        c = Cube()
        data = array.array('H', [0 for x in range(N_EO * MoveTable.N_MOVES)])
        for i in range(N_EO):
            c.setEo(i)
            for j, m in enumerate(MoveTable.MOVES):
                for k in range(4):
                    c.move(m)
                    if k != 3:
                        data[i * MoveTable.N_MOVES + j * 3 + k] = c.getEo()
        MoveTable._saveData(fname, data)
        return data

    # Table of UD-slice edges FR, FL, BL, BR. slice < 11880 in phase 1, slice < 24 in phase 2, slice = 0 for solved cube.
    def CreateSortedSliceTable():
        fname = 'sortedsliceTable'
        N_UDS = 11880
        data = MoveTable._loadData(fname, N_UDS*MoveTable.N_MOVES)
        if data != None:
            return data
        c = Cube()
        data = array.array('H', [0 for x in range(N_UDS * MoveTable.N_MOVES)])
        for i in range(N_UDS):
            c.setSliceSorted(i)
            for j, m in enumerate(MoveTable.MOVES):
                for k in range(4):
                    c.move(m)
                    if k != 3:
                        data[i * MoveTable.N_MOVES + j * 3 + k] = c.getSliceSorted()
        MoveTable._saveData(fname, data)
        return data

    # Table of Up edges UR, UF, UL, UB. uedges < 11880 in phase 1, uedges < 24 in phase 2, uedges = 0 for solved cube.
    def CreateUpEdgesTable():
        fname = 'upedgesTable'
        N_UE = 11880
        data = MoveTable._loadData(fname, N_UE*MoveTable.N_MOVES)
        if data != None:
            return data
        c = Cube()
        data = array.array('H', [0 for x in range(N_UE * MoveTable.N_MOVES)])
        for i in range(N_UE):
            c.setUpEdges(i)
            for j, m in enumerate(MoveTable.MOVES):
                for k in range(4):
                    c.move(m)
                    if k != 3:
                        data[i * MoveTable.N_MOVES + j * 3 + k] = c.getUpEdges()
        MoveTable._saveData(fname, data)
        return data

    # Table of Down edges DR, DF, DL, DB. dedges < 11880 in phase 1, dedges < 24 in phase 2, dedges = 0 for solved cube.
    def CreateDownEdgesTable():
        fname = 'downedgesTable'
        N_DE = 11880
        data = MoveTable._loadData(fname, N_DE*MoveTable.N_MOVES)
        if data != None:
            return data
        c = Cube()
        data = array.array('H', [0 for x in range(N_DE * MoveTable.N_MOVES)])
        for i in range(N_DE):
            c.setDownEdges(i)
            for j, m in enumerate(MoveTable.MOVES):
                for k in range(4):
                    c.move(m)
                    if k != 3:
                        data[i * MoveTable.N_MOVES + j * 3 + k] = c.getDownEdges()
        MoveTable._saveData(fname, data)
        return data

    # Table of Up and Down edges
    # 40320 permutations, only usable in the phase 2
    def CreateUDEdgesTable():
        fname = 'udedgesTable'
        N_UD = 40320
        data = MoveTable._loadData(fname, N_UD*MoveTable.N_MOVES)
        if data != None:
            return data
        c = Cube()
        data = array.array('H', [0 for x in range(N_UD * MoveTable.N_MOVES)])
        for i in range(N_UD):
            c.setUDEdges(i)
            for j, m in enumerate(MoveTable.MOVES):
                for k in range(4):
                    c.move(m)
                    if m in {'R','F','L','B'} and k != 1:
                        continue
                    if k != 3:
                        data[i * MoveTable.N_MOVES + j * 3 + k] = c.getUDEdges()
        MoveTable._saveData(fname, data)
        return data

    def _loadData(fname, size):
        if not path.isdir(MoveTable.FOLDER[:-1]):
            makedirs(MoveTable.FOLDER[:-1])
        if path.isfile(MoveTable.FOLDER + fname):
            print('loading', fname)
            with open(MoveTable.FOLDER + fname, 'rb') as f:
                data = array.array('H')
                data.fromfile(f, size)
            return data
        else:
            print('creating', fname)
            return None

    def _saveData(name, data):
        with open(MoveTable.FOLDER + name, 'wb') as f:
            data.tofile(f)

def main():
    MoveTable.CreateCpTable()
    MoveTable.CreateCoTable()
    MoveTable.CreateEoTable()
    MoveTable.CreateSortedSliceTable()
    MoveTable.CreateUpEdgesTable()
    MoveTable.CreateDownEdgesTable()
    MoveTable.CreateUDEdgesTable()

if __name__ == '__main__':
    main()
