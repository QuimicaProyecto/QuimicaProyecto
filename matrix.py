import numpy as np
from exceptions import IncompatibleDimensionsError,Nonsquarematrixerror

class Matrix:
    def __init__(self,data):
        self.data=np.array(data,dtype=float)

        if  self.data.ndim == 1:
            self.data=self.data.reshape(-1,1)

        self.rows,self.cols=self.data.shape

    def __add__(self,matrix_B):
        if (self.rows != matrix_B.rows) or (self.cols != matrix_B.cols):
            raise IncompatibleDimensionsError("sum", (self.rows, self.cols), (matrix_B.rows, matrix_B.cols))

        return type(self)(self.data+ matrix_B.data)

    def __sub__(self,matrix_B):
        if (self.rows != matrix_B.rows) or (self.cols != matrix_B.cols):
             raise IncompatibleDimensionsError("substraction", (self.rows, self.cols), (matrix_B.rows, matrix_B.cols))
            
        return type(self)(self.data- matrix_B.data)

    def __mul__(self,c):
        if not isinstance(c, (int,float)):
            return NotImplemented

        return type(self)(self.data*c)

    def __rmul__(self,c):
        return self.__mul__(c)

    def __matmul__(self, matrix_B):

        if self.cols != matrix_B.rows:
             raise IncompatibleDimensionsError("multiplication", (self.rows, self.cols), (matrix_B.rows, matrix_B.cols))
        
        return type(self)(self.data @ matrix_B.data)

    def trace(self):
        if self.rows!=self.cols:
            raise Nonsquarematrixerror((self.rows,self.cols))
        return self.data.trace()

    def diagonal(self):
        return self.data.diagonal()

    def transpose(self):
        return Matrix(self.data.T)

    def is_symmetric(self):
        if self.rows != self.cols:
            return False
        return np.allclose(self.data,self.data.T)


    def __repr__(self):
        return f"Matrix(\n{self.data}\n)"

    def __getitem__(self,keys):
        return self.data[keys]

    def __setitem__(self, keys, value):
            self.data[keys] = value

    def copy(self):
        new_mat=np.copy(self.data)
        return type(self)(new_mat)

    def swap_rows(self,i,j):

        temp=np.copy(self[i,:])
        self[i,:]=self[j,:]
        self[j,:]=temp
