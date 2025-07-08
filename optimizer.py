import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
from pyswarm import pso

# ======= Step 1: Load training data =======
_data = pd.read_excel("确定6.0.xlsx")
X = _data.iloc[:, 0:10].values
y = _data.iloc[:, 10:19].values

# ======= Step 2: Standardize input & output =======
scaler_X = StandardScaler().fit(X)
scalers_y = [StandardScaler().fit(y[:, i].reshape(-1, 1)) for i in range(y.shape[1])]

# ======= Step 3: Load trained models =======
models = []
for i in range(y.shape[1]):
    model = XGBRegressor()
    try:
        model.load_model(f"M-XGB_{i+1}.json")
        models.append(model)
    except Exception as e:
        raise RuntimeError(f"Failed to load model M-XGB_{i+1}.json: {e}")

# ======= Step 4: Define output valid range for penalty =======
output_limits = [
    (18.8, 98.22),   # Yield (%)
    (4.1, 13.66),    # pH
    (0.3, 94.7),     # Ash (%)
    (3.29, 95.1),    # Volatile matter (%)
    (0, 6.86),       # Nitrogen (%)
    (0.7, 93.09),    # Fixed carbon (%)
    (3.8, 91.55),    # Carbon (%)
    (0, 3.79),       # H/C ratio
    (0, 1.29)        # O/C ratio
]

# ======= Step 5: Forward Prediction Function =======
def predict_properties(input_features):
    input_scaled = scaler_X.transform([input_features])
    outputs = []
    for model, scaler in zip(models, scalers_y):
        pred_scaled = model.predict(input_scaled)
        pred = scaler.inverse_transform(pred_scaled.reshape(-1, 1))[0][0]
        outputs.append(pred)
    return outputs

# ======= Step 6: Optimize the objective function with PSO (with penalties) =======
def objective_function(conditions, fixed_A_properties, weights):
    full_input = np.hstack((fixed_A_properties, conditions))
    input_scaled = scaler_X.transform([full_input])

    score = 0
    for i, (model, scaler, weight) in enumerate(zip(models, scalers_y, weights)):
        pred_scaled = model.predict(input_scaled)
        pred = scaler.inverse_transform(pred_scaled.reshape(-1, 1))[0][0]

        if pred < output_limits[i][0] or pred > output_limits[i][1]:
            return 1e6

        score += float(weight) * pred_scaled
    return -score

# ======= Step 7: Reverse Optimization with PSO =======
def optimize_conditions(fixed_A_properties, weights):  # ← weights is of the list type
    weights = [float(w) for w in weights]  # ✅ Explicitly convert to float type

    lb = [200, 1, 0]
    ub = [1000, 50, 240]

    opt_conditions, _ = pso(
        lambda c: objective_function(c, fixed_A_properties, weights),
        lb, ub, swarmsize=50, maxiter=50, omega=0.5, phip=2, phig=2
    )

    full_input = np.hstack((fixed_A_properties, opt_conditions))
    input_scaled = scaler_X.transform([full_input])

    outputs = []
    for model, scaler in zip(models, scalers_y):
        pred_scaled = model.predict(input_scaled)
        pred = scaler.inverse_transform(pred_scaled.reshape(-1, 1))[0][0]
        outputs.append(pred)

    return list(map(float, opt_conditions)), list(map(float, outputs))  # ✅ Explicitly return the float type

