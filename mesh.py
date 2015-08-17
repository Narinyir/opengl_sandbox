from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from glctx import gl_begin, gl_push
from dtypes import Vector, Matrix


class Mesh(object):

    def __init__(self):
        self.points = []
        self.triangles = []
        self.quads = []
        self.polygons = []
        self.point_color = [0, 0, 1]
        self.face_color = [0, 1, 0]
        self.matrix = Matrix.identity()

    def draw(self):
        with gl_begin(GL_POINTS):
            glColor3f(*self.point_color)
            for point in self.points:
                glVertex3f(point.x, point.y, point.z)
        with gl_begin(GL_TRIANGLES):
            glColor3f(*self.face_color)
            for triangle in self.triangles:
                for index in triangle:
                    vert = self.points[index]
                    glVertex3f(vert.x, vert.y, vert.z)
        with gl_begin(GL_QUADS):
            glColor3f(*self.face_color)
            for quad in self.quads:
                for index in quad:
                    vert = self.points[index]
                    glVertex3f(vert.x, vert.y, vert.z)
        for polygon in self.polygons:
            glColor3f(*self.face_color)
            with gl_begin(GL_POLYGON):
                for index in polygon:
                    vert = self.points[index]
                    glVertex3f(vert.x, vert.y, vert.z)


class PolyCube(Mesh):

    def __init__(self):
        super(PolyCube, self).__init__()
        self.points = [
            Vector(1, 1, -1),
            Vector(-1, 1, -1),
            Vector(-1, 1, 1),
            Vector(1, 1, 1),
            Vector(1, -1, -1),
            Vector(-1, -1, -1),
            Vector(-1, -1, 1),
            Vector(1, -1, 1),
        ]
        self.quads = [
            [0, 1, 2, 3],
            [7, 6, 5, 4],
            [3, 2, 6, 7],
            [4, 5, 1, 2],
            [2, 1, 5, 6],
            [0, 3, 7, 4],
        ]
