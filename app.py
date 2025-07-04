import streamlit as st
import numpy as np
from optimizer import predict_properties, optimize_conditions

# 页面配置
st.set_page_config(page_title="Biochar Prediction & Optimization", layout="wide")

# 标题与说明
st.markdown("<h1>🌱 Biochar Property Prediction & Optimization</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='font-size:18px'>This platform predicts biochar properties from biomass and process parameters, "
    "and also optimizes experimental conditions to meet desired biochar performance.</p>", 
    unsafe_allow_html=True
)
st.markdown(
    "<span style='color:red; font-size:15px;'>*This reverse optimization process requires significant computation and may take 5 to 10 minutes. Please wait patiently.</span>", 
    unsafe_allow_html=True
)

# 输入生物质属性
st.subheader("🧪 Biomass A Properties")
biomass_labels = ["Ash (%)", "Volatile matter (%)", "Fixed carbon (%)", "Carbon (%)", 
                  "Hydrogen (%)", "Oxygen (%)", "Nitrogen (%)"]
biomass_inputs = []
cols = st.columns(7)
for i, label in enumerate(biomass_labels):
    val = cols[i].number_input(label, value=0.0, format="%.2f")
    biomass_inputs.append(val)

# 正向预测与逆向优化 左右并列
left_col, right_col = st.columns(2)

# ---------- 左侧：正向预测 ----------
with left_col:
    st.subheader("🔍 Forward Prediction")
    temp = st.number_input("Highest temperature (°C)", value=300.0, format="%.2f")
    rate = st.number_input("Heating rate (°C/min)", value=10.0, format="%.2f")
    time = st.number_input("Residence time (min)", value=30.0, format="%.2f")

    if st.button("Predict"):
        prediction_inputs = biomass_inputs + [temp, rate, time]
        pred_outputs = predict_properties(prediction_inputs)

        st.success("✅ Prediction completed!")
        st.subheader("📊 Predicted Biochar Properties")
        pred_props = [
            "Yield (%)", "pH", "Ash (%)", "Volatile matter (%)", "Nitrogen (%)",
            "Fixed carbon (%)", "Carbon (%)", "H/C ratio", "O/C ratio"
        ]
        pred_cols = st.columns(3)
        for i, (k, v) in enumerate(zip(pred_props, pred_outputs)):
            pred_cols[i % 3].metric(k, f"{v:.2f}")

# ---------- 右侧：逆向优化 ----------
with right_col:
    st.subheader("🎯 Reverse Optimization for Biochar Properties")
    st.markdown(
        "<p style='font-size:16px'>Enter biomass properties and assign weights to biochar properties to "
        "design the best experiment condition for preparing your ideal biochar.</p>",
        unsafe_allow_html=True
    )

    # 权重输入
    weights = {}
    opt_props = [
        "Yield (%)", "pH", "Ash (%)", "Volatile matter (%)", "Nitrogen (%)",
        "Fixed carbon (%)", "Carbon (%)", "H/C ratio", "O/C ratio"
    ]
    opt_cols = st.columns(3)
    for i, prop in enumerate(opt_props):
        weights[prop] = opt_cols[i % 3].number_input(f"{prop} weight", value=1, step=1)

    if st.button("Optimize"):
        opt_conditions, opt_outputs = optimize_conditions(biomass_inputs, list(weights.values()))

        st.success("✅ Optimization completed!")
        st.subheader("🔧 Optimized Experimental Conditions")
        opt_labels = ["Highest temperature (°C)", "Heating rate (°C/min)", "Residence time (min)"]
        opt_result_cols = st.columns(3)
        for i, val in enumerate(opt_conditions):
            opt_result_cols[i].metric(opt_labels[i], f"{val:.2f}")

        st.subheader("🎯 Ideal Biochar Properties")
        opt_output_cols = st.columns(3)
        for i, (key, value) in enumerate(zip(opt_props, opt_outputs)):
            opt_output_cols[i % 3].metric(key, f"{value:.2f}")
