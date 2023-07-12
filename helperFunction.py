import numpy as np

def reshape(arr):
        return np.array(arr).reshape(-1, 1, arr.shape[1])