'''
Data Types
==========
'''
from __future__ import division
import numbers
from itertools import izip
from copy import deepcopy

OPERR = 'Unsupported operator {} for types {}, and {}'


def list2d(rows, cols):
    return [[0 for c in xrange(cols)] for r in xrange(rows)]


def transpose2d(rows):
    nr = len(rows)
    nc = len(rows[0])
    return [[rows[c][r] for c in xrange(nc)] for r in xrange(nr)]


def det3(rows):
    '''Determinant of a 3x3 matrix'''

    d1 = rows[0][0] * rows[1][1] * rows[2][2]
    d2 = rows[0][1] * rows[1][2] * rows[2][0]
    d3 = rows[0][2] * rows[1][0] * rows[2][1]

    d4 = rows[0][2] * rows[1][1] * rows[2][0]
    d5 = rows[0][1] * rows[1][0] * rows[2][2]
    d6 = rows[0][0] * rows[1][2] * rows[2][1]

    return (d1+d2+d3) - (d4+d5+d6)


class Vector(object):

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return 'Vector({}, {}, {})'.format(self.x, self.y, self.z)

    def __getitem__(self, i):
        return (self.x, self.y, self.z)[i]

    def __eq__(self, other):
        if isinstance(other, Vector):
            return all(self[i]==other[i] for i in xrange(3))
        return False

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise ValueError(OPERR.format('+', 'Vector', type(other)))
        return Vector(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    def __sub__(self, other):
        if not isinstance(other, Vector):
            raise ValueError(OPERR.format('-', 'Vector', type(other)))
        return Vector(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    def __iadd__(self, other):
        if not isinstance(other, Vector):
            raise ValueError(OPERR.format('+', 'Vector', type(other)))
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def __isub__(self, other):
        if not isinstance(other, Vector):
            raise ValueError(OPERR.format('-', 'Vector', type(other)))
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            return Vector(self.x * other, self.y * other, self.z * other)
        raise ValueError(OPERR.format('*', 'Vector', type(other)))

    def __imul__(self, other):
        if isinstance(other, numbers.Number):
            self.x *= other
            self.y *= other
            self.z *= other
        else:
            raise ValueError(OPERR.format('*', 'Vector', type(other)))
        return self

    def __rmul__(self, other):
        if isinstance(other, numbers.Number):
            return Vector(self.x * other, self.y * other, self.z * other)
        raise ValueError(OPERR.format('*', type(other), 'Vector'))

    def cross(self, v):
        if not isinstance(v, Vector):
            raise TypeError('Reflect must be passed a Vector')
        return Vector(
            self.y * v.z - self.z * v.y,
            -self.x * v.z + self.z * v.x,
            self.x * v.y - self.y * v.x
        )

    def dot(self, v):
        if not isinstance(v, Vector):
            raise TypeError('Reflect must be passed a Vector')
        return self.x*v.x + self.y*v.y + self.z*v.z

    def reflect(self, v):
        if not isinstance(v, Vector):
            raise TypeError('Reflect must be passed a Vector')
        return 2 * self.dot(v) * v - self

    def length(self):
        return (self.x*self.x + self.y*self.y + self.z*self.z)**0.5

    def normalize(self):
        l = 1.0 / self.length()
        self.x *= l
        self.y *= l
        self.z *= l

    def normal(self):
        l = 1.0 / self.length()
        return Vector(self.x * l, self.y * l, self.z * l)

    def project(self, other):
        return self.dot(other.normal()) * other

    @classmethod
    def xaxis(cls):
        return cls(1, 0, 0)

    @classmethod
    def yaxis(cls):
        return cls(0, 1, 0)

    @classmethod
    def zaxis(cls):
        return cls(0, 0, 1)


class Matrix(object):
    '''4x4 Orthogonal Matrix'''

    det_signs = (
        (1, -1, 1, -1),
        (-1, 1, -1, 1),
        (1, -1, 1, -1),
        (-1, 1, -1, 1),
    )

    def __init__(self, *rows):
        self.rows = list(rows)

    def __getitem__(self, i):
        return self.rows[i]

    def __copy__(self):
        return Matrix(*deepcopy(self.rows))

    __deepcopy__ = __copy__

    def __repr__(self):
        rows = '\n\t'.join(str(r) for r in self.rows)
        return 'Matrix(\n{}\n)'.format(rows)

    def __eq__(self, other):
        if isinstance(other, Matrix):
            for selfrow, otherrow in izip(self.rows, other.rows):
                if not selfrow == otherrow:
                    return False
            return True
        return False

    def __add__(self, other):
        if isinstance(other, Matrix):
            return Matrix(*[
                [self[r][c] + other[r][c] for c in xrange(4)]
                 for r in xrange(4)
            ])
        raise ValueError(OPERR.format('+', 'Matrix', type(other)))

    def __sub__(self, other):
        if isinstance(other, Matrix):
            return Matrix(*[
                [self[r][c] - other[r][c] for c in xrange(4)]
                 for r in xrange(4)
            ])
        raise ValueError(OPERR.format('-', 'Matrix', type(other)))

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            return Matrix(*[[c * other for c in r] for r in self.rows])
        if isinstance(other, Matrix):
            rows = list2d(4, 4)
            for r in xrange(4):
                for c in xrange(4):
                    rows[r][c] = sum(self[r][i] * other[i][c]
                                     for i in xrange(4))
            return Matrix(*rows)
        if isinstance(other, Vector):
            return Vector(
                self[0][0]*other.x, self[1][0]*other.y, self[2][0]*other.z,
                self[0][1]*other.x, self[1][1]*other.y, self[2][1]*other.z,
                self[0][2]*other.x, self[1][2]*other.y, self[2][2]*other.z,
            )
        raise ValueError(OPERR.format('*', 'Matrix', type(other)))

    def minor(self, row, col):
        '''Determinant of the cofactor of a single element.'''

        rows = deepcopy(self.rows)
        rows.pop(row)
        for r in rows:
            r.pop(col)
        return Matrix.det_signs[row][col] * det3(rows)

    def cofactor(self):
        '''Return cofactor matrix.

        The minor of each element in the matrix.
        '''

        rows = []

        for r in xrange(4):
            rows.append([])
            for c in xrange(4):
                rows[r].append(self.minor(r, c))

        return rows

    def adjoint(self):
        '''Returns the adjoint of a matrix'''

        return Matrix(*transpose2d(self.cofactor()))

    def determinant(self):
        '''Returns the determinant of a matrix'''

        return sum([self.rows[0][c] * self.minor(0, c) for c in xrange(4)])

    def transpose(self):
        '''Returns the transpose of a matrix'''

        return Matrix(*transpose2d(self.rows))

    def inverse(self):
        '''Since we are assuming this is a 4x4 orthogonal matrix, we can get
        the inverse by transposing the rotation matrix (top left 3x3 matrix)
        and inverting the translation row (fourth row representing a point).
        '''

        return Matrix(
            [self.rows[0][0], self.rows[1][0], self.rows[2][0], 0],
            [self.rows[0][1], self.rows[1][1], self.rows[2][1], 0],
            [self.rows[0][2], self.rows[1][2], self.rows[2][2], 0],
            [-self.rows[3][0], -self.rows[3][1], -self.rows[3][2], 1],
        )

    @classmethod
    def identity(cls):
        return cls(
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        )

    @property
    def x_vector(self):
        return Vector(*self.rows[0][:-1])

    @property
    def y_vector(self):
        return Vector(*self.rows[1][:-1])

    @property
    def z_vector(self):
        return Vector(*self.rows[2][:-1])


