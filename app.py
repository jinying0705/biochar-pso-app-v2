# app.py
import streamlit as st
import pandas as pd
import json
import os
from optimizer import predict_properties, optimize_conditions

st.set_page_config(page_title="Biochar Prediction and Optimization", layout="wide")

st.markdown("## 🌱 Biochar Property Prediction & Optimization Platform")

st.markdown("""
This tool allows you to **predict** biochar properties from biomass and process conditions, or **optimize** process conditions to obtain ideal biochar.  
Choose the desired mode below:
""")

mode = st.radio("Select Function", ["🔍 Predict Biochar Properties", "🎯 Optimize Process Conditions"], horizontal=True)
st.markdown("---")

# Load Excel data
excel_file = "确定6.0.xlsx"
sheet_names = pd.ExcelFile(excel_file).sheet_names
sheet_selection = st.selectbox("Select Biomass Type", sheet_names)
data = pd.read_excel(excel_file, sheet_name=sheet_selection)
biomass_row = data.iloc[0]

# Feature names
feature_labels = [
    "Ash (%)", "Volatile matter (%)", "Fixed carbon (%)", "Carbon (%)",
    "Hydrogen (%)", "Oxygen (%)", "Nitrogen (%)",
    "Highest temperature (°C)", "Heating rate (°C/min)", "Residence time (min)"
]

# Output names
output_labels = [
    "Yield (%)", "pH", "Ash (%)", "Volatile matter (%)", "Nitrogen (%)",
    "Fixed carbon (%)", "Carbon (%)", "H/C ratio", "O/C ratio"
]

if mode == "🔍 Predict Biochar Properties":
    st.markdown("### 🔢 Input Process Conditions")
    cols = st.columns(3)
    input_values = []

    for i, label in enumerate(feature_labels):
        if i < 7:
            # Use biomass_row for the 7 fixed biomass properties
            input_values.append(biomass_row[i])
            cols[i % 3].number_input(label, value=float(biomass_row[i]), disabled=True)
        else:
            val = cols[i % 3].number_input(label, min_value=0.0, value=300.0)
            input_values.append(val)

    if st.button("Predict"):
        st.success("✅ Predicting biochar properties...")
        predictions = predict_properties(input_values)

        st.markdown("### 📋 Predicted Biochar Properties")
        cols_out = st.columns(3)
        for i, label in enumerate(output_labels):
            cols_out[i % 3].markdown(
                f"<div style='padding:10px; border:1px solid #ddd; border-radius:10px; background-color:#f9f9f9;'>"
                f"<strong>{label}</strong><br>{predictions[i]:.2f}</div>",
                unsafe_allow_html=True
            )

elif mode == "🎯 Optimize Process Conditions":
    st.markdown("### ⚖️ Assign Weights to Desired Biochar Properties")
    default_weights = [5, 4, 3, 2, 2, 2, 1, 1, 1]
    weight_inputs = []
    cols_w = st.columns(3)
    for i, label in enumerate(output_labels):
        weight = cols_w[i % 3].number_input(f"{label} weight", min_value=0, max_value=10, value=default_weights[i])
        weight_inputs.append(weight)

    if st.button("Start Optimization"):
        st.success("⏳ Optimizing, this may take a few minutes...")

        opt_conditions, opt_outputs = optimize_conditions(
            fixed_A_properties=biomass_row[:7],
            weights=weight_inputs
        )

        st.success("✅ Optimization Completed!")

        st.markdown("### 🛠️ Recommended Process Conditions")
        cond_labels = feature_labels[7:]
        cols_cond = st.columns(3)
        for i, label in enumerate(cond_labels):
            cols_cond[i].markdown(
                f"<div style='padding:10px; border:1px solid #ccc; border-radius:10px; background-color:#eef2f5;'>"
                f"<strong>{label}</strong><br>{opt_conditions[i]:.2f}</div>",
                unsafe_allow_html=True
            )

        st.markdown("### 🌟 Expected Biochar Properties")
        cols_prop = st.columns(3)
        for i, label in enumerate(output_labels):
            cols_prop[i % 3].markdown(
                f"<div style='padding:10px; border:1px solid #ccc; border-radius:10px; background-color:#ffffff;'>"
                f"<strong>{label}</strong><br>{opt_outputs[i]:.2f}</div>",
                unsafe_allow_html=True
            )

