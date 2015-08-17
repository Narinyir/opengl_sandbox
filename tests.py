from dtypes import Vector, Matrix

def test_matrix_inversion():

    m = Matrix(
        [0, 0, 1, 0],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [3, 3, 3, 1],
    )

    inverse = Matrix(
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [1, 0, 0, 0],
        [-3, -3, -3, 1],
    )

    assert m.inverse() == inverse


def test_matrix_methods():

    m = Matrix(
        [0, 0, 1, 0],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [3, 3, 3, 1],
    )

    determinant = 1

    adjoint = Matrix(
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [1, 0, 0, 0],
        [-3, -3, -3, 1],
    )

    inverse = Matrix(
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [1, 0, 0, 0],
        [-3, -3, -3, 1],
    )

    assert m.determinant() == determinant
    assert m.adjoint() == adjoint
    assert m.inverse() == inverse

def test_matrix_methods_again():

    m = Matrix(
        [0, 1, 0, 0],
        [1, 0, 0, 0],
        [0, 0, 1, 0],
        [3, 3, 3, 1],
    )

    determinant = -1

    adjoint = Matrix(
        [0, -1, 0, 0],
        [-1, 0, 0, 0],
        [0, 0, -1, 0],
        [3, 3, 3, -1],
    )

    inverse = Matrix(
        [0, 1, 0, 0],
        [1, 0, 0, 0],
        [0, 0, 1, 0],
        [-3, -3, -3, 1],
    )

    assert m.determinant() == determinant
    assert m.adjoint() == adjoint
    assert m.inverse() == inverse


if __name__ == '__main__':
    test_matrix_methods()
    test_matrix_methods_again()
