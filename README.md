# 🌱 The multi-task learning model used to predict the properties and optimize the design of biochar

A Streamlit web application for real-time
1️⃣ **Forward prediction of biochar properties** based on 7 biomass properties and 3 pyrolysis conditions.
2️⃣ **Reverse optimization of biochar experimental conditions** based on ideal biochar properties using **Particle Swarm Optimization (PSO)**.

---

## 🔍 Purpose

This app not only helps **researchers and engineers** predict the properties of biochar in advance, but also determines the best experimental parameters (e.g., temperature, heating rate, residence time) to produce biochar with desired properties, such as high yield, optimal pH, and specific elemental composition.

---

## 📦 Features

- 📊 Forward prediction: Real-time visualization of predicted outputs.
- 🔁 Reverse design: Input desired **biochar properties** and assign weights.
- ⚙️ PSO-based backend to search optimal **pyrolysis conditions**.
- 🧠 Supports multi-objective optimization via custom weighting.

---

## 📂 File Structure

biochar-slow pyrolysis-app/
├── app.py # Streamlit app entry point
├── predicter & optimizer.py # Forward prediction & Reverse optimization logic
├── requirements.txt # Python dependencies
├── README.md # Project documentation (this file)
├── *.json # Trained model and configuration files
└── *.xlsx # Biomass property inputs (optional)

---

## 🚀 How to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/jinying0705/biochar-slow pyrolysis-app.git
   cd biochar-slow pyrolysis-app
2. Install required packages:
   pip install -r requirements.txt
3. Run the app:
   streamlit run app.py
🌐 Deployment
This app is deployed on Streamlit Cloud.
You can launch it directly once GitHub is connected and authorized.

🧠 Notes
Some computations may take 1–5 minutes, depending on PSO iterations.

.json files store trained models; do not modify them manually.

.xlsx files include biomass data for model input; you can update them with your own values.

📮 Contact
Maintainer: @jinying0705
Issues or questions? Feel free to open a GitHub issue.

📜 License
This project is for academic and non-commercial use only.

