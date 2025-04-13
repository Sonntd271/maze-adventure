import pygame
import random
from tree import Tree


class Map:
    N, S, E, W = 1, 2, 4, 8
    DX = {E: 1, W: -1, N: 0, S: 0}
    DY = {E: 0, W: 0, N: -1, S: 1}
    OPPOSITE = {E: W, W: E, N: S, S: N}
    WHITE, BLACK, GREEN, RED = (255, 255, 255), (0, 0, 0), (0, 255, 0), (255, 0, 0)
    def __init__(self, rows, cols,cell_size =50):
        self.rows = rows//cell_size
        self.cols = cols//cell_size
        self.cell_size = cell_size
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.sets = [[Tree() for _ in range(self.cols)] for _ in range(self.rows)]
        self.map_boolean = None

        self.generate_maze()
        self.add_exits()

    def generate_maze(self):
        edges = [(x, y, Map.N) for y in range(1, self.rows) for x in range(self.cols)] + \
                [(x, y, Map.W) for y in range(self.rows) for x in range(1, self.cols)]
        random.shuffle(edges)
        print(f"Total edges available: {len(edges)}")
        # (0,1,N) = wall between (0,0) and (0,1)     
        while edges:
            x, y, direction = edges.pop() # 0,1,N
            nx, ny = x + Map.DX[direction], y + Map.DY[direction] # nx = 0 + 0, ny = 1 + (-1) so nx, ny = 0, 0 

            if 0 <= nx < self.cols and 0 <= ny < self.rows: # if  nx and ny not exceed the boarder 
                set1, set2 = self.sets[y][x], self.sets[ny][nx] # set1 from coordinates [x,y] = [0,1] and set2 from coordinates [x,y] = [0,0] 

                if not set1.connected(set2): # check if these two are connected, if not...
                    set1.connect(set2) #connect the set1 and set2  together
                    self.grid[y][x] |= direction # assign the direction, in this case 1 to the coordinatea0,1 in the grid 
                    self.grid[ny][nx] |= Map.OPPOSITE[direction] # assign the opposite, in this case 2 to the coordinate 0,0 in the grid
        self.add_exits()
        return self.map_boolean



    def add_exits(self):
        # Create an entrance at the top row
        top_exit = random.randint(0, self.cols - 1)  
        print(f'The value of the entrance before is {self.grid[0][top_exit]}')

        # Open South (to connect to the maze)
        self.grid[0][top_exit] |= Map.S  
        self.grid[1][top_exit] |= Map.N

        # Open West if not at left boundary
        if top_exit > 0:
            self.grid[0][top_exit] |= Map.W  
            self.grid[0][top_exit - 1] |= Map.E  # Open the East wall of the left neighbor

        # Open East if not at right boundary
        if top_exit < self.cols - 1:
            self.grid[0][top_exit] |= Map.E  
            self.grid[0][top_exit + 1] |= Map.W  # Open the West wall of the right neighbor

        print(f'The value of the entrance after is {self.grid[0][top_exit]}')
        self.entrance = (0, top_exit)  

        # Create an exit at the bottom row
        bottom_exit = random.randint(0, self.cols - 1)
        print(f'The value of the exit before is {self.grid[self.rows - 1][bottom_exit]}')

        # Open North (to connect to the maze)
        self.grid[self.rows - 1][bottom_exit] |= Map.N  
        self.grid[self.rows - 2][bottom_exit] |= Map.S

        # Open West if not at left boundary
        if bottom_exit > 0:
            self.grid[self.rows - 1][bottom_exit] |= Map.W  
            self.grid[self.rows - 1][bottom_exit - 1] |= Map.E  # Open the East wall of the left neighbor

        # Open East if not at right boundary
        if bottom_exit < self.cols - 1:
            self.grid[self.rows - 1][bottom_exit] |= Map.E  
            self.grid[self.rows - 1][bottom_exit + 1] |= Map.W  # Open the West wall of the right neighbor
        self.map_boolean = [[1 for _ in range(self.cols*3)] for _ in range(self.rows*3)]
        for y in range(self.rows):
            for x in range(self.cols):
                cx, cy = x * 3 + 1, y * 3 + 1  # Center position in the boolean map
                self.map_boolean[cy][cx] = 0   # The cell itself is always a path
                if y == self.rows - 1 and x == bottom_exit: 
                    self.map_boolean[cy][cx] = 'X'
                
                if y == 0 and x == top_exit : 
                    self.map_boolean[cy][cx] = 'E'
                # Check directions and open paths accordingly
                if self.grid[y][x] & Map.N:
                    self.map_boolean[cy - 1][cx] = 0
                if self.grid[y][x] & Map.S:
                    self.map_boolean[cy + 1][cx] = 0
                if self.grid[y][x] & Map.W:
                    self.map_boolean[cy][cx - 1] = 0
                if self.grid[y][x] & Map.E:
                    self.map_boolean[cy][cx + 1] = 0
        print(f'The value of the exit after is {self.grid[self.rows - 1][bottom_exit]}')
        self.exit = (self.rows - 1, bottom_exit)   
if __name__ == '__main__':
        x = Map(600, 800)
        print(x.generate_maze())

        
