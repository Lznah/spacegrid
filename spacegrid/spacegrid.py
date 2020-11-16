import numpy as np
import numbers

LEFT=b'<'
RIGHT=b">"
UP=b"^"
DOWN=b"v"
BLANK=b" "
STATION_SYMBOL=b"+"
UNREACHEABLE=-1

TRANSPORT=1
STATION=2
SINGULARITY=3
EMPTY=0

class Node:
    def __init__(self, node_type, row, col):
        self.node_type = node_type
        self.row = row
        self.col = col
        self.distance = -1
        self.direction = BLANK
        self.is_expanded = False
        self.edges = []

    def add_edge(self, edge):
        self.edges.append(edge)

    def determine_neighbors(self, grid, graph):
        width = grid.shape[1]
        height = grid.shape[0]
        row = self.row
        col = self.col
        up = grid[0:row,col][::-1]
        offset = self._find_neighbors_offset(up)
        if offset != -1:
            neighbor = graph.get_node(row-offset, col)
            neighbor.add_edge( Edge(neighbor, self, DOWN) )
            self.add_edge( Edge(self, neighbor, UP) )

        left = grid[row,0:col][::-1]
        offset = self._find_neighbors_offset(left)
        if offset != -1:
            neighbor = graph.get_node(row, col-offset)
            neighbor.add_edge( Edge(neighbor, self, RIGHT) )
            self.add_edge( Edge(self, neighbor, LEFT) )

    def _find_neighbors_offset(self, array):
        for i in range(0,array.shape[0]):
            if array[i] == SINGULARITY:
                break
            elif array[i] != EMPTY:
                return i+1
        return -1

class Edge:
    def __init__(self, start, end, direction):
        self.start = start
        self.end = end
        self.direction = direction
        self.oposite_direction = self._get_oposite_direction(direction)
    def _get_oposite_direction(self, direction):
        if direction == UP:
            return DOWN
        if direction == DOWN:
            return UP
        if direction == LEFT:
            return RIGHT
        if direction == RIGHT:
            return LEFT

class Graph:
    def __init__(self, grid):
        self.nodes = []
        rows = grid.shape[0]
        cols = grid.shape[1]
        for row in range(0, rows):
            for col in range(0, cols):
                if grid[row, col] in [TRANSPORT, STATION]:
                    node_type = grid[row, col]
                    node = Node(node_type, row, col)
                    node.determine_neighbors(grid, self)
                    self.nodes.append(node)
        for node in self.nodes:
            if node.node_type == STATION:
                node.direction = STATION_SYMBOL
                node.distance = 0
        #self.print_nodes_and_neightbors()
 
    def get_node(self, row, col):
        for node in self.nodes:
            if node.row == row and node.col == col:
                return node

    def print_nodes_and_neightbors(self):
        for node in self.nodes:
            print('NODE: '+str(node.row)+','+str(node.col))
            for edge in node.edges:
                print('NEIGHBOR POSITION: '+str(edge.end.row)+','+str(edge.end.col))
    
    def find_nearest_stations(self):
        for node in self.nodes:
            if node.node_type == STATION:
                self._bfs(node)
    def _reset_node_statuses(self):
        for node in self.nodes:
            node.is_expanded = False

    def _bfs(self, start: Node):
        self._reset_node_statuses()
        queue = []
        self._fill_queue(queue, start.edges, 0)

        while queue:
            edge, distance = queue.pop(0)
            node = edge.end
            if node.distance == -1 or node.distance > distance:
                node.distance = distance
                node.direction = edge.oposite_direction
                self._fill_queue(queue, node.edges, distance)
                
    
    def _fill_queue(self, queue, edges, distance):
        for edge in edges:
            node = edge.end
            if not node.is_expanded and not node.node_type == STATION:
                node.is_expanded = True
                queue.append((edge, distance+1))

