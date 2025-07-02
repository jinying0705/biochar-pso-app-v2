# -*- coding: utf-8 -*-
"""
Created on Wed Jul  2 20:56:12 2025

@author: 李津莹
"""
import streamlit as st
import pandas as pd
import json
import os
from optimizer import optimize_conditions

st.set_page_config(page_title="Reverse Optimization for Biochar Properties", layout="wide")

# 标题与说明文字
st.markdown("## 🎯 Reverse Optimization for Biochar Properties")
st.markdown(
    "<div style='color:red; font-size:16px;'>"
    "Enter biomass properties and assign weights to biochar properties to design the best experiment condition for prepare your ideal biochar.<br>"
    "*This reverse optimization process requires significant computation and may take 5 to 10 minutes. Please wait patiently.*"
    "</div>",
    unsafe_allow_html=True,
)
st.markdown("---")

# 加载 JSON 数据
json_folder = "./"
json_files = [f for f in os.listdir(json_folder) if f.endswith(".json") and f.startswith("M-XGB_")]
models = {}

for file in json_files:
    with open(os.path.join(json_folder, file), "r") as f:
        models[file] = json.load(f)

# 加载 excel 数据
excel_file = "确定6.0.xlsx"
sheet_names = pd.ExcelFile(excel_file).sheet_names
sheet_selection = st.sidebar.selectbox("Choose biomass type", sheet_names)
data = pd.read_excel(excel_file, sheet_name=sheet_selection)

st.sidebar.markdown("### ⚖️ Assign Weights to Biochar Properties")
default_weights = [5, 4, 3, 2, 2, 2, 1, 1, 1]  # 可自定义初始权重
weights = {}
properties = [
    "Yield (%)", "pH", "Ash (%)", "Volatile matter (%)", "Nitrogen (%)",
    "Fixed carbon (%)", "Carbon (%)", "H/C ratio", "O/C ratio"
]
for i, prop in enumerate(properties):
    weights[prop] = st.sidebar.number_input(f"{prop} weight", min_value=0, max_value=10, value=default_weights[i], step=1)

if st.sidebar.button("Start Optimization"):
    st.success("✅ Optimization started. Please wait...")

    optimized_conditions, predicted_properties = optimize_conditions(
        biomass_data=data.iloc[0],
        weights=weights,
        models=models,
        num_particles=10,
        max_iter=10
    )

    st.success("✅ Optimization completed!")

    st.markdown("### 🛠️ Optimized Experimental Conditions")
    cols1 = st.columns(3)
    condition_labels = ["Highest temperature (°C)", "Heating rate (°C/min)", "Residence time (min)"]
    for i, label in enumerate(condition_labels):
        cols1[i].markdown(
            f"<div style='padding:10px; border:1px solid #ddd; border-radius:10px; background-color:#f4f4f4;'>"
            f"<strong>{label}</strong><br>{optimized_conditions[i]:.2f}</div>",
            unsafe_allow_html=True
        )

    st.markdown("### 📉 Ideal Biochar Properties")
    cols2 = st.columns(3)
    for i, (key, value) in enumerate(predicted_properties.items()):
        col = cols2[i % 3]
        col.markdown(
            f"<div style='padding:10px; border:1px solid #ddd; border-radius:10px; background-color:#ffffff;'>"
            f"<strong>{key}</strong><br>{value:.2f}</div>",
            unsafe_allow_html=True
        )

