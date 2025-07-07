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

# ---------- 输入 A 物质的属性 ----------
st.subheader("🧪 Biomass A Properties")
input_cols = st.columns(3)
ash = input_cols[0].number_input("Ash (%)", value=0.0, format="%.2f")
volatile = input_cols[1].number_input("Volatile matter (%)", value=0.0, format="%.2f")
fixed_c = input_cols[2].number_input("Fixed carbon (%)", value=0.0, format="%.2f")

input_cols2 = st.columns(3)
carbon = input_cols2[0].number_input("Carbon (%)", value=0.0, format="%.2f")
hydrogen = input_cols2[1].number_input("Hydrogen (%)", value=0.0, format="%.2f")
oxygen = input_cols2[2].number_input("Oxygen (%)", value=0.0, format="%.2f")

input_cols3 = st.columns(3)
nitrogen = input_cols3[0].number_input("Nitrogen (%)", value=0.0, format="%.2f")

biomass_inputs = [ash, volatile, fixed_c, carbon, hydrogen, oxygen, nitrogen]

# ---------- 左右列布局 ----------
left_col, right_col = st.columns(2)

# ---------- 正向预测 ----------
with left_col:
    st.subheader("🔍 Forward Prediction")
    fwd_cols = st.columns(3)
    temp = fwd_cols[0].number_input("Highest temperature (°C)", value=300.0, format="%.2f")
    rate = fwd_cols[1].number_input("Heating rate (°C/min)", value=10.0, format="%.2f")
    time = fwd_cols[2].number_input("Residence time (min)", value=30.0, format="%.2f")

    if st.button("Predict"):
        prediction_inputs = biomass_inputs + [temp, rate, time]
        pred_outputs = predict_properties(prediction_inputs)
        st.success("✅ Prediction completed!")

        st.subheader("📊 Ideal Biochar Properties")
        pred_props = [
            "Yield (%)", "pH", "Ash (%)", "Volatile matter (%)", "Nitrogen (%)",
            "Fixed carbon (%)", "Carbon (%)", "H/C ratio", "O/C ratio"
        ]
        pred_cols = st.columns(3)
        for i, (key, value) in enumerate(zip(pred_props, pred_outputs)):
            pred_cols[i % 3].metric(key, f"{value:.2f}")

# ---------- 逆向优化 ----------
with right_col:
    st.subheader("🎯 Reverse Optimization")
    st.markdown("Enter biomass features and assign weights to output properties to search for the best experiment condition for preparing your ideal biochar.")

    weight_cols1 = st.columns(3)
    yield_w = weight_cols1[0].number_input("Yield (%) weight", value=1)
    pH_w = weight_cols1[1].number_input("pH weight", value=1)
    ash_w = weight_cols1[2].number_input("Ash (%) weight", value=1)

    weight_cols2 = st.columns(3)
    vm_w = weight_cols2[0].number_input("Volatile matter (%) weight", value=1)
    nitro_w = weight_cols2[1].number_input("Nitrogen (%) weight", value=1)
    fc_w = weight_cols2[2].number_input("Fixed carbon (%) weight", value=1)

    weight_cols3 = st.columns(3)
    carbon_w = weight_cols3[0].number_input("Carbon (%) weight", value=1)
    hc_w = weight_cols3[1].number_input("H/C ratio weight", value=1)
    oc_w = weight_cols3[2].number_input("O/C ratio weight", value=1)

    weights = [yield_w, pH_w, ash_w, vm_w, nitro_w, fc_w, carbon_w, hc_w, oc_w]

    if st.button("Optimize"):
        with st.spinner("Running reverse optimization..."):
            opt_conditions, opt_outputs = optimize_conditions(biomass_inputs, weights)

        st.success("✅ Optimization completed!")
        st.subheader("🛠️ Optimal Experimental Conditions")
        param_cols = st.columns(3)
        param_cols[0].metric("Highest temperature (°C)", f"{opt_conditions[0]:.2f}")
        param_cols[1].metric("Heating rate (°C/min)", f"{opt_conditions[1]:.2f}")
        param_cols[2].metric("Residence time (min)", f"{opt_conditions[2]:.2f}")

        st.subheader("📊 Predicted Biochar Properties")
        prop_cols = st.columns(3)
        prop_labels = [
            "Yield (%)", "pH", "Ash (%)", "Volatile matter (%)", "Nitrogen (%)",
            "Fixed carbon (%)", "Carbon (%)", "H/C ratio", "O/C ratio"
        ]
        for i, (label, value) in enumerate(zip(prop_labels, opt_outputs)):
            prop_cols[i % 3].metric(label, f"{value:.2f}")
