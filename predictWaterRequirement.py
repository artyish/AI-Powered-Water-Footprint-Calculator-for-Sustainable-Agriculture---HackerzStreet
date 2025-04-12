import joblib
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import io



model = joblib.load('neural_net_model.pkl')

columns  = ["CROP TYPE_BANANA", "CROP TYPE_BEAN",
 "CROP TYPE_CABBAGE", "CROP TYPE_CITRUS", "CROP TYPE_COTTON",
 "CROP TYPE_MAIZE", "CROP TYPE_MELON", "CROP TYPE_MUSTARD",
 "CROP TYPE_ONION", "CROP TYPE_POTATO", "CROP TYPE_RICE",
 "CROP TYPE_SOYABEAN", "CROP TYPE_SUGARCANE", "CROP TYPE_TOMATO",
 "CROP TYPE_WHEAT", "SOIL TYPE_DRY", "SOIL TYPE_HUMID", "SOIL TYPE_WET",
 "REGION_DESERT", "REGION_HUMID", "REGION_SEMI ARID",
 "REGION_SEMI HUMID", "TEMPERATURE_10-20", "TEMPERATURE_20-30",
 "TEMPERATURE_30-40", "TEMPERATURE_40-50", "WEATHER CONDITION_NORMAL",
 "WEATHER CONDITION_RAINY", "WEATHER CONDITION_SUNNY",
 "WEATHER CONDITION_WINDY"]
       
     
def custom_predict(user_input):
       input_df = pd.DataFrame([[0]*len(columns)], columns=columns)

       for key, value in user_input.items():
        col_name = f"{key}_{value.upper()}"
        if col_name in columns:
            input_df.at[0, col_name] = 1

       prediction = model.predict(input_df)

       return input_df,prediction

def custom_predict_weather_variation(user_input):
    weather_conditions = ["SUNNY", "RAINY", "WINDY", "NORMAL"]
    predictions = []

    for weather in weather_conditions:
        modified_input = user_input.copy()
        modified_input["WEATHER CONDITION"] = weather

        input_df = pd.DataFrame([[0] * len(columns)], columns=columns)
        for key, value in modified_input.items():
            col_name = f"{key}_{value.upper()}"
            if col_name in columns:
                input_df.at[0, col_name] = 1

        prediction = model.predict(input_df)
        predictions.append(prediction[0])

    # Create bar plot
    fig, ax = plt.subplots()
    ax.bar(weather_conditions, predictions, color='skyblue')
    ax.set_title("Water Requirement Prediction by Weather Condition")
    ax.set_ylabel("Water Requirement (mm/m²)")
    ax.set_xlabel("Weather Condition")
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)

    # Save to buffer
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    plt.close(fig)  # 🧼 prevent Streamlit from showing it again automatically
    buf.seek(0)
    return buf