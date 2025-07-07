import streamlit as st
import numpy as np
from optimizer import predict_properties, optimize_conditions

st.set_page_config(page_title="Biochar Prediction & Optimization", layout="wide")

st.markdown(
    "<h1 style='font-size: 30px;'>🌱 The multi-task learning model used to predict the properties and customize the design of biochar</h1>",
    unsafe_allow_html=True,
)

st.markdown("### 🧪 Biomass Properties & Pyrolysis Conditions")

# 生物质属性输入框（全部放在一行）
with st.container():
    cols = st.columns(7)
    biomass_inputs = {}
    labels = ["Ash (%)", "Volatile matter (%)", "Fixed carbon (%)", "Carbon (%)",
              "Hydrogen (%)", "Oxygen (%)", "Nitrogen (%)"]
    for col, label in zip(cols, labels):
        biomass_inputs[label] = col.number_input(label, min_value=0.0, max_value=100.0, value=0.0)

# 页面左右分栏
left_col, right_col = st.columns(2)

# ==== 左侧：Forward Prediction ====
with left_col:
    st.markdown("### 🎯 Forward Prediction")
    st.markdown("Please enter 10 biomass-related properties above and click Predict to view the predicted biochar characteristics.")

    highest_temp = st.number_input("Highest temperature (°C)", min_value=0.0, max_value=1000.0, value=300.0)
    heating_rate = st.number_input("Heating rate (°C/min)", min_value=0.0, max_value=100.0, value=10.0)
    residence_time = st.number_input("Residence time (min)", min_value=0.0, max_value=300.0, value=30.0)

    if st.button("Predict"):
        fwd_inputs = list(biomass_inputs.values()) + [highest_temp, heating_rate, residence_time]
        outputs = predict_properties(fwd_inputs)
        st.subheader("📋 Ideal Biochar Properties")
        st.write(outputs)

# ==== 右侧：Reverse Optimization ====
with right_col:
    st.markdown("### 🔍 Reverse Optimization")
    st.markdown("Enter the biomass properties above and assign weights to the biochar properties below to design optimal experimental conditions for preparing your ideal biochar.")

    weights = {}
    weight_labels = ["Yield (%) weight", "pH weight", "Ash (%) weight", "Volatile matter (%) weight",
                     "Nitrogen (%) weight", "Fixed carbon (%) weight", "Carbon (%) weight",
                     "H/C ratio weight", "O/C ratio weight"]

    weight_cols = st.columns(3)
    for i, label in enumerate(weight_labels):
        col = weight_cols[i % 3]
        weights[label] = col.number_input(label, min_value=0.0, max_value=10.0, value=1.0, step=0.1)

    if st.button("Optimize"):
        input_properties = list(biomass_inputs.values())
        weights_array = list(weights.values())
        result = optimize_conditions(input_properties, weights_array)
        st.subheader("⚙️ Optimized Experimental Conditions")
        st.write(result)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    "<i>Note: This reverse optimization process requires significant computation and may take 5 to 10 minutes. Please wait patiently.</i>",
    unsafe_allow_html=True,
)
