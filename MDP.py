import logging
import argparse

class GridWorld:
    def __init__(self, center, left, right, map):
        self.center = center
        self.left = left
        self.right = right
        self.map = map
        self.discount = .99     # gamma in the equation
        for x in range(0,6):
            for y in range(0,6):
                if map[x][y] == 'start':
                    self.start = (x,y)


    def value_iterate(self):
        utilMapNext = []
        for iterate in range(0,50):
            for x in range(0,6):
                for y in range(0,6):
                    utilMapNext =

def main():
   # parser = argparse.ArgumentParser()
   # parser.add_argument('filename', help='Determine which asm file to use (include ".asm" on input)')
   # args = parser.parse_args()
    # 0 = walls
    grid_map = [['','-1','','','','',],
                 ['','','','0','-1',''],
                 ['','','','0','','3'],
                 ['','start','','0','',''],
                 ['','','','','',''],
                 ['1','-1','','0','-1','-1']]
    gridworld = GridWorld(.8,.1,.1,grid_map)


if __name__ == '__main__':
    main()