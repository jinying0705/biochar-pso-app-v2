# 🌱 Biochar PSO App (Reverse Optimization)

A Streamlit web application for **reverse optimization of biochar experimental conditions** based on ideal output properties using **Particle Swarm Optimization (PSO)**.

---

## 🔍 Purpose

This app helps **researchers and engineers** determine the best experimental parameters (e.g., temperature, heating rate, residence time) to produce biochar with desired properties, such as high yield, optimal pH, and specific elemental composition.

---

## 📦 Features

- 🔁 Reverse design: Input desired **biochar properties** and assign weights.
- ⚙️ PSO-based backend to search optimal **pyrolysis conditions**.
- 📊 Real-time visualization of predicted outputs.
- 🧠 Supports multi-objective optimization via custom weighting.

---

## 📂 File Structure

biochar-pso-app-v2/
├── app.py # Streamlit app entry point
├── optimizer.py # PSO optimization logic
├── requirements.txt # Python dependencies
├── README.md # Project documentation (this file)
├── *.json # Trained model and configuration files
└── *.xlsx # Biomass property inputs (optional)

---

## 🚀 How to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/jinying0705/biochar-pso-app-v2.git
   cd biochar-pso-app-v2
2. Install required packages:
   pip install -r requirements.txt
3. Run the app:
   streamlit run app.py
🌐 Deployment
This app is deployed on Streamlit Cloud.
You can launch it directly once GitHub is connected and authorized.

🧠 Notes
Some computations may take 5–10 minutes, depending on PSO iterations.

.json files store trained models; do not modify them manually.

.xlsx files include biomass data for model input; you can update them with your own values.

📮 Contact
Maintainer: @jinying0705
Issues or questions? Feel free to open a GitHub issue.

📜 License
This project is for academic and non-commercial use only.

