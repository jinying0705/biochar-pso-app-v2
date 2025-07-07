import streamlit as st
import numpy as np
from optimizer import predict_properties, optimize_conditions

st.set_page_config(page_title="Biochar Design", layout="wide")

# 顶部标题
st.markdown("""
<div style='text-align: center; font-size: 34px; padding: 10px 0; font-weight: bold;'>
    🌱 The multi-task learning model used to predict the properties and customize the design of biochar
</div>
""", unsafe_allow_html=True)

# 基础性质输入
st.markdown("<h3>🧪 Biomass Properties & Pyrolysis Conditions</h3>", unsafe_allow_html=True)

input_cols = st.columns(7)
ash = input_cols[0].number_input("Ash (%)", min_value=0.0, step=0.01)
volatile_matter = input_cols[1].number_input("Volatile matter (%)", min_value=0.0, step=0.01)
fixed_carbon = input_cols[2].number_input("Fixed carbon (%)", min_value=0.0, step=0.01)
carbon = input_cols[3].number_input("Carbon (%)", min_value=0.0, step=0.01)
hydrogen = input_cols[4].number_input("Hydrogen (%)", min_value=0.0, step=0.01)
oxygen = input_cols[5].number_input("Oxygen (%)", min_value=0.0, step=0.01)
nitrogen = input_cols[6].number_input("Nitrogen (%)", min_value=0.0, step=0.01)

# 分左右两列
col1, col2 = st.columns(2)

# 🎯 左侧：正向预测
with col1:
    st.markdown("### 🎯 Forward Prediction")
    st.markdown("Enter the biomass properties above and pyrolysis conditions below to view the predicted biochar properties.")

    highest_temp = st.number_input("Highest temperature (°C)", value=300.0, step=1.0)
    heating_rate = st.number_input("Heating rate (°C/min)", value=10.0, step=0.1)
    residence_time = st.number_input("Residence time (min)", value=30.0, step=1.0)

    if st.button("Predict", key="predict_btn"):
        fwd_inputs = [ash, volatile_matter, fixed_carbon, carbon, hydrogen, oxygen,
                      nitrogen, highest_temp, heating_rate, residence_time]
        outputs = predict_properties(fwd_inputs)

        st.markdown("### 🧾 Predicted Biochar Properties")

        output_labels = [
            "Yield (%)", "pH", "Ash (%)", "Volatile matter (%)",
            "Nitrogen (%)", "Fixed carbon (%)", "Carbon (%)",
            "H/C ratio", "O/C ratio"
        ]

        styled_output = ""
        for label, value in zip(output_labels, outputs):
            styled_output += f"""
            <div style="padding:8px 14px; margin:5px 0; background-color:#f9f9f9;
                        border-left: 5px solid #4CAF50; font-size:15px;">
                <b>{label}</b>: {float(value):.2f}
            </div>
            """
        st.markdown(styled_output, unsafe_allow_html=True)

# 🔍 右侧：逆向优化
with col2:
    st.markdown("### 🔍 Reverse Optimization")
    st.markdown("Enter the biomass properties above and assign weights to the biochar properties below to design optimal experimental conditions for preparing your ideal biochar.")
    st.markdown("*This reverse optimization process requires significant computation and may take 1 to 5 minutes. Please wait patiently.*")

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

    if st.button("Optimize", key="optimize_btn"):
        biomass_inputs = [ash, volatile_matter, fixed_carbon, carbon, hydrogen, oxygen, nitrogen]
        weights_list = list(input_weights.values())

        opt_conditions, predicted_outputs = optimize_conditions(biomass_inputs, weights_list)

        st.markdown("### 🧪 Optimal Experimental Conditions")

        cond_labels = ["Highest temperature (°C)", "Heating rate (°C/min)", "Residence time (min)"]
        prop_labels = [
            "Yield (%)", "pH", "Ash (%)", "Volatile matter (%)",
            "Nitrogen (%)", "Fixed carbon (%)", "Carbon (%)",
            "H/C ratio", "O/C ratio"
        ]

        styled_opt_conditions = ""
        for label, value in zip(cond_labels, opt_conditions):
            styled_opt_conditions += f"""
            <div style="padding:8px 14px; margin:5px 0; background-color:#f0f9ff;
                        border-left: 5px solid #2196F3; font-size:15px;">
                <b>{label}</b>: {value:.2f}
            </div>
            """
        st.markdown(styled_opt_conditions, unsafe_allow_html=True)

        st.markdown("### 🧾 Predicted Biochar Properties")

        styled_pred_output = ""
        for label, value in zip(prop_labels, predicted_outputs):
            styled_pred_output += f"""
            <div style="padding:8px 14px; margin:5px 0; background-color:#f9f9f9;
                        border-left: 5px solid #4CAF50; font-size:15px;">
                <b>{label}</b>: {value:.2f}
            </div>
            """
        st.markdown(styled_pred_output, unsafe_allow_html=True)

