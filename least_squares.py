from QR import qr_decomposition_pivoting
from substitution import back_substitution


def OLS(A, b):
    result = qr_decomposition_pivoting(A)
    Q, R, P = result.Q, result.R, result.P

    c = Q.transpose() @ b     
    y = back_substitution(R, c)  
    x_hat = P @ y               

    return x_hat

