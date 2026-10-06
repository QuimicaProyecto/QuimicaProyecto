import numpy as np
import Utils as U

def _sum(X, axis=None):
    array = np.array(X, dtype=float)

    if array.ndim == 1:
         array = array.reshape(1, -1)

    rows, cols = array.shape

    if axis is None:
        tot_sum = 0.0
        for element in array.flat:
           tot_sum += element
        return tot_sum

    if axis == 0:
        result = np.zeros(cols)
        for col in range(cols):
            col_sum = 0.0
            for row in range(rows):
                col_sum += array[row, col]
            result[col] = col_sum
        return result
    
    if axis == 1:
        if np.array(X).ndim == 1:
            raise ValueError("Axis 1 only works with arrays that are not 1D.")
        result = np.zeros(rows)
        for row in range(rows):
            row_sum = 0.0
            for col in range(cols):
                row_sum += array[row, col]
            result[row] = row_sum
        return result
    
    raise ValueError("The axis must be 0, 1, or None.")

def mean(X, axis=None):
    array = np.array(X, dtype=float)

    if array.ndim == 1:
         array = array.reshape(1, -1)

    rows, cols = array.shape
    
    if axis is None:
        return _sum(X, axis) / array.size
    
    if axis == 0:
        result = _sum(X, axis)
        for i in range(len(result)):
             result[i] /= rows
        return result
    
    if axis == 1:
        result = _sum(X, axis)
        for i in range(len(result)):
             result[i] /= cols
        return result

def var(X, axis=None, ddof=1):
    array = np.array(X, dtype=float)
    
    if array.ndim == 1: 
        array = array.reshape(1, -1)
    
    rows, cols = array.shape

    if axis is None:
        medias_calc = mean(X, axis)
        var_sum = 0.0 
        for element in array.flat:
            residual = element - medias_calc
            squared = residual ** 2
            var_sum += squared 
        return var_sum / (array.size - ddof)
    
    if axis == 0:
        medias_calc = mean(X, axis)
        cols_var = np.zeros(cols) 
        for col in range(cols):
            var_sum = 0.0 
            for row in range(rows):
                residual = array[row, col] - medias_calc[col]
                squared = residual ** 2
                var_sum += squared 
            cols_var[col] = var_sum / (rows - ddof)
        return cols_var
    
    if axis == 1:
        if np.array(X).ndim == 1:
            raise ValueError("Axis 1 only works with arrays that are not 1D.")
        medias_calc = mean(X, axis)
        rows_var = np.zeros(rows)
        for row in range(rows):
            var_sum = 0.0
            for col in range(cols):
                residual = array[row, col] - medias_calc[row]
                squared = residual ** 2
                var_sum += squared
            rows_var[row] = var_sum / (cols - ddof)
        return rows_var
    
    raise ValueError("The axis must be 0, 1, or None.")

def std(X, axis=None, ddof=1):
    return var(X, axis, ddof) ** 0.5

def get_range(X, axis=None):
    array = np.array(X, dtype=float)

    if array.ndim == 1:
        array = array.reshape(1, -1)

    rows, cols = array.shape

    if axis is None:
        data = array.flatten()
        min_val = U.get_min(data)
        max_val = U.get_max(data)
        return max_val - min_val
    
    if axis == 0:
        col_range = np.zeros(cols)
        for col in range(cols):
            column_data = np.zeros(rows)
            for row in range(rows):
                column_data[row] = array[row, col]
            c_min = U.get_min(column_data)
            c_max = U.get_max(column_data)
            col_range[col] = c_max - c_min
        return col_range
    
    if axis == 1:
        if np.array(X).ndim == 1:
            raise ValueError("Axis 1 only works with arrays that are not 1D.")
        row_range = np.zeros(rows)
        for row in range(rows):
            row_data = np.zeros(cols)
            for col in range(cols):
                row_data[col] = array[row, col]
            r_min = U.get_min(row_data)
            r_max = U.get_max(row_data)
            row_range[row] = r_max - r_min
        return row_range

    raise ValueError("The axis must be 0, 1, or None.")

def median(X, axis=None):
    array = np.array(X, dtype=float)

    if array.ndim == 1:
        array = array.reshape(1, -1)

    rows, cols = array.shape

    if axis is None:
        data = array.flatten()
        lenght = data.size
        arranged_data = U.quicksort_in_place(data)
        
        if lenght % 2 != 0:
            return arranged_data[lenght // 2]
        else:
            mid_right = lenght // 2
            mid_left = mid_right - 1
            return 0.5 * (arranged_data[mid_left] + arranged_data[mid_right])
        
    if axis == 0:
        col_median = np.zeros(cols)
        for col in range(cols):
            column_data = np.zeros(rows)
            for row in range(rows):
                column_data[row] = array[row, col]
            
            column_data_arranged = U.quicksort_in_place(column_data)
            lenght = column_data_arranged.size

            if lenght % 2 != 0:
                med = column_data_arranged[lenght // 2]
            else:
                mid_right = lenght // 2
                mid_left = mid_right - 1
                med = 0.5 * (column_data_arranged[mid_left] + column_data_arranged[mid_right])
            col_median[col] = med
        return col_median
    
    if axis == 1:
        row_median = np.zeros(rows)
        for row in range(rows):
            row_data = np.zeros(cols)
            for col in range(cols):
                row_data[col] = array[row, col]
            
            row_data_arranged = U.quicksort_in_place(row_data)
            lenght = row_data_arranged.size

            if lenght % 2 != 0:
                med = row_data_arranged[lenght // 2]
            else:
                mid_right = lenght // 2
                mid_left = mid_right - 1
                med = 0.5 * (row_data_arranged[mid_left] + row_data_arranged[mid_right])
            row_median[row] = med
        return row_median

    raise ValueError("The axis must be 0, 1, or None.")

def covariance_matrix(X):
    data = np.array(X, dtype=float)
    rows, cols = data.shape

    cov_mat = np.zeros((cols, cols))
    medias = mean(X, axis=0)

    for i in range(cols):
        for j in range(cols):
            suma_acumulada = 0.0

            for k in range(rows):
                x_residual = data[k, i] - medias[i]
                y_residual = data[k, j] - medias[j]
                suma_acumulada += x_residual * y_residual

            cov_mat[i, j] = suma_acumulada / (rows - 1)
    
    return cov_mat
                
def correlation_matrix(X):
    data = np.array(X, dtype=float)
    rows, cols = data.shape
    
    cov_mat = covariance_matrix(X)
    corr_mat = np.zeros((cols, cols))
    stand_dev = std(X, axis=0)

    for i in range(cols):
        for j in range(cols):
            corr = cov_mat[i, j] / (stand_dev[i] * stand_dev[j])
            corr_mat[i, j] = corr
    
    return corr_mat