class Spacegrid:
    def __init__(self, grid):
        if type(grid) != np.ndarray:
            raise TypeError
        if grid.dtype == 'float':
            raise TypeError
        if grid.ndim != 2:
            raise TypeError
        self.grid = grid
        self.rows = grid.shape[0]
        self.cols = grid.shape[1]
        self.distances = np.full(grid.shape, UNREACHEABLE, dtype="int32")
        self.directions = np.full(grid.shape, BLANK, dtype=('a', 1))
        self._graph = Graph(grid)
        self._graph.find_nearest_stations()
        for node in self._graph.nodes:
            self.distances[node.row, node.col] = node.distance
            self.directions[node.row, node.col] = node.direction 
        for row in range(0, self.rows):
            for col in range(0, self.cols):
                if grid[row, col] == EMPTY:
                    self._find_distances(row, col)
        self.safe_factor = self._compute_safe_factor()
                    
    def route(self, row, column):
        if not isinstance(row, numbers.Integral) or not isinstance(column, numbers.Integral):
            raise IndexError

        if row < 0 or row > self.rows or column < 0 or column > self.cols:
            raise IndexError

        if self.distances[row, column] == UNREACHEABLE:
            raise ValueError

        if self.grid[row, column] == STATION:
            return []

        r = row
        c = column
        r_offset = 0
        c_offset = 0
        path = []
        while self.directions[r+r_offset, c+c_offset] != STATION_SYMBOL:
            if self.directions[r, c] == UP:
                r_offset-=1
            if self.directions[r, c] == DOWN:
                r_offset+=1
            if self.directions[r, c] == LEFT:
                c_offset-=1
            if self.directions[r, c] == RIGHT:
                c_offset+=1
            if self.grid[r+r_offset, c+c_offset] != EMPTY:
                r += r_offset
                c += c_offset
                r_offset = 0
                c_offset = 0
                path.append((r,c))
        return path

    def _compute_safe_factor(self):
        if self.rows == 0 or self.cols == 0:
            return float('nan')

        count = 0
        for row in self.distances:
            for cell in row:
                if cell != UNREACHEABLE:
                    count+=1
        return count/(self.rows*self.cols)

    def _find_distances(self, row, col):
        for row in range(0, self.rows):
            for col in range(0, self.cols):
                if self.grid[row, col] == EMPTY and self.distances[row, col] == -1:
                    min_neighbor, direction = self._find_minimal_neighbor(row, col)
                    if min_neighbor and min_neighbor.distance != -1:
                        if direction == UP:
                            self.distances[row, col] = min_neighbor.distance+1
                            self.directions[row, col] = UP
                        if direction == DOWN:
                            self.distances[row, col] = min_neighbor.distance+1
                            self.directions[row, col] = DOWN
                        if direction == LEFT:
                            self.distances[row, col] = min_neighbor.distance+1
                            self.directions[row, col] = LEFT
                        if direction == RIGHT:
                            self.distances[row, col] = min_neighbor.distance+1
                            self.directions[row, col] = RIGHT

    def _find_minimal_neighbor(self, row, col): 
        grid = self.grid
        graph = self._graph
        width = grid.shape[1]
        height = grid.shape[0]
        minimal_neightbor = None
        direction = BLANK
        minimum = -1

        up = grid[0:row,col][::-1]
        offset = self._find_neighbors_offset(up)
        if offset != -1:
            neighbor = graph.get_node(row-offset, col)
            if not minimal_neightbor or neighbor.distance < minimal_neightbor.distance:
                minimal_neightbor = neighbor
                direction = UP

        down = grid[row+1:height,col]
        offset = self._find_neighbors_offset(down)
        if offset != -1:
            neighbor = graph.get_node(row+offset, col)
            if not minimal_neightbor or neighbor.distance < minimal_neightbor.distance:
                minimal_neightbor = neighbor
                direction = DOWN

        left = grid[row,0:col][::-1]
        offset = self._find_neighbors_offset(left)
        if offset != -1:
            neighbor = graph.get_node(row, col-offset)
            if not minimal_neightbor or neighbor.distance < minimal_neightbor.distance:
                minimal_neightbor = neighbor
                direction = LEFT

        right = grid[row,col+1:width]
        offset = self._find_neighbors_offset(right)
        if offset != -1:
            neighbor = graph.get_node(row, col+offset)
            if not minimal_neightbor or neighbor.distance < minimal_neightbor.distance:
                minimal_neightbor = neighbor
                direction = RIGHT
        return minimal_neightbor, direction

    def _find_neighbors_offset(self, array):
        for i in range(0,array.shape[0]):
            if array[i] == SINGULARITY:
                break
            if array[i] != EMPTY:
                return i+1
        return -1
        
    # def _is_closer_by_manhattan(self, a:Node, b:Node, row, col):
    #     distance_a = abs(a.row-row)+abs(a.col-col)
    #     distance_b = abs(b.row-row)+abs(b.col-col)
    #     if col == 7 and row == 4:
    #         print(a.row,row,':',a.col,col)
    #         print(b.row,row,':',b.col,col)
    #         print(b.row, b.col)
    #         print(distance_a,distance_b)
    #     return distance_a < distance_b
        
def escape_routes(grid):
    return Spacegrid(grid)

