import numpy as np

def escape_routes(grid):
    pass
   
class SpaceObject:
    def __init__(self):
        pass

class EmptySpace(SpaceObject):
    DISTANCE=0
    CODE=0

class TransportVertex(SpaceObject):
    DISTANCE=1
    CODE=1

class RescueStation(SpaceObject):
    DISTANCE=0
    CODE=1

class Singularity(SpaceObject):
    DISTANCE=-1
    CODE=3

class Space:
    def __init__(self, y, x, object: SpaceObject = EmptySpace):
        self.y = y
        self.x = x
        self.fill_with(object)

    def fill_with(self, object: SpaceObject):
        self.object = object
        self.distance = object.DISTANCE
        self.direction = BLANK

LEFT=b'<'
RIGHT=b">"
UP=b"^"
DOWN=b"v"
BLANK=b" "
UNREACHABLE=-1

class Spacegrid:

    def __init__(self, grid):
        self.grid = grid
        self.safe_factor = float('nan')

    @staticmethod
    def load(grid):
        shape = grid.shape
        spacegrid = np.empty(shape, dtype=Space)
        rows = shape[0]
        cols = shape[1]
        for y in range(0, rows):
            for x in range(0, cols):
                spacegrid[y, x] = Space(y, x)
                if int(grid[y, x]) == TransportVertex.CODE:
                    spacegrid[y, x].fill_with(TransportVertex)
                elif grid[y, x] == RescueStation.CODE:
                    spacegrid[y, x].fill_with(RescueStation) 
                elif grid[y, x] == Singularity.CODE:
                    spacegrid[y, x].fill_with(Singularity)
        return Spacegrid(spacegrid)

    def compute(self):
        for station in self.rescue_stations:
            self.get_available_paths(station)

    def compute_safe_factor(distances):
        return 1

    def to_object(self):
        return SpaceObjectResult(self)

    def get_width(self):
        return self.spacegrid.shape[1]

    def get_height(self):
        return self.spacegrid.shape[2]

    def get_available_paths(self, vertex):
        vertexy = vertex.y
        x = vertex.x
        width = self.get_width()
        height = self.get_height()
        for(y=vertex.y; y<)
        return 

def escape_routes(grid):
    spacegrid = Spacegrid.load(grid)
    spacegrid.compute()
    return spacegrid.to_object()

def route(row, column):
    pass

class SpaceObjectResult:
    def __init__(self, spacegrid: Spacegrid):
        shape = spacegrid.grid.shape
        rows = shape[0]
        cols = shape[1]
        distances = np.full(shape, UNREACHABLE)
        directions = np.full(shape, BLANK)
        for y in range(0, rows):
            for x in range(0, cols):
                distances[y, x] = spacegrid.grid[y, x].distance
                directions[y, x] = spacegrid.grid[y, x].direction
        self.distances = distances
        self.directions = directions
