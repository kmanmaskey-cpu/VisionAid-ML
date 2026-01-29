import numpy as np
import matplotlib.pyplot as plt
input_array = np.array([1,2,3])
exp_array = np.exp(input_array)
X = np.array([[0.5, 1.5], [1,1], [1.5, 0.5], [3, 0.5], [2, 2], [1, 2.5]])
y = np.array([0, 0, 0, 1, 1, 1]).reshape(-1,1) 
print(y)