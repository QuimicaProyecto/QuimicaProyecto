from LU import find_pivot_row
from matrix import Matrix
import numpy as np

array1=[[4,5,6],
       [0,1,3],
       [2,4,5]]

array2=[[0,5,6],
       [4,1,3],
       [2,4,5]]

array3=[[0,5,6],
       [0,1,3],
       [0,4,5]]

mat1=Matrix(array1)
mat2=Matrix(array2)
mat3=Matrix(array3)

best_pivot1,best_row1=find_pivot_row(mat1,0,0)
best_pivot2,best_row2=find_pivot_row(mat2,0,0)

print(f"CASE 1\nbest pivot: {best_pivot1}\nbest row: {best_row1}\n")
print(f"CASE 2\nbest pivot: {best_pivot2}\nbest row: {best_row2}\n")

try:
    best_pivot3, best_row3 = find_pivot_row(mat3, 0, 0)
    print(f"CASO 3\nbest pivot: {best_pivot3}\nbest row: {best_row3}")
except Exception as e:
    print(f"CASO 3 (esperado): se lanzó {type(e).__name__}: {e}")