import streamlit as st
import numpy as np
from optimizer import predict_properties, optimize_conditions

st.set_page_config(layout="wide")

st.markdown("## 🌱 The multi-task learning model used to predict the properties and customize the design of biochar")

col_input = st.columns(7)
ash = col_input[0].number_input("Ash (%)", min_value=0.0, value=0.0, step=0.01)
vol = col_input[1].number_input("Volatile matter (%)", min_value=0.0, value=0.0, step=0.01)
fix = col_input[2].number_input("Fixed carbon (%)", min_value=0.0, value=0.0, step=0.01)
c = col_input[3].number_input("Carbon (%)", min_value=0.0, value=0.0, step=0.01)
h = col_input[4].number_input("Hydrogen (%)", min_value=0.0, value=0.0, step=0.01)
o = col_input[5].number_input("Oxygen (%)", min_value=0.0, value=0.0, step=0.01)
n = col_input[6].number_input("Nitrogen (%)", min_value=0.0, value=0.0, step=0.01)

st.markdown("### 🔬 Biomass Properties & Pyrolysis Conditions")

left, right = st.columns(2)

with left:
    st.markdown("### 🎯 Forward Prediction")
    st.write("Please enter 10 biomass-related properties above and click Predict to view the predicted biochar characteristics.")
    temp = st.number_input("Highest temperature (°C)", min_value=0.0, value=300.0, step=1.0)
    rate = st.number_input("Heating rate (°C/min)", min_value=0.0, value=10.0, step=0.1)
    time = st.number_input("Residence time (min)", min_value=0.0, value=30.0, step=1.0)

    if st.button("Predict"):
        fwd_inputs = [ash, vol, fix, c, h, o, n, temp, rate, time]
        try:
            outputs = predict_properties(fwd_inputs)
            st.subheader("🔍 Predicted Biochar Properties")
            for name, value in zip([
                "Yield (%)", "pH", "Ash (%)", "Volatile matter (%)", "Nitrogen (%)",
                "Fixed carbon (%)", "Carbon (%)", "H/C ratio", "O/C ratio"
            ], outputs):
                st.write(f"**{name}:** {value:.2f}")
        except Exception as e:
            st.error(f"Prediction failed: {e}")

with right:
    st.markdown("### 🔎 Reverse Optimization")
    st.write("Enter the biomass properties above and assign weights to the biochar properties below to design optimal experimental conditions for preparing your ideal biochar.")

    weight_names = [
        "Yield (%) weight", "pH weight", "Ash (%) weight",
        "Volatile matter (%) weight", "Nitrogen (%) weight",
        "Fixed carbon (%) weight", "Carbon (%) weight",
        "H/C ratio weight", "O/C ratio weight"
    ]
    weights = []
    weight_cols = st.columns(3)
    for i, name in enumerate(weight_names):
        with weight_cols[i % 3]:
            w = st.number_input(name, min_value=0.0, value=1.0, step=0.1)
            weights.append(w)

    if st.button("Optimize"):
        try:
            fixed_props = [ash, vol, fix, c, h, o, n]
            opt_conditions, opt_outputs = optimize_conditions(fixed_props, weights)
            st.subheader("⚙️ Optimal Experimental Conditions")
            st.write(f"**Highest temperature (°C):** {opt_conditions[0]:.2f}")
            st.write(f"**Heating rate (°C/min):** {opt_conditions[1]:.2f}")
            st.write(f"**Residence time (min):** {opt_conditions[2]:.2f}")

            st.subheader("🧪 Predicted Biochar Properties")
            for name, value in zip([
                "Yield (%)", "pH", "Ash (%)", "Volatile matter (%)", "Nitrogen (%)",
                "Fixed carbon (%)", "Carbon (%)", "H/C ratio", "O/C ratio"
            ], opt_outputs):
                st.write(f"**{name}:** {value:.2f}")
        except Exception as e:
            st.error(f"Optimization failed: {e}")

st.markdown("---")
st.markdown(
    "*Note: This reverse optimization process requires significant computation and may take 5 to 10 minutes. Please wait patiently.*"
)
