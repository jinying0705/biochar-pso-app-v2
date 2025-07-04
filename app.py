import streamlit as st
import numpy as np
from optimizer import predict_properties, optimize_conditions

st.set_page_config(layout="wide")

st.markdown("## 🌱 Reverse Optimization for Biochar Properties")
st.markdown("Enter biomass properties and assign weights to biochar properties to design the best experiment condition for preparing your ideal biochar.")
st.markdown("<span style='color:red;'>*This reverse optimization process requires significant computation and may take 5 to 10 minutes. Please wait patiently.*</span>", unsafe_allow_html=True)
st.markdown("---")

# 输入区域（左）
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("🧪 Input Biomass Properties")
    ash = st.number_input("Ash (%)", value=0.00, format="%.2f")
    vm = st.number_input("Volatile matter (%)", value=0.00, format="%.2f")
    fc = st.number_input("Fixed carbon (%)", value=0.00, format="%.2f")
    c = st.number_input("Carbon (%)", value=0.00, format="%.2f")
    h = st.number_input("Hydrogen (%)", value=0.00, format="%.2f")
    o = st.number_input("Oxygen (%)", value=0.00, format="%.2f")
    n = st.number_input("Nitrogen (%)", value=0.00, format="%.2f")
    temp = st.number_input("Highest temperature (°C)", value=300.0, format="%.2f")
    rate = st.number_input("Heating rate (°C/min)", value=10.0, format="%.2f")
    time = st.number_input("Residence time (min)", value=30.0, format="%.2f")
    if st.button("Predict"):
        A_input = [ash, vm, fc, c, h, o, n, temp, rate, time]
        pred_results = predict_properties(A_input)
        st.success("✅ Prediction completed!")
        st.subheader("🔬 Predicted Biochar Properties")
        cols = st.columns(3)
        labels = ["Yield (%)", "pH", "Ash (%)", "Volatile matter (%)", "Nitrogen (%)",
                  "Fixed carbon (%)", "Carbon (%)", "H/C ratio", "O/C ratio"]
        for i, val in enumerate(pred_results):
            cols[i % 3].metric(labels[i], f"{val:.2f}")

# 权重区域（右）
with right_col:
    st.subheader("🎯 Reverse Optimization for Biochar Properties")
    st.write("Enter biomass properties and assign weights to biochar properties to design the best experiment condition for preparing your ideal biochar.")

    weights_labels = ["Yield (%) weight", "pH weight", "Ash (%) weight",
                      "Volatile matter (%) weight", "Nitrogen (%) weight",
                      "Fixed carbon (%) weight", "Carbon (%) weight",
                      "H/C ratio weight", "O/C ratio weight"]
    
    wcols = st.columns(3)
    weights = []
    for i, label in enumerate(weights_labels):
        w = wcols[i % 3].number_input(label, value=1.0, format="%.2f", key=f"w{i}")
        weights.append(w)

    if st.button("Optimize"):
        A_input = [ash, vm, fc, c, h, o, n]
        opt_conditions, pred_results = optimize_conditions(A_input, weights)
        st.success("✅ Optimization completed!")

        st.subheader("🛠️ Optimized Experimental Conditions")
        c1, c2, c3 = st.columns(3)
        c1.metric("Highest temperature (°C)", f"{opt_conditions[0]:.2f}")
        c2.metric("Heating rate (°C/min)", f"{opt_conditions[1]:.2f}")
        c3.metric("Residence time (min)", f"{opt_conditions[2]:.2f}")

        st.subheader("💡 Ideal Biochar Properties")
        rcols = st.columns(3)
        labels = ["Yield (%)", "pH", "Ash (%)", "Volatile matter (%)", "Nitrogen (%)",
                  "Fixed carbon (%)", "Carbon (%)", "H/C ratio", "O/C ratio"]
        for i, val in enumerate(pred_results):
            rcols[i % 3].metric(labels[i], f"{val:.2f}")
