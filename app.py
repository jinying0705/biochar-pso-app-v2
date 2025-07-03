import streamlit as st
import numpy as np
from optimizer import predict_properties, optimize_conditions

st.set_page_config(page_title="Biochar Prediction & Optimization", layout="wide")

st.title("🌱 Biochar Property Prediction & Optimization")
st.markdown("""
This platform predicts biochar properties from biomass and process conditions,  
and can also optimize process parameters to achieve ideal biochar performance.  
**Note:** Optimization may take 5–10 minutes depending on computational load.
""")

# ---------- Input: Biomass A properties ----------
st.subheader("🧪 Input Biomass Properties")
biomass_inputs = []
biomass_labels = ["Ash (%)", "Volatile matter (%)", "Fixed carbon (%)", "Carbon (%)", 
                  "Hydrogen (%)", "Oxygen (%)", "Nitrogen (%)"]
cols = st.columns(7)
for i, label in enumerate(biomass_labels):
    val = cols[i].number_input(label, value=0.0, format="%.2f")
    biomass_inputs.append(val)

# ---------- Input: Process parameters (for prediction) ----------
st.subheader("🔍 Predict Biochar Properties")
temp = st.number_input("Highest temperature (°C)", value=300.0, format="%.2f")
rate = st.number_input("Heating rate (°C/min)", value=10.0, format="%.2f")
time = st.number_input("Residence time (min)", value=30.0, format="%.2f")

# ---------- Input: Optimization weights ----------
st.subheader("🎯 Optimize for Desired Properties")
weights = {}
output_props = [
    "Yield (%)", "pH", "Ash (%)", "Volatile matter (%)", "Nitrogen (%)",
    "Fixed carbon (%)", "Carbon (%)", "H/C ratio", "O/C ratio"
]
cols = st.columns(3)
for i, prop in enumerate(output_props):
    weights[prop] = cols[i % 3].number_input(f"{prop} weight", value=1, step=1)

# ---------- Prediction ----------
if st.button("Predict"):
    prediction_inputs = biomass_inputs + [temp, rate, time]
    pred_outputs = predict_properties(prediction_inputs)
    
    st.success("✅ Prediction completed!")
    st.subheader("📊 Predicted Biochar Properties")
    pred_cols = st.columns(3)
    for i, (key, value) in enumerate(zip(output_props, pred_outputs)):
        pred_cols[i % 3].metric(key, f"{value:.2f}")

# ---------- Optimization ----------
if st.button("Optimize"):
    opt_conditions, opt_outputs = optimize_conditions(biomass_inputs, list(weights.values()))
    
    st.success("✅ Optimization completed!")
    st.subheader("🔧 Optimal Experimental Conditions")
    opt_cols = st.columns(3)
    opt_labels = ["Highest temperature (°C)", "Heating rate (°C/min)", "Residence time (min)"]
    for i, val in enumerate(opt_conditions):
        opt_cols[i].metric(opt_labels[i], f"{val:.2f}")
    
    st.subheader("📈 Predicted Biochar Properties from Optimal Conditions")
    opt_output_cols = st.columns(3)
    for i, (key, value) in enumerate(zip(output_props, opt_outputs)):
        opt_output_cols[i % 3].metric(key, f"{value:.2f}")
