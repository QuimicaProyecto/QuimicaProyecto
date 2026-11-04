import substitution
from LU import lu_decomposition
from vector import Vector
from exceptions import  SingularMatrixError, DEFAULT_TOL
import numpy as np 

def forward_substitution(L,b):

    '''
    
    '''
    
    n=L.rows
    c=Vector(np.zeros((n,1)))

    for i in range(n):

        dot_prod=Vector(L[i,:i]).dot_product(Vector(c[:i]))

        c[i]=b[i]-dot_prod #b[i] is an raw array with shape (1,) it stills works due broadcasting

    return c

def back_substitution(U,c):

    n=U.rows
    x=Vector(np.zeros((n,1)))

    for i in range(n-1,-1,-1):

        dot_prod=Vector(U[i,i+1:]).dot_product(Vector(x[i+1:]))
        diff=c[i]-dot_prod

        if abs(U[i,i])<DEFAULT_TOL:
            raise SingularMatrixError()
        else:
            x[i]=diff/U[i,i]

    return x