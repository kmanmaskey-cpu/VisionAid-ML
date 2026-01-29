import copy, math
import numpy as np
import matplotlib.pyplot as plt
X_train = np.array([[2104, 5, 1, 45], [1416, 3, 2, 40], [852, 2, 1, 35]]) # features: size, bedrooms, floors, age
y_train = np.array([460, 232, 178]) # target values: price in $1000s
print(f"X Shape: {X_train.shape}, X Type:{type(X_train)})")
print(X_train)
print(f"y Shape: {y_train.shape}, y Type:{type(y_train)})")
print(y_train)
b_init = 785.1811367994083 # initial bias term
w_init = np.array([ 0.39133535, 18.75376741, -53.36032453, -26.42131618]) # initial weights
print(f"w_init shape: {w_init.shape}, b_init type: {type(b_init)}")
def predict(x, w, b): #predixting price for one house
    p = np.dot(x, w) + b 
    return p  
x_vec = X_train[0,:]
print(f"x_vec shape {x_vec.shape}, x_vec value: {x_vec}")


f_wb = predict(x_vec,w_init, b_init)
print(f"f_wb shape {f_wb.shape}, prediction: {f_wb}")

def compute_cost(X, y, w, b): #find error in prediction
    m = X.shape[0]
    cost = 0.0
    for i in range(m):                                
        f_wb_i = np.dot(X[i], w) + b           
        cost = cost + (f_wb_i - y[i])**2       
    cost = cost / (2 * m)                     
    return cost
cost = compute_cost(X_train, y_train, w_init, b_init)
print(f'Cost at optimal w : {cost}')


def gradient(X, y, w, b): #finding how much the weight and bias should be changed to reduce error
    m,n = X.shape[0], X.shape[1]
    dj_dw = np.zeros(n)    
    dj_db = 0.0
    dj_dw_i = np.zeros(n)  
    dj_db_i = 0.0           
    for i in range(m):                                
        f_wb_i = np.dot(X[i], w) + b
        for j in range(n) :        
            dj_dw_i[j] = dj_dw_i[j]+(f_wb_i - y[i]) * X[i, j]      
            dj_db_i = dj_db_i+(f_wb_i - y[i])     
    dj_dw = dj_dw_i/m
    dj_db = dj_db_i/m
    return dj_dw, dj_db
tdj_dw,tdj_db = gradient(X_train, y_train, w_init, b_init)
print(f'tdj_dw shape: {tdj_dw.shape}, tdj_db shape: {tdj_db.shape}')
print(f'tdj_dw: {tdj_dw}')
print(f'tdj_db: {tdj_db}')

def gradient_descent(X, y, w_in, b_in, alpha, num_iters):  # finds the optimal weight and bias using gradient descent
    w = copy.deepcopy(w_in)
    b = b_in
    J_history = []
    for i in range(num_iters):
        dj_dw, dj_db = gradient(X, y, w, b)   
        w = w - alpha * dj_dw               
        b = b - alpha * dj_db                
        if i<100000:                         
            J_history.append(compute_cost(X, y, w, b))
        if i% math.ceil(num_iters / 10) == 0:
            print(f"Iteration {i}: Cost {J_history[-1]}   ")
    return w, b, J_history



initial_w = np.zeros_like(w_init)
initial_b = 0.
iterations = 99999
alpha = 5.0e-7
w_final, b_final, J_hist = gradient_descent(X_train, y_train,initial_w, initial_b,alpha, iterations)
print(f"b,w found by gradient descent: {b_final},{w_final} ")
m= X_train.shape[0]
for i in range(m): #print predictions for each house
    print(f"prediction: {np.dot(X_train[i], w_final) + b_final:0.2f}, target value: {y_train[i]}")


