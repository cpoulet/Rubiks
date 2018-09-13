#!/usr/bin/env python3

import numpy as np
import sys
import re

class Face:

    COLOR = {0: 'blue', 1: 'white', 2: 'orange', 3: 'red', 4: 'yellow', 5: 'green'}

    def __init__(self, color):
        self.color = color;
        self.grid = np.full((3,3), )

class Cube:

    def __init__(self):
        self.cube = np.array([np.full((3,3), x) for x in range(6)])
        


class RubikSolver:

    def __init__(self):
        self.sequence = []
        self.cube = 

    def mix(self, sequence):
        for x in sequence.split():
            if re.match(r'^[FRUBLD][2\']?$', x):
                self.sequence.append(x)
            else:
                raise Exception('Parsing Error')

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
