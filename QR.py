from matrix import Matrix
from exceptions import IncompatibleDimensionsError, InvalidRowIndexError, ZeroMultiplicationError, SingularMatrixError, DEFAULT_TOL
from vector import Vector
from dataclasses import dataclass
import numpy as np

#We create a dataclass in order to store all the results of the decomposition algorithm
@dataclass(frozen=True)
class QRResults:
    #Results of A=QR decomposition
    Q: Matrix
    R: Matrix


#Thin version
def qr_decomposition(A):

    '''
Performs A = QR decomposition of a matrix A using the Modified Gram-Schmidt
method, producing the "economy" (reduced) QR factorization.

Args:
    A: Matrix to decompose. Must have at least as many rows as columns
        (A.rows >= A.cols) for the decomposition to be well-defined --
        otherwise, at least one column is guaranteed to be linearly
        dependent on the others.

Returns:
    QRResults: an object with the following attributes:
        Q: matrix with orthonormal columns (orthogonal and unit-length).
        R: upper triangular matrix holding the norms (diagonal) and
            projections (off-diagonal) computed during orthogonalization.

Raises:
    SingularMatrixError: if, at some step, the norm of the already-
        orthogonalized vector falls below DEFAULT_TOL, indicating that
        the corresponding column of A is a linear combination of the
        previous columns. This necessarily occurs if A.cols > A.rows.

    '''

    #Storing the dimensions of our matrix
    n=A.rows
    m=A.cols

    #We initialize the R matrix as a zero matrix
    R=Matrix.zero_matrix(m,m)

    #We initialize the Q matrix as a zero matrix
    Q=Matrix.zero_matrix(n,m)

    #Main loop
    for j in range(m):
        v= Vector(A[:,j])
        for i in range(0,j):
            R[i,j]=Vector(Q[:,i]).dot_product(v)
            v=v-R[i,j]*Vector(Q[:,i])

        if v.norm()<DEFAULT_TOL:
            raise SingularMatrixError()
        else:
            R[j,j]=v.norm()

        #Q[:,j]=(v/R[j,j]).data.flatten() # Linea original
        Q[:,j]=(np.array(v.data) / R[j,j]).flatten() #We

        # v.data: extrae los números puros
        # np.array: convierte esos números en un arreglo nativo de Numpy
        # / R[j,j]: divide matrices entre números
        # .flatten(): toma la cuadrícula de resultados y la aplana en una sola lista para encajar dentro de la columna Q[:,j]

    return QRResults(Q,R)

def qr_decomposition_pivoting(A):

    '''
Performs AP = QR decomposition of a matrix A using the Modified Gram-Schmidt
method with column pivoting, producing the "economy" (reduced) QR
factorization.

Unlike plain qr_decomposition, which processes columns in their original
order, this version chooses, at each step, the remaining column with the
largest norm (after already subtracting the projections of the previously
computed Q columns) and processes that one next ("good columns come
first"). This makes rank deficiency easier to detect reliably -- the
diagonal of R ends up sorted from largest to smallest in absolute value --
though it does not by itself improve the numerical stability of the
computation (that improvement comes from using Householder reflections
instead of Gram-Schmidt, not from pivoting).

Args:
    A: Matrix to decompose. Must have at least as many rows as columns
        (A.rows >= A.cols) for the decomposition to be well-defined --
        otherwise, at least one column is guaranteed to be linearly
        dependent on the others. NOTE: A is mutated in place during the
        decomposition (its columns are permuted and progressively
        orthogonalized) -- pass a copy if the original matrix must be
        preserved.

Returns:
    QRPivotingResults: an object with the following attributes:
        Q: matrix with orthonormal columns (orthogonal and unit-length).
        R: upper triangular matrix holding the norms (diagonal) and
            projections (off-diagonal) computed during orthogonalization,
            with diagonal entries sorted from largest to smallest in
            absolute value as a result of the pivoting.
        P: permutation matrix (m x m) such that A_original @ P reorders
            the columns of A in the same order they were processed,
            satisfying A_original @ P = Q @ R.

Raises:
    SingularMatrixError: if, at some step, the largest remaining column
        norm falls below DEFAULT_TOL, indicating that all remaining
        columns are linear combinations of the already-processed ones
        (i.e. A does not have full column rank). This necessarily occurs
        if A.cols > A.rows.

    '''

    #Setting the dimensions of our matrix
    n=A.rows
    m=A.cols

    #We initialize our matrices Q,R and P
    Q=Matrix.zero_matrix(n,m)
    R=Matrix.zero_matrix(m,m)
    P=Matrix.identity(m)

    for j in range(m):

        k=find_best_col(A,j) #index of the best column

        #Swapinng our columns
        A.swap_cols(k,j)
        P.swap_cols(k,j)
        
        for row in range(j):
            R[row,k],R[row,j]=R[row,j], R[row,k]
        v=Vector(A[:,j]) #storing that colum

        R[j,j]=v.norm() #calculating it´s norm
        Q[:,j]=(v/R[j,j]).data.flatten() #normalizing that column and updating Q

        for i in range(j+1,m):
            R[j,i]=Vector( Q[:,j]).dot_product(Vector(A[:,i]))

            A[:,i]=A[:,i]- R[j,i] * Vector(Q[:,j]).data.flatten()

    return QRResults(Q,R,P)

def find_best_col(A,start_col):
    best_col=start_col
    best_norm= 0

    for i in range(start_col,A.cols): #Loop that iterates through all the columns of our matrix
        norm=Vector(A[:,i]).norm() #We calculate the norm of our current column

        if norm>best_norm: #comparing the norms
            best_norm=norm #Updating the best norm variable and it´s index
            best_col=i

    if best_norm<DEFAULT_TOL:
        raise SingularMatrixError()

    return best_col #Returning the index of our column with biggest norm

