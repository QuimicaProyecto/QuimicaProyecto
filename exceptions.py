class LinearAlgebraError(Exception):
    pass

class IncompatibleDimensionsError(LinearAlgebraError):
    def __init__(self,op,form_a,form_b):
        self.op=op
        self.form_a=form_a
        self.form_b=form_b

        message=f"Incompatible dimensions for {op}: {form_a} vs {form_b}"
        super().__init__(message)


class Nonsquarematrixerror(LinearAlgebraError):
    def __init__(self,shape):
        self.shape=shape
        message=f"A square matrix is ​​required; a different form was received {shape}"
        super().__init__(message)


class SingularMatrixError(LinearAlgebraError):

    def __init__(self,mesasge="The matrix is singular (not invertable)"):
        super().__init__(mesasge)


class VectorInvalidError(LinearAlgebraError):
    def __init__(self,shape):
        self.shape=shape
        message=f"Vector must have one column (nx1), it took shape: {shape}"
        super().__init__(message)


class ZeroVectorError(LinearAlgebraError):
    def __init__(self):
        super().__init__("It cannot be normalized with zero vector (norm=0)")


class ConvergenceError(LinearAlgebraError):
    def __init__(self, method, max_iterations):
        self.method=method
        message=f"{method} did not converge after {max_iterations} iterations"
        super().__init__(message)


class InvalidRowIndexError(LinearAlgebraError):
    def __init__(self, message="El índice de la fila es inválido o está fuera de rango."):
        super().__init__(message)

class ZeroMultiplicationError(LinearAlgebraError):
    def __init__(self, message="División o multiplicación por cero detectada."):
        super().__init__(message)