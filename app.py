import streamlit as st
import numpy as np
from optimizer import run_pso_optimization

st.set_page_config(page_title="Reverse Optimization for Biochar", layout="wide")

st.markdown("""
    <h2 style='text-align: center; color: black;'>Reverse Optimization for Biochar Properties</h2>
    <div style='text-align: center; font-size: 16px; color: #555555;'>
        Please enter the biomass properties and assign weights to each biochar output property.
        <br>Click "Run Optimization" to find the best experimental conditions using PSO.
    </div><br>
""", unsafe_allow_html=True)

# -------------------- Sidebar: 输入部分 --------------------
st.sidebar.header("📌 Biomass Properties")
biomass_labels = [
    "Ash (%)", "Volatile matter (%)", "Fixed carbon (%)", "Carbon (%)",
    "Hydrogen (%)", "Oxygen (%)", "Nitrogen (%)"
]
fixed_properties = []
for label in biomass_labels:
    val = st.sidebar.number_input(label, value=0.0)
    fixed_properties.append(val)

st.sidebar.header("🎯 Output Property Weights")
output_labels = [
    "Yield (%)", "pH", "Ash (%)", "Volatile matter (%)", "Nitrogen (%)",
    "Fixed carbon (%)", "Carbon (%)", "H/C ratio", "O/C ratio"
]
weights = []
for label in output_labels:
    w = st.sidebar.number_input(f"{label} weight", min_value=0, max_value=10, value=1, step=1)
    weights.append(w)

# -------------------- 主体区域 --------------------
if st.sidebar.button("Run Optimization"):
    with st.spinner("Running PSO optimization, please wait..."):
        opt_conditions, opt_outputs = run_pso_optimization(fixed_properties, weights)

    st.success("✅ Optimization Completed!")

    st.markdown("### 🔧 Optimal Experimental Conditions")
    condition_labels = ["Highest temperature (℃)", "Heating rate (℃/min)", "Residence time (min)"]
    cols1 = st.columns(3)
    for i, label in enumerate(condition_labels):
        cols1[i].markdown(f"""
            <div style='padding:10px; border:1px solid #ddd; border-radius:10px; background-color:#f4f4f4;'>
                <strong>{label}</strong><br><span style='font-size:20px;'>{opt_conditions[i]:.2f}</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("### 📈 Predicted Biochar Properties")
    cols2 = st.columns(3)
    for i, label in enumerate(output_labels):
        cols2[i % 3].markdown(f"""
            <div style='padding:10px; border:1px solid #ddd; border-radius:10px; background-color:#ffffff;'>
                <strong>{label}</strong><br><span style='font-size:20px;'>{opt_outputs[i]:.2f}</span>
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("👈 Please fill in the parameters and click 'Run Optimization'.")

