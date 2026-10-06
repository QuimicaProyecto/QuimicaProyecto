#QuickSort in-place Algorithm

#Auxiliar function
def partition(a,low,high):
    i=low-1
    pivot=a[high]
    for j in range(low,high):
        if a[j]<= pivot:
            i+=1
            a[i],a[j]=a[j],a[i]
    a[i+1],a[high]=a[high],a[i+1]
    return i+1

#Quicksort in-place algorithm (O(nlog n))
def quicksort_in_place(a,low=0,high=None):
    if high ==None:
        high=a.size-1
    if low<high:
        p_idx=partition(a,low,high)
        quicksort_in_place(a,low,p_idx-1)
        quicksort_in_place(a,p_idx+1,high)
    
    return a


def get_max(a):
    max=a[0]
    for val in a[1:]:
        if val >max:
            max=val
    return max


def get_min(a):
    min=a[0]
    for val in a[1:]:
        if val <min:
            min=val
    return min