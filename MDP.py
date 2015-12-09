import logging
import numpy as np
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GridWorld:
    def __init__(self, center, left, right, grid_map):
        self.center = center
        self.left = left
        self.right = right
        self.map = grid_map
        self.counter = 0
        self.discount = .7     # gamma in the equation
        self.util_map = [[0.0 for _ in range(0, 6)] for _ in range(0, 6)]        # probably should have made a tuple instead of seperate maps
        self.reward_map = [[-.04 for _ in range(0, 6)] for _ in range(0, 6)]
        self.policy_map = [['' for _ in range(0, 6)] for _ in range(0, 6)]
        self.max_map = [[-5 for _ in range(0, 6)] for _ in range(0, 6)]
        self.same = 0
        self.iter = [0]
        self.utillist1 = [0]
        self.utillist2 = [0]
        self.utillist3 = [0]
        self.utillist4 = [0]
        self.utillist5 = [0]
        self.utillist6 = [0]
        self.utillist7 = [0]
        self.utillist8 = [0]
        self.utillist9 = [0]

        for x in range(0, 6):
            for y in range(0, 6):
                if self.map[x][y] == 'start':
                    self.start = (x, y)
                    self.map[x][y] = ''
                if self.map[x][y] == '*':
                    self.policy_map[x][y] = '*'
                    self.util_map[x][y] = 0.0
                    self.reward_map[x][y] = 0.0
                if self.map[x][y] == '':
                    self.util_map[x][y] = 0.0
                    self.reward_map[x][y] = -.04
                if self.map[x][y] != 'start' and self.map[x][y] != '*' and self.map[x][y] != '':
                    self.util_map[x][y] = int(self.map[x][y])
                    self.reward_map[x][y] = int(self.map[x][y])
                    self.policy_map[x][y] = 'T'
        logger.info(self.reward_map)
        logger.info(self.util_map)
        logger.info(self.policy_map)
        logger.info(self.map)


    def value_iterate_term(self):
        for iterate in range(0, 50):
            next_util_map = self.util_map
            for x in range(0, 6):
                for y in range(0, 6):
                    self.same = 0
                    if self.map[x][y] == '':
                        next_util_map[x][y] = (self.discount * self.optimal_util(self.util_map,x, y)) # x is row y is column
                        next_util_map[x][y] += self.reward_map[x][y]

                        #if(x == 0 and y == 0):
                         #   logger.info(next_util_map[x][y])
            self.utillist1 = np.append(next_util_map[0][0],self.utillist1)
            self.utillist2 = np.append(next_util_map[1][1],self.utillist2)
            self.utillist3 = np.append(next_util_map[2][4],self.utillist3)
            self.utillist4 = np.append(next_util_map[3][4],self.utillist4)
            self.utillist5 = np.append(next_util_map[4][5],self.utillist5)
            self.utillist6 = np.append(next_util_map[4][3],self.utillist6)
            self.utillist7 = np.append(next_util_map[2][2],self.utillist7)
            self.utillist8 = np.append(next_util_map[4][4],self.utillist8)

            self.util_map = next_util_map
            self.counter += 1
            self.iter = np.append(self.counter,self.iter)
            #logger.info(self.util_map)
            #logger.info(self.max_map)
            #logger.info(self.reward_map)
           # logger.info(self.policy_map)
           # logger.info(self.map)
            #logger.info(next_util_map)

           # logger.info(self.util_map[0][0])
        logger.info(self.util_map)
        logger.info(self.policy_map)
        plt.plot(self.iter, self.utillist1,'b-')
        plt.plot(self.iter, self.utillist2,'r-')
        plt.plot(self.iter, self.utillist3,'g-')
        plt.plot(self.iter, self.utillist4,'o-')
        plt.plot(self.iter, self.utillist5,'y-')
        plt.plot(self.iter, self.utillist6,'s-')
        plt.plot(self.iter, self.utillist7,'k-')
        plt.plot(self.iter, self.utillist8,'w-')
        plt.ylabel('Values')
        plt.xlabel('Iteration')
        plt.show()


    def value_iterate_nonterm(self):
        next_util_map = self.util_map
        for iterate in range(0, 500):
            for x in range(0, 6):
                for y in range(0, 6):
                    if self.map[x][y] != '*':
                        next_util_map[x][y] = self.reward_map[x][y] + (self.discount * self.optimal_util(x, y)) # x is row y is column

            self.util_map = next_util_map

            #logger.info(next_util_map)

           # logger.info(self.util_map[0][0])

        logger.info(self.util_map)
        logger.info(self.policy_map)


    # (0,0) is top left (north west) (5,5) is bot right (south east)
    def optimal_util(self, curr_map, rowval, colval):
        north_wall = 0
        east_wall = 0
        south_wall = 0
        west_wall = 0

        # borders
        if rowval == 0:
            north_wall = 1
        if rowval >= 5:
            south_wall = 1
        if colval >= 5:
            east_wall = 1
        if colval == 0:
            west_wall = 1

        # account for walls that aren't the borders
        if rowval > 0:
            if self.map[rowval - 1][colval] == '*':
                north_wall = 1
        if colval > 0:
            if self.map[rowval][colval - 1] == '*':
                west_wall = 1
        if rowval < 5:
            if self.map[rowval + 1][colval] == '*':
                south_wall = 1
        if colval < 5:
            if self.map[rowval][colval + 1] == '*':
                east_wall = 1
        #logger.info(rowval)
        #logger.info(colval)
        #logger.info(west_wall)
        #logger.info(self.util_map)
        if north_wall == 1:
            if east_wall == 1:
                max_val = self.calc_dir(0, 0, curr_map[rowval+1][colval], curr_map[rowval][colval-1],\
                                        north_wall, east_wall, south_wall, west_wall, rowval, colval)

            elif west_wall == 1:
                max_val = self.calc_dir(0, curr_map[rowval][colval+1], curr_map[rowval+1][colval], 0,\
                                        north_wall, east_wall, south_wall, west_wall, rowval, colval)
            elif south_wall == 1:
                max_val = self.calc_dir(0, curr_map[rowval][colval+1], 0, curr_map[rowval][colval-1],\
                                        north_wall, east_wall, south_wall, west_wall, rowval, colval)
            else:
                max_val = self.calc_dir(0, curr_map[rowval][colval+1], curr_map[rowval+1][colval], curr_map[rowval][colval-1],\
                                        north_wall, east_wall, south_wall, west_wall, rowval, colval)
        elif south_wall == 1:
            if west_wall == 1:
                max_val = self.calc_dir(curr_map[rowval-1][colval], curr_map[rowval][colval+1], 0, 0,\
                                        north_wall, east_wall, south_wall, west_wall, rowval, colval)
            elif east_wall == 1:
                max_val = self.calc_dir(curr_map[rowval-1][colval], 0, 0, curr_map[rowval][colval-1],\
                                        north_wall, east_wall, south_wall, west_wall, rowval, colval)
            else:
                max_val = self.calc_dir(curr_map[rowval-1][colval], curr_map[rowval][colval+1], 0, curr_map[rowval][colval-1],\
                                        north_wall, east_wall, south_wall, west_wall, rowval, colval)
        elif east_wall == 1:
            if west_wall == 1:
                max_val = self.calc_dir(curr_map[rowval-1][colval], 0, curr_map[rowval+1][colval], 0,\
                                        north_wall, east_wall, south_wall, west_wall, rowval, colval)
            else:
                max_val = self.calc_dir(curr_map[rowval-1][colval], 0, curr_map[rowval+1][colval], curr_map[rowval][colval-1],\
                                        north_wall, east_wall, south_wall, west_wall, rowval, colval)

        elif west_wall == 1:
            max_val = self.calc_dir(curr_map[rowval-1][colval], curr_map[rowval][colval+1], curr_map[rowval+1][colval], 0,\
                                    north_wall, east_wall, south_wall, west_wall, rowval, colval)
        else:
            max_val = self.calc_dir(curr_map[rowval-1][colval], curr_map[rowval][colval+1], curr_map[rowval+1][colval], curr_map[rowval][colval-1],\
                                    north_wall, east_wall, south_wall, west_wall, rowval, colval)

           # logger.info(max_val)
       # if(rowval == 0 and colval == 0):
            #logger.info(max_val)
        return max_val

    def calc_dir(self, north, east, south, west, north_wall, east_wall, south_wall, west_wall, rowval, colval):
        north_center = (self.center * north) +(self.left * west) + (self.right * east)

        east_center = (self.center * east) +(self.left * north) + (self.right * south)

        south_center = (self.center * south) + (self.left * east) + (self.right * west)

        west_center = (self.center * west) + (self.left * south) + (self.right * north)

        #logger.info(north_center)
        max_val = max(north_center, east_center, south_center, west_center)
        self.max_map[rowval][colval] = np.append(max_val,self.max_map[rowval][colval])

        if max_val >= max(self.max_map[rowval][colval]):
            if north_center == max_val:
                self.policy_map[rowval][colval] = 'N'
                if north_wall == 1:
                    self.same = 1
            elif east_center == max_val:
                self.policy_map[rowval][colval] = 'E'
                if east_wall == 1:
                    self.same = 1
            elif south_center == max_val:
                self.policy_map[rowval][colval] = 'S'
                if south_wall == 1:
                    self.same = 1
            elif west_center == max_val:
                self.policy_map[rowval][colval] = 'W'
                if west_wall == 1:
                    self.same = 1
        #logger.info(self.max_map[0][0])
        return max(self.max_map[rowval][colval])

def main():
    # * = walls
    grid_map = [ ['',   '-1',    '',     '',     '',     ''],
                 ['',   '',      '',     '*',    '-1',   ''],
                 ['',   '',      '',     '*',    '',     '3'],
                 ['',   'start', '',     '*',    '',     ''],
                 ['',   '',      '',     '',     '',     ''],
                 ['1',  '-1',    '',     '*',    '-1',   '-1']]
    grid_world = GridWorld(.8, .1, .1, grid_map)
    grid_world.value_iterate_term()
  #  grid_world.value_iterate_nonterm()


if __name__ == '__main__':
    main()