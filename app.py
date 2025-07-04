import streamlit as st
import numpy as np
from optimizer import optimize_conditions, predict_properties

# ---------- 页面设置 ----------
st.set_page_config(page_title="Biochar Prediction & Optimization", layout="wide")

# ---------- 页面标题和说明 ----------
st.markdown(
    """
    <h1 style='font-size:36px; margin-bottom:10px;'>🌱 Biochar Property Prediction & Optimization</h1>
    <p style='font-size:18px;'>
    This platform predicts biochar properties from biomass and process conditions, and optimizes experimental parameters to achieve ideal biochar performance.
    </p>
    <p style='font-size:16px; color:gray;'>
    <strong>Note:</strong> Optimization may take 5–10 minutes depending on computational load.
    </p>
    """,
    unsafe_allow_html=True
)

# ---------- 第一部分：输入 A 的性质 ----------
st.subheader("🧪 Biomass A Properties")
biomass_labels = ["Ash (%)", "Volatile matter (%)", "Fixed carbon (%)", "Carbon (%)",
                  "Hydrogen (%)", "Oxygen (%)", "Nitrogen (%)"]
biomass_inputs = []
cols = st.columns(len(biomass_labels))
for i, label in enumerate(biomass_labels):
    val = cols[i].number_input(label, value=0.0, format="%.2f")
    biomass_inputs.append(val)

# ---------- 第二部分：预测与优化并排 ----------
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
        output_props = [
            "Yield (%)", "pH", "Ash (%)", "Volatile matter (%)", "Nitrogen (%)",
            "Fixed carbon (%)", "Carbon (%)", "H/C ratio", "O/C ratio"
        ]
        cols_pred = st.columns(3)
        for i, (label, value) in enumerate(zip(output_props, pred_outputs)):
            cols_pred[i % 3].metric(label, f"{value:.2f}")

# ---------- 右侧：逆向优化 ----------
with right_col:
    st.subheader("🎯 Reverse Optimization")
    output_props = [
        "Yield (%)", "pH", "Ash (%)", "Volatile matter (%)", "Nitrogen (%)",
        "Fixed carbon (%)", "Carbon (%)", "H/C ratio", "O/C ratio"
    ]
    weights = []
    cols_opt = st.columns(3)
    for i, label in enumerate(output_props):
        weight = cols_opt[i % 3].number_input(f"{label} weight", min_value=0, max_value=10, value=1)
        weights.append(weight)

    if st.button("Optimize"):
        st.warning("⏳ Running optimization... Please wait.")
        opt_conditions, opt_outputs = optimize_conditions(biomass_inputs, weights)

        st.success("✅ Optimization completed!")
        st.subheader("🔧 Optimal Experimental Conditions")
        opt_labels = ["Highest temperature (°C)", "Heating rate (°C/min)", "Residence time (min)"]
        opt_cols = st.columns(3)
        for i, val in enumerate(opt_conditions):
            opt_cols[i].metric(opt_labels[i], f"{val:.2f}")

        st.subheader("📈 Predicted Biochar Properties from Optimal Conditions")
        opt_out_cols = st.columns(3)
        for i, (label, value) in enumerate(zip(output_props, opt_outputs)):
            opt_out_cols[i % 3].metric(label, f"{value:.2f}")

