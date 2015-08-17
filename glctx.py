import contextlib
from OpenGL.GL import *


@contextlib.contextmanager
def gl_push(attrs):
    '''ContextManager that will call glPushAttrib on open and glPopAttrib on
    close with the specified attrs. You can combine attrs using the bitwise
    or operator.

    Accepted Attrs::
    GL_ACCUM_BUFFER_BIT, GL_COLOR_BUFFER_BIT, GL_CURRENT_BIT,
    GL_DEPTH_BUFFER_BIT, GL_ENABLE_BIT, GL_EVAL_BIT, GL_FOG_BIT, GL_HINT_BIT
    GL_LIGHTING_BIT, GL_LINE_BIT, GL_LIST_BIT, GL_MULTISAMPLE_BIT,
    GL_PIXEL_MODE_BIT, GL_POINT_BIT, GL_POLYGON_BIT, GL_POLYGON_STIPPLE_BIT,
    GL_SCISSOR_BIT, GL_STENCIL_BUFFER_BIT, GL_TEXTURE_BIT, GL_TRANSFORM_BIT,
    GL_VIEWPORT_BIT
    '''

    try:
        glPushAttrib(attrs)
        yield
    except:
        raise
    finally:
        glPopAttrib()


@contextlib.contextmanager
def gl_begin(mode):
    '''ContextManager that will call glBegin on open and glEnd on close
    with the specified mode.

    Accepted Modes::
    GL_POINTS, GL_LINES, GL_LINE_STRIP, GL_LINE_LOOP, GL_TRIANGLES,
    GL_TRIANGLE_STRIP, GL_TRIANGLE_FAN, GL_QUADS, GL_QUAD_STRIP, GL_POLYGON
    '''

    try:
        glBegin(mode)
        yield
    except:
        raise
    finally:
        glEnd()
