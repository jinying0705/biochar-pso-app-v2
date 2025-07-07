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

# ======= Step 4: Define output valid range =======
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

# ======= Step 5: 正向预测函数 =======
def predict_properties(input_features):
    input_scaled = scaler_X.transform([input_features])
    outputs = []
    for model, scaler in zip(models, scalers_y):
        pred_scaled = model.predict(input_scaled)
        pred = scaler.inverse_transform(pred_scaled.reshape(-1, 1))[0][0]
        outputs.append(float(pred))
    return outputs

# ======= Step 6: PSO目标函数 =======
def objective_function(conditions, fixed_A_properties, weights):
    full_input = np.hstack((fixed_A_properties, conditions))
    input_scaled = scaler_X.transform([full_input])

    score = 0
    for i, (model, scaler, weight) in enumerate(zip(models, scalers_y, weights)):
        pred_scaled = model.predict(input_scaled)
        pred = scaler.inverse_transform(pred_scaled.reshape(-1, 1))[0][0]

        if pred < output_limits[i][0] or pred > output_limits[i][1]:
            return 1e6

        score += float(weight) * float(pred)
    return -score

# ======= Step 7: 逆向优化函数，返回格式化 HTML =======
def optimize_conditions(fixed_A_properties, weight_dict):
    weights = [float(w) for w in weight_dict.values()]

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
        outputs.append(float(pred))

    # ======= 格式化 HTML 输出 =======
    output_labels = [
        "Yield (%)", "pH", "Ash (%)", "Volatile matter (%)",
        "Nitrogen (%)", "Fixed carbon (%)", "Carbon (%)",
        "H/C ratio", "O/C ratio"
    ]

    styled_html = ""

    # Optimal Conditions
    styled_html += "<h4>🧪 Optimal Conditions</h4>"
    condition_labels = ["Highest temperature (°C)", "Heating rate (°C/min)", "Residence time (min)"]
    for label, val in zip(condition_labels, opt_conditions):
        styled_html += f"""
        <div style="padding:8px 14px; margin:5px 0; background-color:#eef9ff;
                    border-left: 5px solid #2196F3; font-size:15px;">
            <b>{label}</b>: {float(val):.2f}
        </div>
        """

    # Predicted Biochar Properties
    styled_html += "<h4>🌟 Predicted Biochar Properties</h4>"
    for label, val in zip(output_labels, outputs):
        styled_html += f"""
        <div style="padding:8px 14px; margin:5px 0; background-color:#f9f9f9;
                    border-left: 5px solid #4CAF50; font-size:15px;">
            <b>{label}</b>: {float(val):.2f}
        </div>
        """

    return styled_html
