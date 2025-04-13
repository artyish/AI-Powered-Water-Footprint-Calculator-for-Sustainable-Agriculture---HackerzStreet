import streamlit as st
from streamlit_folium import st_folium
import requests
import time
from datetime import datetime
from predictWaterRequirement import custom_predict
from predictWaterRequirement import custom_predict_weather_variation
import pandas as pd
import folium
import matplotlib.pyplot as plt
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import together
soil_type = ""
weather = ""
humidity = ""
temperature = ""
acres = "" 
available_water_kl = ""


current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
together.api_key = "939528084fd82f939d2fb65ae8d7738435751a8f048b9670e1cdebe55026729f"
API_KEY = "ca427cf3782dcfec326df5af4f76b17f"

st.title("🌱 Water Requirement Predictor")


indian_cities = [
    "Ahmedabad", "Amritsar", "Aurangabad", "Bangalore", "Bhopal", "Bhubaneswar", "Chandigarh",
    "Chennai", "Coimbatore", "Cuttack", "Dehradun", "Delhi", "Dhanbad", "Durgapur", "Faridabad",
    "Ghaziabad", "Goa", "Guwahati", "Gwalior", "Hubli", "Hyderabad", "Indore", "Jabalpur",
    "Jaipur", "Jalandhar", "Jammu", "Jamshedpur", "Jhansi", "Jodhpur", "Kanpur", "Kochi",
    "Kolhapur", "Kolkata", "Kota", "Lucknow", "Ludhiana", "Madurai", "Mangalore", "Meerut",
    "Mumbai", "Mysore", "Nagpur", "Nashik", "Navi Mumbai", "Noida", "Patna", "Pimpri-Chinchwad",
    "Pondicherry", "Prayagraj", "Pune", "Raipur", "Rajkot", "Ranchi", "Rourkela", "Salem",
    "Siliguri", "Srinagar", "Surat", "Thane", "Thiruvananthapuram", "Thrissur", "Tiruchirappalli",
    "Tirunelveli", "Udaipur", "Ujjain", "Vadodara", "Varanasi", "Vasai-Virar", "Vijayawada",
    "Visakhapatnam", "Warangal", "Agra", "Aligarh", "Ajmer", "Bareilly", "Belgaum", "Bilaspur",
    "Gaya", "Haldwani", "Hisar", "Jamnagar", "Kakinada", "Karnal", "Kharagpur", "Kollam",
    "Korba", "Moradabad", "Muzaffarpur", "Nanded", "Nellore", "Panipat", "Rewa", "Rohtak",
    "Saharanpur", "Sambalpur", "Satna", "Shimla", "Solapur", "Sonipat", "Tirupati", "Tumkur" , "Kerala"
]

city = st.selectbox("Search for a city", sorted(indian_cities))


crop_options = ['Banana', 'Soyabean', 'Cabbage', 'Potato', 'Rice', 'Melon', 'Maize',
                'Citrus', 'Bean', 'Wheat', 'Mustard', 'Cotton', 'Sugarcane', 'Tomato', 'Onion']

#regionhumid_options = ['DESERT', 'SEMI ARID', 'SEMI HUMID', 'HUMID']

#temperature_options = ['10-20', '20-30', '30-40', '40-50']

#weather_options = ['NORMAL', 'SUNNY', 'WINDY', 'RAINY']

soiltype_options = ['Dry', 'Humid', 'Wet']

# Streamlit selectboxes
crop_type = st.selectbox("Crop Type", crop_options)
soil_type = st.selectbox("Soil Type", soiltype_options)
acres = st.number_input("Enter Area (in acres)", min_value=0.1, step=0.1)
city_type = city
available_water_kl = st.number_input("Enter available water (in kiloliters) (only needed for crop recommendation else leave blank)", min_value=0.0, step=0.1) 



