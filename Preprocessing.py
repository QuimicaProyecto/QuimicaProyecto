import numpy as np
import Utils as U
import Descriptive_statistics as ds
from matrix import Matrix
from vector import Vector
from QR import qr_decomposition
from substitution import back_substitution
from scipy.special import factorial

def zero_variance(matrix):
    deviations=ds.std(matrix,axis=0)

    useful_cols=deviations>1e-8

    filtered_matrix=matrix[:,useful_cols]

    original_cols=matrix.shape[1]
    new_cols=filtered_matrix.shape[1]
    deleted=original_cols-new_cols

    print(f"Filter applied: {deleted} wavelengths containing no information were removed.")

    return filtered_matrix,useful_cols

def mean_centering(X):

    data=np.array(X,dtype=float)
    rows,cols=data.shape

    transformed_matrix= np.zeros((rows,cols))
    means=ds.mean(X,axis=0)

    for i in range(rows):
        for j in range(cols):

            transformed_matrix[i,j]=data[i,j]-means[j]

    return transformed_matrix

def standard(X):

    data=np.array(X,dtype=float)
    rows,cols=data.shape

    transformed_matrix= np.zeros((rows,cols))
    means=ds.mean(X,axis=0)
    sta_dev=ds.std(X,axis=0)

    for i in range(rows):
        for j in range(cols):

            z_value= (data[i,j]-means[j])/sta_dev[j]
            transformed_matrix[i,j]=z_value

    return transformed_matrix


def Min_Max_scaler(X):

    data=np.array(X,dtype=float)
    rows,cols=data.shape

    transformed_matrix= np.zeros((rows,cols))
    ranges=ds.get_range(X,axis=0)

    min_vals=np.zeros(cols)
    for j in range(cols):
        col=data[:,j]
        min_vals[j]=U.get_min(col)

    for i in range(rows):
        for j in range(cols):
            
            if ranges[j]==0:
                transformed_matrix[i,j]=0.0
            else:
                transformed_matrix[i,j]=(data[i,j]-min_vals[j])/ranges[j]


    return transformed_matrix




def sav_gol_matrix(M,N):

    n=Vector(np.array([i for i in range(-M, M+1)], dtype=float)) #Window

    A=Matrix.zero_matrix(2*M+1,N+1) #Vandermonde matrix
    H=Matrix.zero_matrix(N+1,2*M+1) #Weights matrix

    #Filling the Vandermonde matrix
    for i in range(A.cols):
        A[:,i]=n.data.flatten()**i

    #using QR decomposition 
    results=qr_decomposition(A)
    Q,R=results.Q,results.R

    #solving the system Ra=Q^TI by back-substitution 
    for i in range(2*M+1):

        b=Vector(Q[i,:])
        H[:,i]=back_substitution(R,b).data.flatten()

    return H

def sav_gol_apply(A,M,N,der=0):

    #Validating parameter
    if M<=0:
        raise ValueError(f"The window must have positive values") 

    if N<0:
        raise ValueError("There´s no negative polyonomials")

    if A.cols<2*M+1:
            raise ValueError(f"The matrix A must have at least {2*M+1} columns to apply the window with {M} points") 
        #For further application it is important to apply a padding auxiliar function

    if N> 2*M:
        raise ValueError("Underdetermined system, you need at least as many points as the polynomial grade")
    
    transformed_matrix=A.copy()
    H=sav_gol_matrix(M,N)
    
    weights=factorial(der)*Vector(H[der,:])
    
    #Edges and convolution
    for i in range(A.rows):
        for j in range(M,A.cols-M):
                window=Vector(A[i,j-M:j+M+1])
                transformed_matrix[i,j]=window.dot_product(weights)
                
            
    return transformed_matrix

def sav_gol_smoothing_pol(A,M,N,):
    return sav_gol_apply(A,M,N,der=0)

def sav_gol_der(A,M,N,der=1):
    return sav_gol_apply(A,M,N,der)