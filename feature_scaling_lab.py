import numpy as np
import matplotlib.pyplot as plt
import copy, math

def plot_cost_i_w(X, y, J_history):
    """Simple cost plot"""
    plt.figure(figsize=(8, 4))
    plt.plot(J_history)
    plt.title("Cost vs Iterations")
    plt.xlabel("Iteration")
    plt.ylabel("Cost")
    plt.grid(True)
    plt.show()

def norm_plot(ax, data):
    """Simple normalized plot"""
    ax.hist(data, bins=20, density=True, alpha=0.7)
    return ax

def plt_equal_scale(X_norm, X_train):
    """Compare scaled vs unscaled"""
    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
    ax[0].scatter(X_train[:, 0], X_train[:, 1])
    ax[1].scatter(X_norm[:, 0], X_norm[:, 1])
    return fig, ax

def run_gradient_descent_feng(X, y, iterations=1000, alpha=0.01):
    """Your own gradient descent function"""
    m, n = X.shape
    w = np.zeros(n)
    b = 0
    J_history = []
    
    for i in range(iterations):
        # Compute predictions
        f_wb = X @ w + b
        # Compute gradients
        dj_dw = (1/m) * (X.T @ (f_wb - y))
        dj_db = (1/m) * np.sum(f_wb - y)
        # Update parameters
        w = w - alpha * dj_dw
        b = b - alpha * dj_db
        # Compute cost
        cost = (1/(2*m)) * np.sum((f_wb - y)**2)
        J_history.append(cost)
        
        if i % 100 == 0:
            print(f"Iteration {i:4}: Cost {cost:0.4e}")
    
    return w, b, J_history

def zscore_normalize_features(X):
    """Your own normalization function"""
    mu = np.mean(X, axis=0)
    sigma = np.std(X, axis=0)
    X_norm = (X - mu) / sigma
    return X_norm, mu, sigma