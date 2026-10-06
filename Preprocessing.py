import numpy as np
import Utils as U
import Descriptive_statistics as ds

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