if st.button("🔮 Predict Water Requirement"):
    st.success("Thinking like a farmer... predicting like a model 🤖🌿")
    st.markdown(f"""
        ---
        """)
    
    if city_type:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_type}&appid={API_KEY}&units=metric"
        
        response = requests.get(url)
        data = response.json()
        main_temperature = data["main"]["temp"]
        main_weather = data["weather"][0]["description"]
        main_humidity = data["main"]["humidity"]

        with st.spinner('Loading live data'):
            time.sleep(2)


        main_weather = main_weather.lower()
        if main_weather in ['clear']:
            weather = "SUNNY"
        elif main_weather in ['rain', 'drizzle', 'thunderstorm']:
            weather = "RAINY"
        elif main_weather in ['squall', 'tornado']:
            weather = "WINDY"
        else:
            weather = "NORMAL"

        if main_humidity <= 20:
            humidity  = "DESERT"
        elif main_humidity <= 40:
            humidity  = "SEMI ARID"
        elif main_humidity <= 60:
            humidity  = "SEMI HUMID"
        else:
            humidity  = "HUMID"

        if 10 <= main_temperature < 20:
            temperature = "10-20"
        elif 20 <= main_temperature < 30:
            temperature = "20-30"
        elif 30 <= main_temperature < 40:
            temperature = "30-40"
        elif 40 <= main_temperature <= 50:
            temperature = "40-50"
        else:
            temperature = "40-50"

        st.markdown(f"""
    <div style="background-color:#111827;padding:1.2rem;border-radius:12px;border:1px solid 2d3748;">
    <h4 style="color:38bdf8;font-weight:600;">📡 Local Climate Snapshot <span style="font-size:0.85rem;color:10b981;">(Live • {current_time})</span></h4>
    <p style="color:e5e7eb;font-size:1rem;">
       ✅ <b>Temperature:</b> {main_temperature}°C  
       <br>
       ✅ <b>Weather:</b> {main_weather.capitalize()}  
       <br>
       ✅ <b>Humidity:</b> {main_humidity}  
       <br><br>
       <span style="color:94a3b8;">Optimized for smarter crop decisions 🌱</span>
    </p>
    </div>
    """, unsafe_allow_html=True)

        user_input = {
        "CROP TYPE": crop_type.capitalize(),
        "SOIL TYPE": soil_type.capitalize(),
        "REGION": humidity.capitalize(),
        "TEMPERATURE": temperature,
        "WEATHER CONDITION": weather.capitalize()
}       
        

        st.markdown(f"""
        ---
        """)

        with st.spinner('Calculating optimal irrigation needs...'):
            time.sleep(2)
        df , prediction = custom_predict(user_input)
    
        area_m2 = acres * 4046.86
        total_liters = prediction[0] * area_m2
        total_kl = total_liters / 1000

        st.markdown(f"""
<div style="background-color:#1e293b;padding:1.2rem;border-radius:12px;border:1px solid #334155;">
    <h4 style="color:#38bdf8;font-weight:600;">💧 Water Requirement Summary per Irrigation</h4>
    <p style="color:#f1f5f9;font-size:1rem;">
       ✅ <b>Estimated Water Requirement:</b> <span style="color:#10b981;">{prediction[0]:.2f} mm</span> per m²  
       <br>
       ✅ <b>Selected Area:</b> {acres:.2f} acres  
       <br>
       ✅ <b>Total Water Required:</b> <span style="color:#fbbf24;">{total_kl:,.2f} kiloliters</span> (≈ {total_liters:,.0f} liters)
       <br><br>
       <span style="color:#94a3b8;">Plan irrigation accordingly to optimize usage 🌾</span>
    </p>
</div>
""", unsafe_allow_html=True)
        st.markdown(f"""
        ---
        """)
        with st.spinner("🤖 Analyzing how weather affects crop water requirements..."):
            time.sleep(2)
        image_buf = custom_predict_weather_variation(user_input)
        st.image(image_buf, caption="Water Requirement vs Weather",use_container_width=True)
        st.markdown(f"""
        ---
        """)
        st.write("#### Input Data")
        st.write(user_input)

        st.session_state.prediction_data = {
            "user_input": user_input,
            "prediction": prediction,
            "acres": acres,
            "total_kl": total_kl,
            "total_liters": total_liters
        }
        st.session_state.prediction_data["image_buf"] = image_buf

        
    

