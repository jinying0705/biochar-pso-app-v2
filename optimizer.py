# optimizer.py
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
from pyswarm import pso

# Load data and models once
_data = pd.read_excel("确定6.0.xlsx")
X = _data.iloc[:, 0:10].values
y = _data.iloc[:, 10:19].values

scaler_X = StandardScaler().fit(X)
scalers_y = [StandardScaler().fit(y[:, i].reshape(-1, 1)) for i in range(y.shape[1])]

models = []
for i in range(y.shape[1]):
    model = XGBRegressor()
    model.load_model(f"M-XGB_{i+1}.json")
    models.append(model)

# Output constraints (can be adjusted)
output_limits = [
    (18.8, 98.22), (4.1, 13.66), (0.3, 94.7), (3.29, 95.1), (0, 6.86),
    (0.7, 93.09), (3.8, 91.55), (0, 3.79), (0, 1.29)
]

def objective_function(conditions, fixed_A_properties, weights):
    combined_input = np.hstack((fixed_A_properties, conditions))
    combined_input_scaled = scaler_X.transform([combined_input])

    total = 0
    for i, (model, scaler, weight) in enumerate(zip(models, scalers_y, weights)):
        pred_scaled = model.predict(combined_input_scaled)
        pred = scaler.inverse_transform(pred_scaled.reshape(-1, 1))[0][0]

        if pred < output_limits[i][0] or pred > output_limits[i][1]:
            return 1e6  # penalty for out-of-bound prediction

        total += weight * pred
    return -total  # negative for maximization

def run_pso_optimization(fixed_A_properties, weights):
    lb = [200, 1, 0]      # Lower bounds: temp, rate, time
    ub = [1000, 50, 240]  # Upper bounds

    opt_conditions, _ = pso(
        lambda cond: objective_function(cond, fixed_A_properties, weights),
        lb, ub, swarmsize=50, maxiter=50, omega=0.5, phip=2, phig=2
    )

    # Predict with best condition
    full_input = np.hstack((fixed_A_properties, opt_conditions))
    full_scaled = scaler_X.transform([full_input])

    outputs = []
    for model, scaler in zip(models, scalers_y):
        pred_scaled = model.predict(full_scaled)
        pred = scaler.inverse_transform(pred_scaled.reshape(-1, 1))[0][0]
        outputs.append(pred)

    return opt_conditions, outputs

