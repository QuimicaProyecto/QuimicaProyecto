from matrix import Matrix
from exceptions import Nonsquarematrixerror, IncompatibleDimensionsError, InvalidRowIndexError, ZeroMultiplicationError, SingularMatrixError
from vector import Vector
from dataclasses import dataclass
import numpy as np

#Global tolerance 
TOL=1e-10

#We create a dataclass in order to return all the results of the decomposition
@dataclass(frozen=True)
class LUResults: #We make it inmutable
    #Results of a PA=LU decomposition with partial pivoting
    L: Matrix
    U: Matrix
    P: Matrix
    num_swaps: int

#Auxiliar functions
def find_pivot_row(A,col,start_row): 

    '''
    Finds the the element with greater absolute value in the whole column

    Args:
        A: Matrix we´re working with
        col: Index of the column we´re moving through
        start_row: the index of the row where we start to search our best pivot

    Returns:
        best_pivot: The element with the greater absolute value of the column
        best_row: The index of the row where our best pivot is

    Raises:
        SingularMatrixError: If all the elements of the column are zero
    '''
    best_pivot=0
    best_row=start_row

    for row in range(start_row,A.rows):
        if abs(A[row,col]) > abs(best_pivot):
            best_pivot=A[row,col]
            best_row=row

    if abs(best_pivot)<TOL:
        raise SingularMatrixError()

    return best_pivot, best_row


#LU decomposition function
def lu_decomposition(A,partial_pivoting=True): 

    '''
    Performs PA = LU decomposition of a given square matrix using Gaussian
    elimination, with optional partial pivoting.

Args:
    A: the Matrix to decompose (must be square).
    partial_pivoting: if True (default), searches each column for the
        element with the largest absolute value as pivot, swapping rows
        when needed to improve numerical stability. If False, uses the
        diagonal element directly as pivot, without searching or swapping
        rows -- faster, but may fail or be numerically unstable if that
        element is zero or very small.

Returns:
    LUResults: an object with the following attributes:
        L: lower triangular matrix holding the multipliers used during
            Gaussian elimination (unit diagonal).
        U: upper triangular matrix, the result of applying row operations
            to the original matrix.
        P: permutation matrix recording the row swaps performed.
        num_swaps: number of row swaps performed during the algorithm
            (useful for determinant sign calculation).

Raises:
    NonSquareMatrixError: if A is not a square matrix.
    SingularMatrixError: if, at some step of the elimination, every
        element of the current column (from the pivot row downward) is
        zero, indicating that A is singular.
    '''

    if A.cols != A.rows:
        raise NonSquareMatrixError((A.rows,A.cols))

    #Creating a copy of A
    U=A.copy()

    #Initiating L and P
    L=Matrix.identity(A.rows)
    P=Matrix.identity(A.rows)

    #Initiating num_swaps 
    num_swaps=0
    #Defining dimension
    n=A.cols

    for k in range(n-1):

        if not partial_pivoting:
            pivot= U[k,k]

            if abs(pivot)< TOL:
                raise SingularMatrixError()

        else:
            pivot,best_row=find_pivot_row(U,k,k)

            if best_row == k:
                pivot=U[k,k]

            else:
                U.swap_rows(best_row,k)
                pivot=U[k,k]
                num_swaps+=1
                #Updating P
                P.swap_rows(best_row,k)
                #Updating L
                temp = np.copy(L[best_row, :k])
                L[best_row, :k] = L[k, :k]
                L[k, :k] = temp
            

        for i in range(k+1,n):
            factor= U[i,k]/pivot
            L[i,k]=factor
            U.add_scaled_row(i,k,-factor)
            

    return LUResults(L,U,P,num_swaps)

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

        if abs(U[i,i])<TOL:
            raise SingularMatrixError()
        else:
            x[i]=diff/U[i,i]

    return x

def solve_system(A,b):
    L,U,P,num_swaps=lu_decomposition(A)
    Pb=Vector(P.data @ b.data) #Since we resolve the system LUx=Pb
    c=forward_substitution(L,b)
    x=back_substitution(U,c)

    return x

def determinant(A):
    # Calcula el determinante de una matriz cuadrada A usando la descomposición LU.
    try:
        resultados = lu_decomposition(A)
    except SingularMatrixError:
        # Si el algoritmo detecta que es singular durante el proceso, 
        return 0.0

    # Extraemos las variables que necesitamos de LUResults
    U = resultados.U
    num_swaps = resultados.num_swaps
    n = U.rows
    
    # Aplicamos la Productoria (Π) a la diagonal (U_ii)
    det = 1.0
    for i in range(n):
        det *= U[i, i]
        
    # Ajustamos el signo con (-1)^num_swaps
    det = det * ((-1) ** num_swaps)
    
    return det