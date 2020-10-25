import numpy as np

def escape_routes(grid):
    pass
   
class SpaceObject:
    def __init__(self):
        pass

class EmptySpace(SpaceObject):
    DISTANCE="0"
    CODE="0"

class TransportVertex(SpaceObject):
    DISTANCE="1"
    CODE="1"

class RescueStation(SpaceObject):
    DISTANCE="0"
    CODE="1"

class Singularity(SpaceObject):
    DISTANCE="-1"
    CODE="3"

class Space:
    def __init__(self, object : SpaceObject = EmptySpace):
        self.fill_place_with(object)

    def fill_place_with(SpaceObject: object):
        self.object = object
        self.distance = object.DISTANCE
        self.direction = BLANK

LEFT=b'<'
RIGHT=b">"
UP=b"^"
DOWN=b"v"
BLANK=b" "

class Spacegrid:

    def __init__(self, grid):
        self.grid = grid
        self.safe_factor = 0

    @staticmethod
    def load(grid):
        shape = grid.shape
        grid = np.full(shape, Space)
        for row in grid:
            for cell in row:
                if cell == TransportVertex.CODE:
                    grid[row,cell].fill_place_with(TransportVertex) 
                elif cell == RescueStation.CODE:
                    grid[row,cell].fill_place_with(RescueStation) 
                elif cell == Singularity.CODE:
                    Spacegrid[row,cell].fill_place_with(Singularity) 
        return Spacegrid(grid)

    def compute(self):
        pass

    def compute_safe_factor(distances):
        return 1


def escape_routes(grid):
    spacegrid = Spacegrid.load(grid)
    spacegrid.compute()

def route():
    pass