if "prediction_data" in st.session_state:
    if st.button("📄 Generate PDF Report"):
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=A4)
        width, height = A4

        # Unpack from session state
        data = st.session_state.prediction_data
        user_input = data["user_input"]
        prediction = data["prediction"]
        acres = data["acres"]
        total_kl = data["total_kl"]
        total_liters = data["total_liters"]

        # Title
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width / 2.0, height - 60, "Water Requirement Report")

        # Timestamp
        c.setFont("Helvetica", 10)
        c.drawRightString(width - 40, height - 30, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # User Input Section
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 100, "• User Input")
        c.setFont("Helvetica", 12)
        y = height - 120
        for key, value in user_input.items():
            c.drawString(60, y, f"{key}: {value}")
            y -= 20

        # Prediction Section
        c.setFont("Helvetica-Bold", 14)
        y -= 20
        c.drawString(50, y, "• Prediction Results")
        y -= 20
        c.setFont("Helvetica", 12)
        c.drawString(60, y, f"Estimated Requirement: {prediction[0]:.2f} mm per m²")
        y -= 20
        c.drawString(60, y, f"Area Entered: {acres:.2f} acres")
        y -= 20
        c.drawString(60, y, f"Total Requirement: {total_kl:,.2f} kiloliters ({total_liters:,.0f} liters)")
        y -= 40

        # Footer
        c.setFont("Helvetica-Oblique", 11)
        c.drawString(50, y, "Plan irrigation wisely to optimize water usage and sustainability.")

        image_buf = data["image_buf"]
        image_buf.seek(0)  # Rewind to start
        chart_image = ImageReader(image_buf)

        # Optional: Resize and position chart image
        chart_width = 400
        chart_height = 250
        x_pos = (width - chart_width) / 2
        y_pos = y - chart_height - 20  # leave space below last text

        # Draw image on the PDF
        c.drawImage(chart_image, x_pos, y_pos, width=chart_width, height=chart_height)

        # Finalize and offer download
        c.save()
        pdf_buffer.seek(0)

        st.download_button(
            label="⬇️ Download Water Report PDF",
            data=pdf_buffer,
            file_name="water_requirement_report.pdf",
            mime="application/pdf"
        )


    if st.button("🤖 Recommend Crop"):
        prompt = f"""
        You are an expert AI in agriculture and irrigation.

        Based on the details provided, choose:
        - The single most suitable crop from the list.
        - The most appropriate irrigation method from the list.
        
        Your answer must:
        - Be written in plain, natural English
        - Be exactly **two short sentences**
        - Avoid any lists, formatting, code, or repetition
        - Be concise and stop immediately after the second sentence
        
        Here are the conditions:
        - Area: {acres} acres
        - Available water: {available_water_kl} kiloliters
        - Soil type: {soil_type}
        - Weather: {weather}
        - Humidity: {humidity}
        - Temperature: {temperature}°C
        
        Available crops: {", ".join(crop_options)}
        Available irrigation methods: Drip irrigation, Sprinkler irrigation, Flood irrigation, Centre pivot         irrigation, Surface irrigation, Canal irrigation
        
        Answer:
        """
        with st.spinner("🤖 Generating Crop Recommendation"):
            response = together.Complete.create(
            prompt=prompt,
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
            max_tokens=90,  
            temperature=0.3
        )
        recommended_crop = response['choices'][0]['text'].strip().strip('"').strip("[]")
        clean_text = recommended_crop.strip().strip('"').strip("[]").replace("```", "")
        st.markdown(f"""
    <div style='background-color: #e0ffe0; padding: 15px; border-radius: 10px; border: 1px solid #b2d8b2;'>
        <h4 style='color: #2e7d32;'>🌱 AI Recommendation:</h4>
        <p style='font-size: 16px;color:#2e7d32;'>{clean_text}</p>
    </div>
    """, unsafe_allow_html=True)




                

        
        


