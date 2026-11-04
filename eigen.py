from QR import qr_decomposition
from matrix import Matrix
from exceptions import DEFAULT_TOL,ConvergenceError
import numpy as np


def eigen_vals(A,max_iter):
    
    '''
Computes the eigenvalues of a square matrix A using the (unshifted) QR
algorithm: repeated QR decomposition and recombination in reverse order.

At each iteration, A is factored as A = QR (via Modified Gram-Schmidt,
without column pivoting -- pivoting would break the similarity
transformation this algorithm relies on) and reassembled as A' = RQ.
Since A' = Qᵀ·A·Q, this is an orthogonal similarity transformation, so A'
has the exact same eigenvalues as A at every step. Repeating this process
drives the strictly-below-diagonal entries toward zero, converging to an
upper triangular matrix whose diagonal holds the eigenvalues.

This is the baseline version of the algorithm: it does not use shifts,
Hessenberg reduction, or deflation, so it is slower to converge than a
production-grade implementation (e.g. LAPACK's dgeev/dsyev) and is not
guaranteed to converge for general matrices with complex conjugate
eigenvalues. For symmetric matrices, however, it converges reliably.

Args:
    A: square Matrix whose eigenvalues will be computed. Convergence is
        only guaranteed for symmetric matrices; for general matrices the
        algorithm may converge slowly or fail to converge at all.
    max_iter: maximum number of QR iterations to attempt before giving up.

Returns:
    A 1-D array with the computed eigenvalues (on the diagonal of the
    final iterate), in no particular order.

Raises:
    ConvergenceError: if the algorithm does not converge (the
        strictly-below-diagonal entries do not fall below DEFAULT_TOL)
        within max_iter iterations.

    '''
    E=A.copy()


    for i in range(max_iter):
        sum=0

        results=qr_decomposition(E)
        Q,R=results.Q,results.R
        E=R@Q

        for row in range(1,E.rows):
            for col in range(0,E.cols):
                if row>col:
                    sum+=abs(E[row,col])

        if sum< DEFAULT_TOL:
                break
        
    else:
        raise ConvergenceError("eigen values",max_iter) 
        

    return E.diagonal()

    


