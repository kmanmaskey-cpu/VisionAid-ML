import numpy as np
import matplotlib.pyplot as plt
from practice import gradient_descent 

def load_house_data():
    X_train = np.array([
        [952, 2, 1, 65],
        [1244, 3, 2, 64],  
        [1947, 3, 2, 17]
    ])
    y_train = np.array([271.5, 232, 509.8])
    return X_train, y_train

X_train, y_train = load_house_data()
X_features = ['size(sqft)','bedrooms','floors','age']  
fig, ax = plt.subplots(1, 4, figsize=(12, 3))
for i in range(len(ax)):
    ax[i].scatter(X_train[:, i], y_train)
    ax[i].set_xlabel(X_features[i])
ax[0].set_ylabel("Price (1000's)")
plt.show()

initial_w = np.zeros(4)
initial_b = 0.0
iterations = 10
alpha1 = 9.9e-7
alpha2 = 1e-7

def plot_cost_i_w(X, y, J_history):
    """Simple cost plot"""
    plt.figure(figsize=(8, 4))
    plt.plot(J_history)
    plt.title("Cost vs Iterations")
    plt.xlabel("Iteration")
    plt.ylabel("Cost")
    plt.grid(True)
    plt.show()


w_final, b_final, hist1 = gradient_descent(
    X_train, y_train, 
    initial_w, initial_b,
    alpha=alpha1,
    num_iters=iterations)

plot_cost_i_w(X_train,y_train,hist1)

w_final, b_final, hist2 = gradient_descent(
    X_train, y_train, 
    initial_w, initial_b,
    alpha=alpha2,
    num_iters=iterations)

plot_cost_i_w(X_train,y_train,hist2)

def zscore_normalize_features(X):
    mu     = np.mean(X, axis=0)                
    sigma  = np.std(X, axis=0)                  
    X_norm = (X - mu) / sigma      
    return (X_norm, mu, sigma)

mu     = np.mean(X_train,axis=0)   
sigma  = np.std(X_train,axis=0) 
X_mean = (X_train - mu)
X_norm = (X_train - mu)/sigma      

fig,ax=plt.subplots(1, 3, figsize=(12, 3))
ax[0].scatter(X_train[:,0], X_train[:,3])
ax[0].set_xlabel(X_features[0]); ax[0].set_ylabel(X_features[3]);
ax[0].set_title("unnormalized")
ax[0].axis('equal')

ax[1].scatter(X_mean[:,0], X_mean[:,3])
ax[1].set_xlabel(X_features[0]); ax[1].set_ylabel(X_features[3]);
ax[1].set_title(r"X - $\mu$")
ax[1].axis('equal')

ax[2].scatter(X_norm[:,0], X_norm[:,3])
ax[2].set_xlabel(X_features[0]); ax[0].set_ylabel(X_features[3]);
ax[2].set_title(r"Z-score normalized")
ax[2].axis('equal')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
fig.suptitle("distribution of features before, during, after normalization")
plt.show()
X_norm, X_mu, X_sigma = zscore_normalize_features(X_train)
print(f"X_mu = {X_mu}, \nX_sigma = {X_sigma}")
print(f"Peak to Peak range by column in Raw        X:{np.ptp(X_train,axis=0)}")   
print(f"Peak to Peak range by column in Normalized X:{np.ptp(X_norm,axis=0)}")

def plt_equal_scale(X_norm, X_train):
    """Compare scaled vs unscaled"""
    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
    ax[0].scatter(X_train[:, 0], X_train[:, 1])
    ax[1].scatter(X_norm[:, 0], X_norm[:, 1])
    return fig, ax

def norm_plot(ax, data):
    """Simple normalized plot"""
    ax.hist(data, bins=20, density=True, alpha=0.7)
    return ax
    
fig,ax=plt.subplots(1, 4, figsize=(12, 3))
for i in range(len(ax)):
    norm_plot(ax[i],X_train[:,i],)
    ax[i].set_xlabel(X_features[i])
ax[0].set_ylabel("count");
fig.suptitle("distribution of features before normalization")
plt.show()

fig,ax=plt.subplots(1,4,figsize=(12,3))
for i in range(len(ax)):
    norm_plot(ax[i],X_norm[:,i],)
    ax[i].set_xlabel(X_features[i])
ax[0].set_ylabel("count"); 
fig.suptitle("distribution of features after normalization")

plt.show()

w_norm, b_norm, hist = gradient_descent(
    X_norm, 
    y_train,
    np.zeros(X_norm.shape[1]),
    0.0,                          
    1.0e-1,                    
    10000)          


m = X_norm.shape[0]
yp = np.zeros(m)
for i in range(m):
    yp[i] = np.dot(X_norm[i], w_norm) + b_norm


fig, ax = plt.subplots(1, 4, figsize=(12, 3), sharey=True)
for i in range(len(ax)):
    ax[i].scatter(X_train[:, i], y_train, label='target', color='blue')
    ax[i].set_xlabel(X_features[i])
    ax[i].scatter(X_train[:, i], yp, color='orange', label='predict', marker='s')
ax[0].set_ylabel("Price (1000's)")
ax[0].legend()
fig.suptitle("Target vs Prediction using Z-score normalized model")
plt.show()

x_house = np.array([1200, 3, 1, 40])
x_house_norm = (x_house - X_mu) / X_sigma
print(x_house_norm)
x_house_predict = np.dot(x_house_norm, w_norm) + b_norm
print(f" predicted price of a house with 1200 sqft, 3 bedrooms, 1 floor, 40 years old = ${x_house_predict*1000:0.0f}")

def find_best_alpha(X, y, initial_w, initial_b, alphas, num_iters=2000):
    """Try multiple learning rates and return the best one by final cost.

    Returns: (best_tuple, results)
      best_tuple = (alpha, final_cost, w, b, J_history)
      results = list of tuples for each alpha
    """
    results = []
    for a in alphas:
        w_try, b_try, J_hist = gradient_descent(
            X, y, initial_w.copy(), initial_b, alpha=a, num_iters=num_iters
        )
        final_cost = J_hist[-1] if len(J_hist) > 0 else np.inf
        results.append((a, final_cost, w_try, b_try, J_hist))


    results.sort(key=lambda t: t[1])
    best = results[0]

    plt.figure(figsize=(8, 5))
    for a, final_cost, w_try, b_try, J_hist in results:
        plt.plot(J_hist, label=f"{a:.0e}")
    plt.xlabel("Iteration")
    plt.ylabel("Cost")
    plt.title("Cost vs Iterations for different alphas")
    plt.legend(title='alpha')
    plt.grid(True)
    plt.show()

    return best, results



alphas = np.logspace(-7, -1, 13)
best_alpha_tuple, sweep_results = find_best_alpha(
    X_norm,
    y_train,
    np.zeros(X_norm.shape[1]),
    0.0,
    alphas,
    num_iters=2000,
)

print(f"Best alpha: {best_alpha_tuple[0]:.0e}, final cost: {best_alpha_tuple[1]:.6f}")

plt_equal_scale(X_train, X_norm)  
plt.show()