import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
from pyswarm import pso

# ======= Step 1: Load training data =======
_data = pd.read_excel("确定6.0.xlsx")
X = _data.iloc[:, 0:10].values  # 10个输入变量
y = _data.iloc[:, 10:19].values  # 9个输出变量

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

# ======= Step 5: 正向预测函数（10维输入） =======
def predict_properties(input_features):
    """
    Predict biochar properties based on all 10 input features.
    input_features: [ash, vm, fc, c, h, o, n, temp, rate, time]
    """
    input_scaled = scaler_X.transform([input_features])
    outputs = []
    for model, scaler in zip(models, scalers_y):
        pred_scaled = model.predict(input_scaled)
        pred = scaler.inverse_transform(pred_scaled.reshape(-1, 1))[0][0]
        outputs.append(pred)
    return outputs

# ======= Step 6: PSO目标函数（带惩罚） =======
def objective_function(conditions, fixed_A_properties, weights):
    """
    PSO目标函数：输入待优化条件（3个）+ 固定的A属性（7个） + 权重列表（9个）
    输出为负加权得分（因为PSO是最小化问题）
    """
    full_input = np.hstack((fixed_A_properties, conditions))  # 补全为10维
    input_scaled = scaler_X.transform([full_input])

    score = 0
    for i, (model, scaler, weight) in enumerate(zip(models, scalers_y, weights)):
        pred_scaled = model.predict(input_scaled)
        pred = scaler.inverse_transform(pred_scaled.reshape(-1, 1))[0][0]

        # 超出预测范围就强烈惩罚
        if pred < output_limits[i][0] or pred > output_limits[i][1]:
            return 1e6

        score += weight * pred
    return -score  # PSO是最小化问题，我们要最大化目标函数

# ======= Step 7: PSO求最优工艺条件 =======
def optimize_conditions(fixed_A_properties, weights):
    """
    fixed_A_properties: list of 7 biomass properties
    weights: list of 9 output weights
    Return: 最优条件 [temp, rate, time], 对应预测的biochar属性
    """
    lb = [200, 1, 0]      # temp, rate, time 下界
    ub = [1000, 50, 240]  # 上界

    print("Running PSO optimization...")
    print("Input A properties:", fixed_A_properties)
    print("Target weights:", weights)

    opt_conditions, _ = pso(
        lambda c: objective_function(c, fixed_A_properties, weights),
        lb, ub, swarmsize=50, maxiter=50
    )

    # 得到预测输出
    full_input = np.hstack((fixed_A_properties, opt_conditions))
    input_scaled = scaler_X.transform([full_input])

    outputs = []
    for model, scaler in zip(models, scalers_y):
        pred_scaled = model.predict(input_scaled)
        pred = scaler.inverse_transform(pred_scaled.reshape(-1, 1))[0][0]
        outputs.append(pred)

    return opt_conditions, outputs
