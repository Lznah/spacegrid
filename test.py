import spacegrid
import numpy as np

grid = np.eye(4, dtype=np.uint8)
grid[3,2] = 3
grid[1,2] = 2
grid[1,1] = 1
grid[3,3] = 2


obj = spacegrid.escape_routes(grid)
print(obj.distances)
print(grid)
print(grid[:,3])