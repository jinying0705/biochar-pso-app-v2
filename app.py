import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import StandardScaler
from pyswarm import pso

# 页面设置
st.set_page_config(page_title="Biochar Property Prediction & Optimization", layout="wide")

# 标题与说明
st.title("🌱 Biochar Property Prediction & Optimization")
st.markdown("""
This platform predicts biochar properties from biomass and process conditions,  
and can also optimize process parameters to achieve ideal biochar performance.  

**Note:** Optimization may take 5–10 minutes depending on computational load.
""")

# 载入数据和模型
@st.cache_data
def load_data_and_scalers():
    data = pd.read_excel("确定6.0.xlsx")
    X = data.iloc[:, 0:10].values
    y = data.iloc[:, 10:19].values
    scaler_X = StandardScaler().fit(X)
    scalers_y = [StandardScaler().fit(y[:, i].reshape(-1, 1)) for i in range(y.shape[1])]
    return data, scaler_X, scalers_y

@st.cache_resource
def load_models():
    models = []
    for i in range(9):
        model = xgb.XGBRegressor()
        model.load_model(f"M-XGB_{i+1}.json")
        models.append(model)
    return models

# 预测函数
def predict_properties(input_values, scaler_X, scalers_y, models):
    input_scaled = scaler_X.transform([input_values])
    preds = []
    for model, scaler in zip(models, scalers_y):
        pred_scaled = model.predict(input_scaled)
        pred = scaler.inverse_transform(pred_scaled.reshape(-1, 1))[0][0]
        preds.append(pred)
    return preds

# 优化函数
output_limits = [
    (18.8, 98.22), (4.1, 13.66), (0.3, 94.7), (3.29, 95.1), (0, 6.86),
    (0.7, 93.09), (3.8, 91.55), (0, 3.79), (0, 1.29)
]

def objective_function(conditions, fixed_A, weights, scaler_X, scalers_y, models):
    full_input = np.hstack((fixed_A, conditions))
    input_scaled = scaler_X.transform([full_input])
    total = 0
    for i, (model, scaler, weight) in enumerate(zip(models, scalers_y, weights)):
        pred_scaled = model.predict(input_scaled)
        pred = scaler.inverse_transform(pred_scaled.reshape(-1, 1))[0][0]
        if pred < output_limits[i][0] or pred > output_limits[i][1]:
            return 1e6
        total += weight * pred
    return -total

def optimize_conditions(fixed_A, weights, scaler_X, scalers_y, models):
    lb = [200, 1, 0]
    ub = [1000, 50, 240]
    opt_conditions, _ = pso(
        lambda x: objective_function(x, fixed_A, weights, scaler_X, scalers_y, models),
        lb, ub, swarmsize=30, maxiter=30
    )
    full_input = np.hstack((fixed_A, opt_conditions))
    input_scaled = scaler_X.transform([full_input])
    preds = []
    for model, scaler in zip(models, scalers_y):
        pred_scaled = model.predict(input_scaled)
        pred = scaler.inverse_transform(pred_scaled.reshape(-1, 1))[0][0]
        preds.append(pred)
    return opt_conditions, preds

# 数据与模型加载
data, scaler_X, scalers_y = load_data_and_scalers()
models = load_models()

# 属性标签
input_labels = ["Ash (%)", "Volatile matter (%)", "Fixed carbon (%)", "Carbon (%)", "Hydrogen (%)", "Oxygen (%)", "Nitrogen (%)"]
process_labels = ["Highest temperature (℃)", "Heating rate (℃/min)", "Residence time (min)"]
output_labels = [
    "Yield (%)", "pH", "Ash (%)", "Volatile matter (%)", "Nitrogen (%)",
    "Fixed carbon (%)", "Carbon (%)", "Hydrogen-carbon ratio", "Oxygen-carbon ratio"
]

# 输入物质 A 的属性
st.markdown("### 🔬 Biomass A Properties")
cols = st.columns(len(input_labels))
biomass_inputs = []
for i, label in enumerate(input_labels):
    val = cols[i].number_input(label, value=float(data.iloc[0, i]), format="%.2f")
    biomass_inputs.append(val)

# 左右布局
left, right = st.columns(2)

with left:
    st.markdown("### 🔧 Forward Prediction")
    process_inputs = []
    for label in process_labels:
        val = st.number_input(label, value=300.0, format="%.2f")
        process_inputs.append(val)

    if st.button("Predict"):
        input_all = biomass_inputs + process_inputs
        pred_outputs = predict_properties(input_all, scaler_X, scalers_y, models)

        st.success("✅ Prediction completed!")
        st.markdown("### 🧾 Predicted Biochar Properties")
        pred_cols = st.columns(3)
        for i, val in enumerate(pred_outputs):
            pred_cols[i % 3].metric(output_labels[i], f"{val:.2f}")

with right:
    st.markdown("### 🎯 Reverse Optimization")
    weights = []
    weight_cols = st.columns(3)
    for i, label in enumerate(output_labels):
        w = weight_cols[i % 3].number_input(f"{label} weight", value=1)
        weights.append(w)

    if st.button("Optimize"):
        opt_conditions, opt_outputs = optimize_conditions(biomass_inputs, weights, scaler_X, scalers_y, models)

        st.success("✅ Optimization completed!")
        st.markdown("### ⚙️ Optimal Experimental Conditions")
        opt_cols = st.columns(3)
        for i, val in enumerate(opt_conditions):
            opt_cols[i].metric(process_labels[i], f"{val:.2f}")

        st.markdown("### 📈 Predicted Biochar Properties under Optimal Conditions")
        opt_output_cols = st.columns(3)
        for i, val in enumerate(opt_outputs):
            opt_output_cols[i % 3].metric(output_labels[i], f"{val:.2f}")
