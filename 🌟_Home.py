import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
import plotly.express as px
import numpy as npst
import io

st.set_page_config(
    page_title="Water Requirement App",
    page_icon="💧",
    layout="centered"
)

# 🏠 App title
st.title("AquaFootprint AI for Sustainable Agriculture")
st.subheader("Empowering Farmers with Data-Driven Decisions 🌾")


st.markdown("#### 💡 About This App")
st.write("""
This **Water Requirement** Predictor is designed to help farmers and agricultural planners make smart, data-driven decisions by estimating crop-specific water needs per irrigation event, based on real-time weather and soil conditions.

#### 🌾 What it does:
- **Predicts the optimal water requirement** for various crops based on:
  - Crop type
  - Soil condition
  - Regional humidity
  - Temperature range
  - Weather condition

- **Recommends suitable crops** based on weather and soil!

#### 🧠 How it helps:
- **Water Efficiency**: Know exactly how much to irrigate, saving water.
- **Crop Planning**: Choose crops best suited to your environment.
- **Sustainability**: Encourages smarter agriculture with fewer resources.

Try the prediction tool in the sidebar and optimize your field like a pro!
""")
st.markdown("### 📊 Actual vs Predicted Water Requirement by Crop Type")

with open("actual_vs_predicted.html",  encoding="utf-8") as f:
    html = f.read()

st.components.v1.html(html, height=600)


