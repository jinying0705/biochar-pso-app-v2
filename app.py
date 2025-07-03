# app.py
import streamlit as st
import pandas as pd
from optimizer import predict_properties, optimize_conditions

st.set_page_config(page_title="Biochar Prediction & Optimization", layout="wide")

# Title & intro
st.markdown("## 🌱 Biochar Property Prediction & Optimization")
st.markdown("""
This platform predicts biochar properties from biomass and process conditions,  
and can also optimize process parameters to achieve ideal biochar performance.

**Note**: Optimization may take 5–10 minutes depending on computation load.
""")

# Load Excel & sheet
excel_file = "确定6.0.xlsx"
sheet_names = pd.ExcelFile(excel_file).sheet_names
sheet_selection = st.selectbox("Choose biomass type", sheet_names)
data = pd.read_excel(excel_file, sheet_name=sheet_selection)
biomass_row = data.iloc[0]

# Labels
feature_labels = [
    "Ash (%)", "Volatile matter (%)", "Fixed carbon (%)", "Carbon (%)",
    "Hydrogen (%)", "Oxygen (%)", "Nitrogen (%)",
    "Highest temperature (°C)", "Heating rate (°C/min)", "Residence time (min)"
]
output_labels = [
    "Yield (%)", "pH", "Ash (%)", "Volatile matter (%)", "Nitrogen (%)",
    "Fixed carbon (%)", "Carbon (%)", "H/C ratio", "O/C ratio"
]

# --- Biomass A properties (horizontal) ---
st.markdown("### 🔬 Biomass A Properties")
cols_A = st.columns(len(feature_labels[:7]))
for i, label in enumerate(feature_labels[:7]):
    cols_A[i].number_input(label, value=float(biomass_row[i]), disabled=True, key=f"A_{label}")

# --- Two-column layout for Predict and Optimize ---
col1, col2 = st.columns(2)

# --------------------------- Predict (left) ---------------------------
with col1:
    st.markdown("### 🔍 Predict Biochar Properties")

    process_inputs = []
    for i, label in enumerate(feature_labels[7:]):
        val = st.number_input(f"{label}", min_value=0.0, value=300.0, key=f"cond_{i}")
        process_inputs.append(val)

    if st.button("Predict"):
        st.success("Predicting biochar properties...")
        full_input = list(biomass_row[:7]) + process_inputs
        preds = predict_properties(full_input)

        st.markdown("#### 📋 Predicted Biochar Properties")
        cols_pred = st.columns(3)
        for i, label in enumerate(output_labels):
            cols_pred[i % 3].markdown(
                f"<div style='padding:10px; border:1px solid #ddd; border-radius:10px; background-color:#f9f9f9;'>"
                f"<strong>{label}</strong><br>{preds[i]:.2f}</div>",
                unsafe_allow_html=True
            )

# --------------------------- Optimize (right) ---------------------------
with col2:
    st.markdown("### 🎯 Optimize for Desired Properties")

    default_weights = [5, 4, 3, 2, 2, 2, 1, 1, 1]
    weights = []
    for i, label in enumerate(output_labels):
        w = st.number_input(f"{label} weight", min_value=0, max_value=10, value=default_weights[i], key=f"w_{i}")
        weights.append(w)

    if st.button("Optimize"):
        st.success("Optimizing... please wait (may take up to 10 min)")

        opt_conditions, opt_outputs = optimize_conditions(
            fixed_A_properties=list(biomass_row[:7]),
            weights=weights
        )

        st.markdown("#### 🛠️ Optimal Process Conditions")
        cols_optcond = st.columns(3)
        for i, label in enumerate(feature_labels[7:]):
            cols_optcond[i % 3].markdown(
                f"<div style='padding:10px; border:1px solid #ccc; border-radius:10px; background-color:#eef2f5;'>"
                f"<strong>{label}</strong><br>{opt_conditions[i]:.2f}</div>",
                unsafe_allow_html=True
            )

        st.markdown("#### 🌟 Predicted Biochar Under Optimal Conditions")
        cols_optout = st.columns(3)
        for i, label in enumerate(output_labels):
            cols_optout[i % 3].markdown(
                f"<div style='padding:10px; border:1px solid #ccc; border-radius:10px; background-color:#ffffff;'>"
                f"<strong>{label}</strong><br>{opt_outputs[i]:.2f}</div>",
                unsafe_allow_html=True
            )
