import streamlit as st
import numpy as np
from optimizer import optimize_conditions

# ---------- 页面设置 ----------
st.set_page_config(page_title="Biochar Prediction & Optimization", layout="wide")

# ---------- 页面标题和说明 ----------
st.markdown("<h1>🌱 Biochar Property Prediction & Optimization</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='font-size:18px'>This platform predicts biochar properties from biomass and process conditions, "
    "and optimizes process parameters to achieve ideal biochar performance.</p>", 
    unsafe_allow_html=True
)
st.markdown(
    "<b>Note:</b> Optimization may take 5–10 minutes depending on computational load.",
    unsafe_allow_html=True
)

# ---------- 第一部分：输入A的性质 ----------
st.subheader("🧪 Biomass A Properties")
biomass_labels = ["Ash (%)", "Volatile matter (%)", "Fixed carbon (%)", "Carbon (%)", 
                  "Hydrogen (%)", "Oxygen (%)", "Nitrogen (%)"]
biomass_inputs = []
cols = st.columns(len(biomass_labels))
for i, label in enumerate(biomass_labels):
    val = cols[i].number_input(label, value=0.0, format="%.2f")
    biomass_inputs.append(val)

# ---------- 第二部分：预测与优化并排 ----------
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("🔍 Forward Prediction")
    temp = st.number_input("Highest temperature (°C)", value=300.0, format="%.2f")
    rate = st.number_input("Heating rate (°C/min)", value=10.0, format="%.2f")
    time = st.number_input("Residence time (min)", value=30.0, format="%.2f")
    if st.button("Predict"):
        prediction_inputs = biomass_inputs + [temp, rate, time]

        # 替换为你自己的模型调用逻辑
        def predict_properties(inputs):
            return [np.random.uniform(0, 100) for _ in range(10)]  # 示例随机数

        pred_outputs = predict_properties(prediction_inputs)

        st.success("✅ Prediction completed!")
        st.subheader("📊 Predicted Biochar Properties")
        pred_props = [
            "Yield (%)", "pH", "Ash (%)", "Volatile matter (%)", "Nitrogen (%)",
            "Fixed carbon (%)", "Carbon (%)", "H/C ratio", "O/C ratio", "Hydrogen-carbon ratio"
        ]
        cols_pred = st.columns(3)
        for i, (k, v) in enumerate(zip(pred_props, pred_outputs)):
            cols_pred[i % 3].metric(k, f"{v:.2f}")

with right_col:
    st.subheader("🎯 Reverse Optimization")
    weights = {}
    opt_props = [
        "Yield (%)", "pH", "Ash (%)", "Volatile matter (%)", "Nitrogen (%)",
        "Fixed carbon (%)", "Carbon (%)", "Hydrogen-carbon ratio", "Oxygen-carbon ratio"
    ]
    cols_opt = st.columns(3)
    for i, prop in enumerate(opt_props):
        weights[prop] = cols_opt[i % 3].number_input(f"{prop} weight", value=1, step=1)

    if st.button("Optimize"):
        opt_conditions, opt_outputs = optimize_conditions(biomass_inputs, list(weights.values()))

        st.success("✅ Optimization completed!")
        st.subheader("🔧 Optimal Experimental Conditions")
        opt_labels = ["Highest temperature (°C)", "Heating rate (°C/min)", "Residence time (min)"]
        opt_cols = st.columns(3)
        for i, val in enumerate(opt_conditions):
            opt_cols[i].metric(opt_labels[i], f"{val:.2f}")

        st.subheader("📈 Predicted Biochar Properties from Optimal Conditions")
        opt_out_cols = st.columns(3)
        for i, (k, v) in enumerate(zip(opt_props, opt_outputs)):
            opt_out_cols[i % 3].metric(k, f"{v:.2f}")
