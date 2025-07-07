import streamlit as st
import numpy as np
from optimizer import optimize_conditions, predict_properties

# ---------- 页面配置 ----------
st.set_page_config(page_title="Reverse Optimization for Biochar Properties", layout="wide")

# ---------- 页面主标题 ----------
st.markdown("<h1 style='font-size:28px;'>The multi-task learning model used to predict the properties and customize the design of biochar</h1>", unsafe_allow_html=True)

# ---------- 输入部分 ----------
st.subheader("🧪 Biomass Properties & Pyrolysis Conditions")

biomass_labels = [
    "Ash (%)", "Volatile matter (%)", "Fixed carbon (%)", "Carbon (%)",
    "Hydrogen (%)", "Oxygen (%)", "Nitrogen (%)"
]
biomass_inputs = []
cols = st.columns(len(biomass_labels))
for i, label in enumerate(biomass_labels):
    biomass_inputs.append(cols[i].number_input(label, value=0.0, format="%.2f", key=f"bio_{i}"))

# ---------- 左右并排：预测 与 反向优化 ----------
left_col, right_col = st.columns(2)

# ---------- 🎯 Forward Prediction ----------
with left_col:
    st.subheader("🎯 Forward Prediction")
    st.markdown(
        "<p style='font-size:16px;'>Please enter 10 biomass-related properties above and click Predict to view the predicted biochar characteristics.</p>",
        unsafe_allow_html=True
    )

    temp = st.number_input("Highest temperature (°C)", value=300.0, format="%.2f", key="temp")
    rate = st.number_input("Heating rate (°C/min)", value=10.0, format="%.2f", key="rate")
    time = st.number_input("Residence time (min)", value=30.0, format="%.2f", key="time")

    if st.button("Predict"):
        input_features = biomass_inputs + [temp, rate, time]
        predictions = predict_properties(input_features)

        st.success("✅ Prediction completed!")
        st.subheader("📊 Predicted Biochar Properties")
        pred_props = [
            "Yield (%)", "pH", "Ash (%)", "Volatile matter (%)", "Nitrogen (%)",
            "Fixed carbon (%)", "Carbon (%)", "H/C ratio", "O/C ratio"
        ]
        pred_cols = st.columns(3)
        for i, (key, val) in enumerate(zip(pred_props, predictions)):
            pred_cols[i % 3].metric(key, f"{val:.2f}")

# ---------- 🔍 Reverse Optimization ----------
with right_col:
    st.subheader("🔍 Reverse Optimization")
    st.markdown(
        "<p style='font-size:16px;'>Enter the biomass properties above and assign weights to the biochar properties below to design optimal experimental conditions for preparing your ideal biochar.</p>",
        unsafe_allow_html=True
    )

    weights = {}
    opt_props = [
        "Yield (%)", "pH", "Ash (%)", "Volatile matter (%)", "Nitrogen (%)",
        "Fixed carbon (%)", "Carbon (%)", "H/C ratio", "O/C ratio"
    ]
    weight_cols = st.columns(3)
    for i, prop in enumerate(opt_props):
        weights[prop] = weight_cols[i % 3].number_input(f"{prop} weight", value=1, step=1, key=f"w_{i}")

    if st.button("Optimize"):
        opt_conditions, opt_outputs = optimize_conditions(biomass_inputs, list(weights.values()))

        st.success("✅ Optimization completed!")
        st.subheader("🔧 Optimal Experimental Conditions")
        cond_labels = ["Highest temperature (°C)", "Heating rate (°C/min)", "Residence time (min)"]
        cond_cols = st.columns(3)
        for i, val in enumerate(opt_conditions):
            cond_cols[i].metric(cond_labels[i], f"{val:.2f}")

        st.subheader("📈 Optimal Biochar Properties")
        opt_out_cols = st.columns(3)
        for i, (key, val) in enumerate(zip(opt_props, opt_outputs)):
            opt_out_cols[i % 3].metric(key, f"{val:.2f}")

# ---------- 底部注意说明 ----------
st.markdown(
    "<p style='font-size:14px; color:gray;'><b>Note:</b> This reverse optimization process requires significant computation and may take 5 to 10 minutes. Please wait patiently.</p>",
    unsafe_allow_html=True
)
