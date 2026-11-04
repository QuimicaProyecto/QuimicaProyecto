from matrix import Matrix
from exceptions import VectorInvalidError, ZeroVectorError, IncompatibleDimensionsError
import numpy as np

class Vector(Matrix):

    def __init__(self, data):
        super().__init__(data)

        if self.cols !=1:
            raise VectorInvalidError((self.rows, self.cols))

    def norm(self):
        # np.sum procesa el arreglo correctamente y .item() extrae el número puro
        return np.sqrt(np.sum(np.array(self.data)**2)).item()

    def dot_product(self,vector_B):
        if self.rows!=vector_B.rows:
           raise IncompatibleDimensionsError("dot product", (self.rows, self.cols), (vector_B.rows, vector_B.cols))

        return np.sum(np.array(self.data) * np.array(vector_B.data)).item()

    def normalization(self):
        n=self.norm()
        if n==0:
            raise ZeroVectorError()
        # Mantenemos compatibilidad usando arreglos para la división
        return Vector((np.array(self.data)/n).tolist())

    def __repr__(self):
        return f"Vector(\n{self.data}\n)"