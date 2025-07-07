import streamlit as st
import numpy as np
from optimizer import predict_properties, optimize_conditions

st.set_page_config(page_title="Biochar Design", layout="wide")

st.markdown("<h1 style='font-size: 28px;'>🌱 The multi-task learning model used to predict the properties and customize the design of biochar</h1>", unsafe_allow_html=True)
st.markdown("<h3>🧪 Biomass Properties & Pyrolysis Conditions</h3>", unsafe_allow_html=True)

# 先放7个输入在一行（上方）
input_cols = st.columns(7)
ash = input_cols[0].number_input("Ash (%)", min_value=0.0, step=0.01)
volatile_matter = input_cols[1].number_input("Volatile matter (%)", min_value=0.0, step=0.01)
fixed_carbon = input_cols[2].number_input("Fixed carbon (%)", min_value=0.0, step=0.01)
carbon = input_cols[3].number_input("Carbon (%)", min_value=0.0, step=0.01)
hydrogen = input_cols[4].number_input("Hydrogen (%)", min_value=0.0, step=0.01)
oxygen = input_cols[5].number_input("Oxygen (%)", min_value=0.0, step=0.01)
nitrogen = input_cols[6].number_input("Nitrogen (%)", min_value=0.0, step=0.01)

# 下方左右两块：Forward Prediction 和 Reverse Optimization
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🎯 Forward Prediction")
    st.markdown("Please enter 10 biomass-related properties above and click Predict to view the predicted biochar characteristics.")

    highest_temp = st.number_input("Highest temperature (°C)", value=300.0, step=1.0)
    heating_rate = st.number_input("Heating rate (°C/min)", value=10.0, step=0.1)
    residence_time = st.number_input("Residence time (min)", value=30.0, step=1.0)

    if st.button("Predict"):
        fwd_inputs = [ash, volatile_matter, fixed_carbon, carbon, hydrogen, oxygen,
                      nitrogen, highest_temp, heating_rate, residence_time]
        outputs = predict_properties(fwd_inputs)
        st.subheader("Predicted Biochar Properties")
        st.write(outputs)

with col2:
    st.markdown("### 🔍 Reverse Optimization")
    st.markdown("Enter the biomass properties above and pyrolysis conditions below to view the predicted biochar properties.")

    weight_labels = [
        "Yield (%) weight", "pH weight", "Ash (%) weight",
        "Volatile matter (%) weight", "Nitrogen (%) weight", "Fixed carbon (%) weight",
        "Carbon (%) weight", "H/C ratio weight", "O/C ratio weight"
    ]

    input_weights = {}
    for i in range(0, len(weight_labels), 3):
        row = st.columns(3)
        for j in range(3):
            label = weight_labels[i + j]
            input_weights[label] = row[j].number_input(label, value=1.0, step=0.1)

    if st.button("Optimize"):
        biomass_inputs = [ash, volatile_matter, fixed_carbon, carbon, hydrogen, oxygen, nitrogen]
        optimal_conditions = optimize_conditions(biomass_inputs, input_weights)
        st.subheader("Optimal Experimental Conditions")
        st.write(optimal_conditions)

st.markdown(
    "<p style='font-size: 12px; color: gray;'><em>Note: This reverse optimization process requires significant computation and may take 5 to 10 minutes. Please wait patiently.</em></p>",
    unsafe_allow_html=True
)
