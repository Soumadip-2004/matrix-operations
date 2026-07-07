class Matrix:
    def __init__(self, data):
        self._validate(data)
        self._data = [row[:] for row in data]
        self._rows = len(data)
        self._cols = len(data[0])

    def _validate(self, data):
        if not data or not all(isinstance(row, list) for row in data):
            raise TypeError("Matrix data must be a list of lists")
        row_len = len(data[0])
        if any(len(row) != row_len for row in data):
            raise ValueError("All rows must have the same length")

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

    @property
    def data(self):
        return [row[:] for row in self._data]

    def __str__(self):
        rows = []
        for row in self._data:
            rows.append(" , ".join("{}".format(val) for val in row))
        return "\n".join(rows)

    def __add__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError(
                "Matrix addition and subtraction can only be performed "
                "between matrices with the same dimension."
            )
        result = [
            [self._data[i][j] + other._data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def __sub__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError(
                "Matrix addition and subtraction can only be performed "
                "between matrices with the same dimension."
            )
        result = [
            [self._data[i][j] - other._data[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]
        return Matrix(result)

    def __mul__(self, other):
        # Case 1: scalar multiplication (Matrix * number)
        if isinstance(other, (int, float)):
            result = [[val * other for val in row] for row in self._data]
            return Matrix(result)

        # Case 2: matrix multiplication (Matrix * Matrix)
        elif isinstance(other, Matrix):
            if self.cols != other.rows:
                raise ValueError(
                    "For multiplication, the number of columns in "
                    "Matrix A must equal the number of rows in Matrix B."
                )
            result = [
                [
                    sum(self._data[i][k] * other._data[k][j] for k in range(self.cols))
                    for j in range(other.cols)
                ]
                for i in range(self.rows)
            ]
            return Matrix(result)

        else:
            raise TypeError("Unsupported operand type for *")

    def __rmul__(self, other):
        # allows number * Matrix (e.g. 2 * m) in addition to m * 2
        return self.__mul__(other)

    def transpose(self):
        transposed = [
            [self._data[i][j] for i in range(self.rows)]
            for j in range(self.cols)
        ]
        return Matrix(transposed)

    def _minor(self, row_to_remove, col_to_remove):
        """Return the submatrix data with the given row and column removed."""
        return [
            [self._data[i][j] for j in range(self.cols) if j != col_to_remove]
            for i in range(self.rows) if i != row_to_remove
        ]

    def determinant(self):
        if self.rows != self.cols:
            raise ValueError("Determinant is only defined for square matrices")

        n = self.rows
        mat = self._data

        if n == 1:
            return mat[0][0]
        if n == 2:
            return mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]

        det = 0
        for col in range(n):
            minor = self._minor(0, col)
            cofactor = ((-1) ** col) * mat[0][col] * Matrix(minor).determinant()
            det = det + cofactor
        return det

    def adjoint(self):
        if self.rows != self.cols:
            raise ValueError("Adjoint is only defined for square matrices")

        n = self.rows
        if n == 1:
            return Matrix([[1]])

        cofactor_data = [
            [
                ((-1) ** (i + j)) * Matrix(self._minor(i, j)).determinant()
                for j in range(n)
            ]
            for i in range(n)
        ]
        # adjoint = transpose of the cofactor matrix
        transposed = [
            [cofactor_data[i][j] for i in range(n)]
            for j in range(n)
        ]
        return Matrix(transposed)

    def inverse(self):
        if self.rows != self.cols:
            raise ValueError("Inverse is only defined for square matrices")

        det = self.determinant()
        if det == 0:
            raise ValueError("Matrix is singular; inverse does not exist")

        adj = self.adjoint()
        result = [[val / det for val in row] for row in adj._data]
        return Matrix(result)