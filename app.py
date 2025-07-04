import streamlit as st
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import StandardScaler
from optimizer import optimize_conditions, predict_properties

st.set_page_config(page_title="Biochar Prediction & Optimization", layout="wide")

# ----------------------------
# Load Data, Scalers, Models
# ----------------------------
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

data, scaler_X, scalers_y = load_data_and_scalers()
models = load_models()

# ----------------------------
# 页面标题与说明
# ----------------------------
st.markdown("<h1 style='text-align: center;'>🌱 Biochar Property Prediction & Optimization</h1>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align: center; font-size: 16px;'>"
    "This platform predicts biochar properties from biomass and process parameters, and also optimizes experimental conditions to meet desired biochar performance."
    "</div><br>", unsafe_allow_html=True)

# ----------------------------
# 左右两列结构
# ----------------------------
left_col, right_col = st.columns(2)

# ----------------------------
# 左侧：正向预测模块
# ----------------------------
with left_col:
    st.subheader("🔍 Forward Prediction")

    input_labels = [
        "Ash (%)", "Volatile matter (%)", "Fixed carbon (%)", "Carbon (%)",
        "Hydrogen (%)", "Oxygen (%)", "Nitrogen (%)",
        "Highest temperature (℃)", "Heating rate (℃/min)", "Residence time (min)"
    ]
    input_values = []
    for label in input_labels:
        val = st.number_input(label, value=0.0, format="%.2f")
        input_values.append(val)

    if st.button("Predict"):
        with st.spinner("Predicting..."):
            pred_results = predict_properties(input_values)
            st.success("✅ Prediction completed!")

            output_labels = [
                "Yield (%)", "pH", "Ash (%)", "Volatile matter (%)", "Nitrogen (%)",
                "Fixed carbon (%)", "Carbon (%)", "H/C ratio", "O/C ratio"
            ]
            st.markdown("### 🔍 Predicted Biochar Properties")
            cols = st.columns(3)
            for i, val in enumerate(pred_results):
                with cols[i % 3]:
                    st.markdown(f"<div style='padding:10px; border:1px solid #ddd; border-radius:10px; background-color:#f9f9f9;'><b>{output_labels[i]}</b><br><span style='font-size:20px;'>{val:.2f}</span></div>", unsafe_allow_html=True)

# ----------------------------
# 右侧：逆向优化模块
# ----------------------------
with right_col:
    st.subheader("🎯 Reverse Optimization")
    st.markdown("*This reverse optimization process requires significant computation and may take 5 to 10 minutes. Please wait patiently.*", unsafe_allow_html=True)

    st.markdown("#### ✏️ Enter Biomass Properties")
    biomass_labels = [
        "Ash (%)", "Volatile matter (%)", "Fixed carbon (%)", "Carbon (%)",
        "Hydrogen (%)", "Oxygen (%)", "Nitrogen (%)"
    ]
    fixed_props = []
    for label in biomass_labels:
        val = st.number_input(label, key=f"opt_{label}", value=0.0, format="%.2f")
        fixed_props.append(val)

    st.markdown("#### ⚖️ Assign Weights to Biochar Properties")
    opt_labels = [
        "Yield (%)", "pH", "Ash (%)", "Volatile matter (%)", "Nitrogen (%)",
        "Fixed carbon (%)", "Carbon (%)", "H/C ratio", "O/C ratio"
    ]
    weights = []
    for label in opt_labels:
        val = st.number_input(f"{label} weight", min_value=0, value=1, step=1, format="%d")
        weights.append(val)

    if st.button("Optimize"):
        with st.spinner("Running PSO optimization..."):
            opt_conditions, pred_outputs = optimize_conditions(fixed_props, weights)
            st.success("✅ Optimization completed!")

            st.markdown("### 🔧 Optimized Experimental Conditions")
            condition_labels = ["Highest temperature (℃)", "Heating rate (℃/min)", "Residence time (min)"]
            cols1 = st.columns(3)
            for i, val in enumerate(opt_conditions):
                cols1[i].markdown(f"<div style='padding:10px; border:1px solid #ddd; border-radius:10px; background-color:#f4f4f4;'><b>{condition_labels[i]}</b><br><span style='font-size:20px;'>{val:.2f}</span></div>", unsafe_allow_html=True)

            st.markdown("### 🎯 Ideal Biochar Properties")
            cols2 = st.columns(3)
            for i, val in enumerate(pred_outputs):
                cols2[i % 3].markdown(f"<div style='padding:10px; border:1px solid #ddd; border-radius:10px; background-color:#f9f9f9;'><b>{opt_labels[i]}</b><br><span style='font-size:20px;'>{val:.2f}</span></div>", unsafe_allow_html=True)
