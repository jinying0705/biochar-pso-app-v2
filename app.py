# app.py
import streamlit as st
import numpy as np
from optimizer import optimize_conditions


st.set_page_config(page_title="Biochar Prediction & Optimization", layout="wide")

# ------------------- Title Section -------------------
st.markdown("""
    <h1 style='text-align: center; font-size: 32px;'>🌱 Biochar Property Prediction & Optimization</h1>
    <p style='text-align: center; font-size: 18px;'>
    This platform predicts biochar properties from biomass and process parameters,  
    and also optimizes experimental conditions to meet desired biochar performance.
    </p>
    <hr>
""", unsafe_allow_html=True)

# ------------------- Biomass A Input -------------------
st.subheader("🧪 Biomass A Properties")
biomass_labels = ["Ash (%)", "Volatile matter (%)", "Fixed carbon (%)", 
                  "Carbon (%)", "Hydrogen (%)", "Oxygen (%)", "Nitrogen (%)"]
biomass_inputs = []
cols_biomass = st.columns(len(biomass_labels))
for i, label in enumerate(biomass_labels):
    val = cols_biomass[i].number_input(label, value=0.0, format="%.2f")
    biomass_inputs.append(val)

# ------------------- Split Columns for Predict & Optimize -------------------
left_col, right_col = st.columns(2)

# -------- Left Column: Forward Prediction --------
with left_col:
    st.subheader("🔍 Forward Prediction")

    temp = st.number_input("Highest temperature (°C)", value=300.0, format="%.2f")
    rate = st.number_input("Heating rate (°C/min)", value=10.0, format="%.2f")
    time = st.number_input("Residence time (min)", value=30.0, format="%.2f")

    if st.button("Predict"):
        def predict_properties(inputs):
            import pandas as pd
            from sklearn.preprocessing import StandardScaler
            from xgboost import XGBRegressor

            X = pd.read_excel("确定6.0.xlsx").iloc[:, 0:10].values
            scaler = StandardScaler().fit(X)

            input_scaled = scaler.transform([inputs])
            results = []

            for i in range(9):  # 9 output models
                model = XGBRegressor()
                model.load_model(f"M-XGB_{i+1}.json")
                pred = model.predict(input_scaled)[0]
                results.append(pred)
            return results

        pred_inputs = biomass_inputs + [temp, rate, time]
        pred_outputs = predict_properties(pred_inputs)

        st.success("✅ Prediction Completed")
        pred_labels = [
            "Yield (%)", "pH", "Ash (%)", "Volatile matter (%)", "Nitrogen (%)",
            "Fixed carbon (%)", "Carbon (%)", "H/C ratio", "O/C ratio"
        ]
        pred_cols = st.columns(3)
        for i, (label, value) in enumerate(zip(pred_labels, pred_outputs)):
            pred_cols[i % 3].metric(label, f"{value:.2f}")

# -------- Right Column: Reverse Optimization --------
with right_col:
    st.subheader("🎯 Reverse Optimization")

    weight_labels = [
        "Yield (%)", "pH", "Ash (%)", "Volatile matter (%)", "Nitrogen (%)",
        "Fixed carbon (%)", "Carbon (%)", "H/C ratio", "O/C ratio"
    ]
    weights = []
    cols_weights = st.columns(3)
    for i, label in enumerate(weight_labels):
        val = cols_weights[i % 3].number_input(f"{label} weight", value=1, step=1)
        weights.append(val)

    if st.button("Optimize"):
        with st.spinner("⏳ Optimizing using PSO..."):
            best_conditions, best_outputs = run_pso_optimization(biomass_inputs, weights)

        st.success("✅ Optimization Completed")

        st.markdown("#### 🔧 Optimal Experimental Conditions")
        condition_labels = ["Highest temperature (°C)", "Heating rate (°C/min)", "Residence time (min)"]
        cond_cols = st.columns(3)
        for i, val in enumerate(best_conditions):
            cond_cols[i].metric(condition_labels[i], f"{val:.2f}")

        st.markdown("#### 📈 Predicted Biochar Properties")
        output_cols = st.columns(3)
        for i, (label, val) in enumerate(zip(weight_labels, best_outputs)):
            output_cols[i % 3].metric(label, f"{val:.2f}")
