import sys
from PySide import QtGui, QtCore, QtOpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from glctx import gl_begin, gl_push
from mesh import PolyCube

class Viewport(QtOpenGL.QGLWidget):

    def __init__(self, parent=None):
        super(Viewport, self).__init__(parent)

    def initializeGL(self):
        "runs once, after OpenGL context is created"
        glEnable(GL_DEPTH_TEST)
        glClearColor(1,1,1,0) # white background
        glShadeModel(GL_SMOOTH)
        glEnable(GL_COLOR_MATERIAL)
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialfv(GL_FRONT, GL_SHININESS, [50.0])
        glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [1.0, 1.0, 1.0, 0.0])
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        self.orientCamera()
        gluLookAt(
            -10, 10, -10, # eye position
            0, 0, 0, # focal point
            0, 1, 0 # up vector
        )

    def paintGL(self):
        "runs every time an image update is needed"
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        PolyCube().draw()

    def resizeGL(self, w, h):
        "runs every time the window changes size"
        glViewport(0, 0, w, h)
        self.orientCamera()

    def orientCamera(self):
        "update projection matrix, especially when aspect ratio changes"
        with gl_push(GL_TRANSFORM_BIT):
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(60.0, self.width()/float(self.height()), 0.01, 1000)


class Win(QtGui.QMainWindow):

    def __init__(self):
        super(Win, self).__init__()

        self.setWindowTitle('Main Window')
        self.setMinimumSize(640, 480)
        self.create_layout()

    def create_layout(self):
        viewport = Viewport(self)
        self.setCentralWidget(viewport)


def main():
    app = QtGui.QApplication(sys.argv)
    win = Win()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
