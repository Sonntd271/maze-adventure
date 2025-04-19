import random
from modules.core.tree import Tree

class Map:
    # Direction constants
    N, S, E, W = 1, 2, 4, 8
    DX = {E: 1, W: -1, N: 0, S: 0}
    DY = {E: 0, W: 0, N: -1, S: 1}
    OPPOSITE = {E: W, W: E, N: S, S: N}

    def __init__(self, rows, cols, cell_size=50):
        self.__rows = rows // cell_size
        self.__cols = cols // cell_size
        self.__levels = {}

    @property
    def width(self):
        return self.__cols * 3

    @property
    def height(self):
        return self.__rows * 3

    def fetch_map_level(self, level):
        if level not in self.__levels:
            self.__levels[level] = self.__generate_level()
        return self.__levels[level]

    def is_walkable(self, level, x, y):
        layout = self.__levels[level]["layout"]
        if 0 <= y < len(layout) and 0 <= x < len(layout[0]):
            return layout[y][x] == 0 or layout[y][x] in ('E', 'X')
        return False

    def __generate_level(self):
        grid = [[0 for _ in range(self.__cols)] for _ in range(self.__rows)]
        sets = [[Tree() for _ in range(self.__cols)] for _ in range(self.__rows)]

        edges = [(x, y, Map.N) for y in range(1, self.__rows) for x in range(self.__cols)] + \
                [(x, y, Map.W) for y in range(self.__rows) for x in range(1, self.__cols)]
        random.shuffle(edges)

        while edges:
            x, y, direction = edges.pop()
            nx, ny = x + Map.DX[direction], y + Map.DY[direction]
            if 0 <= nx < self.__cols and 0 <= ny < self.__rows:
                set1, set2 = sets[y][x], sets[ny][nx]
                if not set1.connected(set2):
                    set1.connect(set2)
                    grid[y][x] |= direction
                    grid[ny][nx] |= Map.OPPOSITE[direction]

        # Entrance and exit
        entrance_col = random.randint(0, self.__cols - 1)
        exit_col = random.randint(0, self.__cols - 1)
        grid[0][entrance_col] |= Map.S
        grid[1][entrance_col] |= Map.N
        grid[self.__rows - 1][exit_col] |= Map.N
        grid[self.__rows - 2][exit_col] |= Map.S

        entrance = (0, entrance_col)
        exit_ = (self.__rows - 1, exit_col)

        layout = [[1 for _ in range(self.__cols * 3)] for _ in range(self.__rows * 3)]
        for y in range(self.__rows):
            for x in range(self.__cols):
                cx, cy = x * 3 + 1, y * 3 + 1
                layout[cy][cx] = 0
                if (y, x) == entrance:
                    layout[cy][cx] = 'E'
                if (y, x) == exit_:
                    layout[cy][cx] = 'X'
                if grid[y][x] & Map.N:
                    layout[cy - 1][cx] = 0
                if grid[y][x] & Map.S:
                    layout[cy + 1][cx] = 0
                if grid[y][x] & Map.W:
                    layout[cy][cx - 1] = 0
                if grid[y][x] & Map.E:
                    layout[cy][cx + 1] = 0

        return {
            "layout": layout,
            "start": self.__to_tile_coords(entrance),
            "exit": self.__to_tile_coords(exit_)
        }

    def __to_tile_coords(self, cell_coords):
        y, x = cell_coords
        return (x * 3 + 1, y * 3 + 1)

if __name__ == "__main__":
    game_map = Map(rows=600, cols=600, cell_size=50)
    for level in range(1, 4):
        print(f"\n=== Level {level} ===")
        map_info = game_map.fetch_map_level(level)
        layout = map_info["layout"]
        for row in layout:
            print("".join(str(c) if c in ('E', 'X') else '.' if c == 0 else '#' for c in row))
