import queue
import numpy
import cython
cimport numpy
from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free

ctypedef job * next
ctypedef job * toBeRemoved
cdef enum directions:
    up = 94,
    down = 118,
    left = 60,
    right = 62
    stay = 32

cdef numpy.uint8_t direction

ctypedef struct job:
    int x
    int y
    int dist
    job * next


__all__ = ['escape_routes']


class _EscapeRoutes:
    """
    Internal class to calculate and represent escape_routes() results.
    A reference to the given grid is kept and used in route().
    """
    def __init__(self, grid):
        self.grid = grid
        self.distances, self.directions = self.distance_directions(grid)

    @classmethod
    @cython.nonecheck(False)
    @cython.boundscheck(False)
    @cython.wraparound(False)
    def distance_directions(cls, grid):
        try:
            shape = grid.shape
            dtype = grid.dtype
            size = grid.size
            ndim = grid.ndim
        except AttributeError:
            raise TypeError('grid does not quack like a numpy array')
        if ndim != 2:
            raise TypeError('grid does not quack like a 2D-numpy array')
        if not numpy.issubdtype(dtype, numpy.integer):
            raise TypeError('grid does not quack like an integer array')

        cdef numpy.ndarray[numpy.int64_t, ndim=2] distances = numpy.full(shape, -1, dtype=numpy.int64)
        cdef numpy.ndarray[numpy.int8_t, ndim=2]  directions = numpy.full(shape, b' ', dtype=('a', 1))
        cdef numpy.ndarray[numpy.uint8_t, ndim=2] _grid = grid

        cdef job * rear = NULL
        cdef job * end = NULL
        cdef job * curr = NULL

        stations = numpy.argwhere(grid == 2)
        cdef numpy.uint64_t row, column
        cdef int width = shape[0]
        cdef int height = shape[1]
        for row, column in stations:
            directions[row, column] = b'+'
            distances[row, column] = 0
            curr = <job *>PyMem_Malloc(sizeof(job))
            curr.x = row
            curr.y = column
            curr.dist = 1
            curr.next = NULL
            if rear == NULL:
                rear = curr
                end = rear
            else:
                end.next = curr
                end = end.next

        cdef int x, y, dist, x_, y_, dist_
        #cdef char reverse
        while rear != NULL:
            x_ = rear.x
            y_ = rear.y
            dist_ = rear.dist
            for direction in range(4): # any order
                # reset the values for each direction
                x = x_
                y = y_
                dist = dist_
                while True:
                    # walk that direction, but stop at boundary
                    # this ugly if could be delegated to functions in dict :/
                    if direction == 0:
                        x = x+1
                        reverse = up
                        if x == width:
                            break
                    elif direction == 1:
                        y = y+1
                        reverse = left
                        if y == height:
                            break
                    elif direction == 2:
                        x = x-1
                        reverse = down
                        if x < 0:
                            break
                    else:  # left
                        y = y-1
                        reverse = right
                        if y < 0:
                            break
                    # singularities cannot be beamed trough
                    # no point of checking past a safe station
                    if _grid[x,y] > 1:
                        break
                    # been there better? skip but check further if not a node
                    if 0 <= distances[x,y] <= dist:
                        if _grid[x,y] == 1:
                            break
                        continue
                    distances[x,y] = dist
                    directions[x,y] = reverse
                    # if it's a transport node,
                    # we need to increase our distance and
                    # schedule a job
                    if _grid[x,y] == 1:
                        dist += 1
                        curr = <job *>PyMem_Malloc(sizeof(job))
                        curr.x = x
                        curr.y = y
                        curr.dist = dist
                        curr.next = NULL
                        end.next = curr
                        end = end.next
            toBeFreed = rear
            rear = rear.next
            PyMem_Free(toBeFreed)
        return distances, directions

    @property
    def safe_factor(self):
        reachable = numpy.count_nonzero(self.distances >= 0)
        try:
            return reachable / self.distances.size
        except ZeroDivisionError:
            return float('nan')

    def _route_generator(self, row, column):
        """
        A generator implementation of .route() without the exceptions.
        """
        direction = self.directions[row, column]
        while not direction == b'+':
            if direction == b'v':
                row += 1
            elif direction == b'>':
                column += 1
            elif direction == b'^':
                row -= 1
            elif direction == b'<':
                column -= 1
            if self.grid[row, column] > 0:
                direction = self.directions[row, column]
                yield row, column

    def route(self, row, column):
        """
        For given coordinates of a space ship,
        returns a sequence of coordinates of the best route to a safe station.
        Dos not include coordinates of the space ship.
        Includes coordinates of the safe station,
        unless the space ship is on a safe station,
        in that case it returns an empty sequence.

        Raises ValueError when not possible.
        Raises IndexError when given coordinates are out of bounds.

        Assumes self.directions are valid. If self.directions is tempered with,
        this may give incorrect results or even enter an endless loop.

        Not a generator so we can raise as soon as called.
        """
        if self.directions[row, column] == b' ':
            raise ValueError('No route to host...ehm...safe station')
        return self._route_generator(row, column)


def escape_routes(grid):
    """
    This function calculates the escape routes from the 2D space grid.

    For details, see the assignment at github.com/cvut/spacegrid
    """
    return _EscapeRoutes(grid)
