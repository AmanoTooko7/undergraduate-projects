import numpy as np

def convolve_with_numpy(array1, array2):
    return np.convolve(array1, array2)

#print(convolve_with_numpy([1, 2, 3], [4, 5, 6]))
a = [1, 2, 3]
b = [4, 5, 6]
result = [0] * (len(a) + len(b) - 1)
print(result)

