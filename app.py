import streamlit as st
import numpy as np
from optimizer import predict_properties, optimize_conditions

st.set_page_config(page_title="Reverse Optimization for Biochar Properties", layout="wide")

st.title("🌱 Reverse Optimization for Biochar Properties")
st.write("Enter biomass properties and assign weights to output properties to design the best experiment condition for preparing your ideal biochar.")

st.markdown(
    "*This reverse optimization process requires significant computation and may take 5 to 10 minutes. Please wait patiently.*",
    unsafe_allow_html=True,
)

# ---------- Biomass Properties & Process Inputs ----------
st.markdown("### 🧪 Biomass A Properties & Process Parameters")

labels = [
    "Ash (%)", "Volatile matter (%)", "Fixed carbon (%)",
    "Carbon (%)", "Hydrogen (%)", "Oxygen (%)", "Nitrogen (%)",
    "Highest temperature (°C)", "Heating rate (°C/min)", "Residence time (min)"
]
defaults = [0.0] * 7 + [300.0, 10.0, 30.0]

cols = st.columns(3)
inputs = []
for i, label in enumerate(labels):
    with cols[i % 3]:
        value = st.number_input(label, value=defaults[i], step=0.01)
        inputs.append(value)

# ---------- Forward Prediction ----------
st.markdown("### 🔍 Forward Prediction")

if st.button("Predict"):
    fwd_inputs = inputs
    outputs = predict_properties(fwd_inputs)

    st.subheader("Ideal Biochar Properties")
    output_labels = [
        "Yield (%)", "pH", "Ash (%)", "Volatile matter (%)",
        "Fixed carbon (%)", "Carbon (%)", "Nitrogen (%)",
        "H/C ratio", "O/C ratio"
    ]
    for label, value in zip(output_labels, outputs):
        st.write(f"**{label}**: {value:.2f}")

# ---------- Reverse Optimization ----------
st.markdown("### 🎯 Reverse Optimization")

st.write("Enter biomass features and assign weights to output properties to search for the best experiment condition for preparing your ideal biochar.")

weights_labels = [
    "Yield (%) weight", "pH weight", "Ash (%) weight", "Volatile matter (%) weight",
    "Fixed carbon (%) weight", "Carbon (%) weight", "Nitrogen (%) weight",
    "H/C ratio weight", "O/C ratio weight"
]
weight_cols = st.columns(3)
weights = []
for i, label in enumerate(weights_labels):
    with weight_cols[i % 3]:
        w = st.number_input(label, min_value=0.0, value=1.0, step=0.1)
        weights.append(w)

if st.button("Optimize"):
    fixed_A = inputs[:7]  # only biomass A properties
    best_conditions, predicted_outputs = optimize_conditions(fixed_A, weights)

    st.subheader("Optimized Experimental Conditions")
    st.write(f"**Highest temperature (°C):** {best_conditions[0]:.2f}")
    st.write(f"**Heating rate (°C/min):** {best_conditions[1]:.2f}")
    st.write(f"**Residence time (min):** {best_conditions[2]:.2f}")

    st.subheader("Ideal Biochar Properties")
    output_labels = [
        "Yield (%)", "pH", "Ash (%)", "Volatile matter (%)",
        "Fixed carbon (%)", "Carbon (%)", "Nitrogen (%)",
        "H/C ratio", "O/C ratio"
    ]
    for label, value in zip(output_labels, predicted_outputs):
        st.write(f"**{label}**: {value:.2f}")

