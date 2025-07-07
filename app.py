import streamlit as st
import numpy as np
from optimizer import predict_properties, optimize_conditions

st.set_page_config(layout="wide")

st.title("🌱 Reverse Optimization for Biochar Properties")
st.markdown("Enter biomass properties and assign weights to biochar properties to design the best experiment condition for preparing your ideal biochar.")
st.markdown(
    "*This reverse optimization process requires significant computation and may take 5 to 10 minutes. Please wait patiently.*",
    unsafe_allow_html=True,
)

# ---------------- 左右两列 ----------------
left_col, right_col = st.columns(2)

# ---------------- 左边：正向预测模块 ----------------
with left_col:
    st.subheader("🔍 Forward Prediction")
    st.markdown("Enter all biomass features and processing parameters to predict biochar properties.")

    fwd_inputs = []

    fwd_rows = [st.columns(3) for _ in range(5)]
    labels = [
        "Ash (%)", "Volatile matter (%)", "Fixed carbon (%)",
        "Carbon (%)", "Hydrogen (%)", "Oxygen (%)",
        "Nitrogen (%)", "Silicon (%)", "Cellulose (%)",
        "Highest temperature (°C)", "Heating rate (°C/min)", "Residence time (min)"
    ]
    defaults = [0.0] * 7 + [0.0, 0.0] + [300.0, 10.0, 30.0]

    for i, (label, default) in enumerate(zip(labels, defaults)):
        col = fwd_rows[i // 3][i % 3]
        value = col.number_input(label, value=default, format="%.2f")
        fwd_inputs.append(value)

    if st.button("Predict"):
        outputs = predict_properties(fwd_inputs)
        st.success("✅ Prediction completed!")
        st.subheader("📊 Ideal Biochar Properties")
        pred_labels = [
            "Yield (%)", "pH", "Ash (%)", "Volatile matter (%)", "Nitrogen (%)",
            "Fixed carbon (%)", "Carbon (%)", "H/C ratio", "O/C ratio"
        ]
        pred_cols = st.columns(3)
        for i, (k, v) in enumerate(zip(pred_labels, outputs)):
            pred_cols[i % 3].metric(k, f"{v:.2f}")

# ---------------- 右边：逆向优化模块 ----------------
with right_col:
    st.subheader("🎯 Reverse Optimization")
    st.markdown("Assign weights to biochar properties to guide the optimization toward your ideal material.")

    weight_rows = [st.columns(3) for _ in range(3)]
    weight_labels = [
        "Yield (%) weight", "pH weight", "Ash (%) weight",
        "Volatile matter (%) weight", "Nitrogen (%) weight", "Fixed carbon (%) weight",
        "Carbon (%) weight", "H/C ratio weight", "O/C ratio weight"
    ]
    weights = []

    for i, label in enumerate(weight_labels):
        col = weight_rows[i // 3][i % 3]
        value = col.number_input(label, value=1.0)
        weights.append(value)

    if st.button("Optimize"):
        with st.spinner("Running optimization..."):
            biomass_inputs = fwd_inputs[:10]  # 前10个是生物质属性
            opt_params, opt_outputs = optimize_conditions(biomass_inputs, weights)

        st.success("✅ Optimization completed!")
        st.subheader("🛠️ Optimized Experimental Conditions")
        param_cols = st.columns(3)
        param_cols[0].metric("Highest temperature (°C)", f"{opt_params[0]:.2f}")
        param_cols[1].metric("Heating rate (°C/min)", f"{opt_params[1]:.2f}")
        param_cols[2].metric("Residence time (min)", f"{opt_params[2]:.2f}")

        st.subheader("📊 Predicted Biochar Properties")
        prop_cols = st.columns(3)
        for i, (k, v) in enumerate(zip(weight_labels, opt_outputs)):
            prop_cols[i % 3].metric(k.replace(" weight", ""), f"{v:.2f}")
