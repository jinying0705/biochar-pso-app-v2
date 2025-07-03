import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
from pyswarm import pso

# Load training data
_data = pd.read_excel("确定6.0.xlsx")
X = _data.iloc[:, 0:10].values
y = _data.iloc[:, 10:19].values

# Scale input and output
scaler_X = StandardScaler().fit(X)
scalers_y = [StandardScaler().fit(y[:, i].reshape(-1, 1)) for i in range(y.shape[1])]

# Load trained models
models = []
for i in range(y.shape[1]):
    model = XGBRegressor()
    model.load_model(f"M-XGB_{i+1}.json")
    models.append(model)

# Constraints for output range
output_limits = [
    (18.8, 98.22), (4.1, 13.66), (0.3, 94.7), (3.29, 95.1), (0, 6.86),
    (0.7, 93.09), (3.8, 91.55), (0, 3.79), (0, 1.29)
]

def objective_function(conditions, fixed_A_properties, weights):
    full_input = np.hstack((fixed_A_properties, conditions))
    input_scaled = scaler_X.transform([full_input])

    score = 0
    for i, (model, scaler, weight) in enumerate(zip(models, scalers_y, weights)):
        pred_scaled = model.predict(input_scaled)
        pred = scaler.inverse_transform(pred_scaled.reshape(-1, 1))[0][0]

        if pred < output_limits[i][0] or pred > output_limits[i][1]:
            return 1e6  # penalty if out of range

        score += weight * pred
    return -score  # maximize

def run_pso_optimization(fixed_A_properties, weights):
    lb = [200, 1, 0]
    ub = [1000, 50, 240]

    opt_conditions, _ = pso(
        lambda c: objective_function(c, fixed_A_properties, weights),
        lb, ub, swarmsize=50, maxiter=50
    )

    full_input = np.hstack((fixed_A_properties, opt_conditions))
    input_scaled = scaler_X.transform([full_input])

    outputs = []
    for model, scaler in zip(models, scalers_y):
        pred_scaled = model.predict(input_scaled)
        pred = scaler.inverse_transform(pred_scaled.reshape(-1, 1))[0][0]
        outputs.append(pred)

    return opt_conditions, outputs


