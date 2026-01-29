import numpy as np
import matplotlib.pyplot as plt

def zscore_normalize_features(X):
    mu = np.mean(X, axis=0)
    sigma = np.std(X, axis=0)
    X_norm = (X - mu) / sigma
    return X_norm, mu, sigma

def run_gradient_descent_feng(X, y, iterations=1000, alpha=0.01):
    m, n = X.shape
    w = np.zeros(n)
    b = 0
    J_history = []
    
    for i in range(iterations):
        f_wb = X @ w + b
        dj_dw = (1/m) * (X.T @ (f_wb - y))
        dj_db = (1/m) * np.sum(f_wb - y)
        w = w - alpha * dj_dw
        b = b - alpha * dj_db
        cost = (1/(2*m)) * np.sum((f_wb - y)**2)
        J_history.append(cost)
        
        if i % 100 == 0:
            print(f"Iteration {i:4}: Cost {cost:0.4e}")
    
    return w, b, J_history

np.set_printoptions(precision=2)
x = np.arange(0, 20, 1)
y = 1 + x**2
X = x.reshape(-1, 1)


model_w, model_b, _ = run_gradient_descent_feng(X, y, iterations=1000, alpha=1e-2)
plt.scatter(x, y, marker='x', c='r', label="Actual Value")
plt.title("Added x**2 feature")
plt.plot(x,X@model_w + model_b, label="Predicted Value")  #@=dot product
plt.xlabel("X")
plt.ylabel("y")
plt.legend()
plt.show()

x = np.arange(0, 20, 1)
y = x**2


X = np.c_[x, x**2, x**3]
X_features = ['x','x^2','x^3']
print("X shape:", X.shape)
print(X)


model_w, model_b, _ = run_gradient_descent_feng(X, y, iterations=1000, alpha=1e-7)

plt.scatter(x, y, marker='x', c='r', label="Actual Value")
plt.title("x, x**2, x**3 features")
plt.plot(x, X @ model_w + model_b, label="Predicted Value")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show()

fig,ax=plt.subplots(1, 3, figsize=(12, 3), sharey=True)
for i in range(len(ax)):
    ax[i].scatter(X[:,i],y)
    ax[i].set_xlabel(X_features[i])
ax[0].set_ylabel("y")
plt.show()

x = np.arange(0,20,1)
X = np.c_[x, x**2, x**3]
print(f"Peak to Peak range by column in Raw        X:{np.ptp(X,axis=0)}")


X = zscore_normalize_features(X)     
print(f"Peak to Peak range by column in Normalized X:{np.ptp(X,axis=0)}")

x = np.arange(0,20,1)
y = x**2

X = np.c_[x, x**2, x**3]
X = zscore_normalize_features(X) 

model_w, model_b = run_gradient_descent_feng(X, y, iterations=100000, alpha=1e-1)

plt.scatter(x, y, marker='x', c='r', label="Actual Value"); plt.title("Normalized x x**2, x**3 feature")
plt.plot(x,X@model_w + model_b, label="Predicted Value"); plt.xlabel("x"); plt.ylabel("y"); plt.legend(); plt.show()

x = np.arange(0,20,1)
y = np.cos(x/2)

X = np.c_[x, x**2, x**3,x**4, x**5, x**6, x**7, x**8, x**9, x**10, x**11, x**12, x**13]
X = zscore_normalize_features(X) 

model_w,model_b = run_gradient_descent_feng(X, y, iterations=1000000, alpha = 1e-1)

plt.scatter(x, y, marker='x', c='r', label="Actual Value"); plt.title("Normalized x x**2, x**3 feature")
plt.plot(x,X@model_w + model_b, label="Predicted Value"); plt.xlabel("x"); plt.ylabel("y"); plt.legend(); plt.show()