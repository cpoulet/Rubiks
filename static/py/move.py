#from static.py.cube import Cube
from cube import Cube
from os import path
import array

CORNERS = {1:'URF',2:'UFL',3:'ULB',4:'UBR',5:'DFR',6:'DLF',7:'DBL',8:'DRB'}
C_O = 0

class MoveTable:
    FOLDER = 'movetable/'
    MOVES = ['U','R','F','D','L','B']
    N_MOVES = 18

    def CreateCpTable():
        fname = 'cpTable'
        N_CP = 2048
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

    def _loadData(fname, size):
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
    MoveTable.CreateCoTable()
    MoveTable.CreateCpTable()
    MoveTable.CreateSortedSliceTable()

if __name__ == '__main__':
    main()
