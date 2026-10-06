from matrix import Matrix
from exceptions import VectorInvalidError, ZeroVectorError,IncompatibleDimensionsError
import numpy as np

class Vector(Matrix):

    def __init__(self, data):
        super().__init__(data)

        if self.cols !=1:
            raise VectorInvalidError((self.rows, self.cols))

    def norm(self):
        return float(np.sqrt(sum(self.data**2)))

    def dot_product(self,vector_B):
        if self.rows!=vector_B.rows:
           raise IncompatibleDimensionsError("dot product", (self.rows, self.cols), (vector_B.rows, vector_B.cols))
        return float(np.sum(self.data*vector_B.data))

    def normalization(self):
        n=self.norm()
        if n==0:
            raise ZeroVectorError()
        return Vector(self.data/n)

    def __repr__(self):
        return f"Vector(\n{self.data}\n)"

