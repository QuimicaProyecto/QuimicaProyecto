from substitution import forward_substitution, back_substitution
from LU import lu_decomposition
from vector import Vector

def solve_system(A,b):
    L,U,P,num_swaps=lu_decomposition(A)
    Pb=Vector(P.data @ b.data) #Since we resolve the system LUx=Pb
    c=forward_substitution(L,b)
    x=back_substitution(U,c)

    return x