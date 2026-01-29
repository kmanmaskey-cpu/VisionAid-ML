import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import StandardScaler

def load_house_data():
    """Load sample house price data"""
    X_train = np.array([
        [2104, 5, 1, 45],
        [1416, 3, 2, 40],
        [852, 2, 1, 35]
    ])
    y_train = np.array([460, 232, 178])
    return X_train, y_train

dlc = {
    'dlblue': '#0096ff',
    'dlorange': '#FF9300', 
    'dldarkred': '#C00000',
    'dlmagenta': '#FF40FF',
    'dlpurple': '#7030A0'
}

np.set_printoptions(precision=2)
plt.style.use('seaborn-v0_8-whitegrid')

X_train, y_train = load_house_data()
X_features = ['size(sqft)','bedrooms','floors','age']

scaler = StandardScaler()
X_norm = scaler.fit_transform(X_train)
print(f"Peak to Peak range by column in Raw        X:{np.ptp(X_train,axis=0)}")   
print(f"Peak to Peak range by column in Normalized X:{np.ptp(X_norm,axis=0)}")

sgdr = SGDRegressor(max_iter=1000)
sgdr.fit(X_norm, y_train)
print(sgdr)
print(f"number of iterations completed: {sgdr.n_iter_}, number of weight updates: {sgdr.t_}")

b_norm = sgdr.intercept_
w_norm = sgdr.coef_
print(f"model parameters:                   w: {w_norm}, b:{b_norm}")
print( "model parameters from previous lab: w: [110.56 -21.27 -32.71 -37.97], b: 363.16")

y_pred_sgd = sgdr.predict(X_norm)
y_pred = np.dot(X_norm, w_norm) + b_norm  
print(f"prediction using np.dot() and sgdr.predict match: {np.allclose(y_pred, y_pred_sgd)}")

print(f"Prediction on training set:\n{y_pred[:4]}" )
print(f"Target values \n{y_train[:4]}")

fig,ax=plt.subplots(1,4,figsize=(12,3),sharey=True)
for i in range(len(ax)):
    ax[i].scatter(X_train[:,i],y_train, label = 'target')
    ax[i].set_xlabel(X_features[i])
    ax[i].scatter(X_train[:,i],y_pred,color=dlc["dlorange"], label = 'predict')
ax[0].set_ylabel("Price"); ax[0].legend();
fig.suptitle("target versus prediction using z-score normalized model")
plt.show()