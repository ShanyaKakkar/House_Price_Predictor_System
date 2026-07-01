import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="House Price Predictor",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- LOAD MODEL ----------
model = joblib.load('Model/house_price_model.pkl')
model_columns = joblib.load('Model/model_columns.pkl')
feature_info = joblib.load('Model/feature_info.pkl')
# ---------- VACATION / COASTAL THEME CSS ----------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

    html, body, [class*="css"], p, span, div, label {
        font-family: 'Poppins', sans-serif;
        color: #1A1A1A !important;
    }
    .stApp { background-color: #FAFAFA; }

    h1, h2, h3 { color: #002D62 !important; font-weight: 700; }

    .hero {
        background: linear-gradient(135deg, #E6F4F7 0%, #FFFFFF 100%);
        padding: 2.5rem 2.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        border: 1px solid #cdeef4;
        text-align: center;
    }
    .hero h1 { color: #002D62 !important; font-size: 2.6rem; margin: 0; }
    .hero p { color: #FF7F50 !important; font-size: 1rem; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; margin-top: 0.5rem; }

    .info-card {
        background-color: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-top: 4px solid #E6F4F7;
        border-radius: 12px;
        padding: 1.8rem;
        box-shadow: 0 4px 15px rgba(0,45,98,0.06);
        margin-bottom: 1.5rem;
    }
    .info-card h3 { color: #002D62 !important; }

    section[data-testid="stSidebar"] {
        background-color: #E6F4F7;
    }
    section[data-testid="stSidebar"] * {
        color: #002D62 !important;
    }
    section[data-testid="stSidebar"] label {
        font-weight: 600 !important;
    }

    .stTable, .stTable * { color: #1A1A1A !important; }

    div.stButton > button {
        background-color: #FF7F50;
        color: #FFFFFF !important;
        border: none;
        border-radius: 8px;
        padding: 0.9rem 2rem;
        font-weight: 700;
        font-size: 1.1rem;
        width: 100%;
        box-shadow: 0 4px 12px rgba(255,127,80,0.35);
        transition: all 0.25s ease;
    }
    div.stButton > button:hover {
        background-color: #002D62;
        color: #FFFFFF !important;
        transform: translateY(-2px);
    }
    div.stButton > button p {
        color: #FFFFFF !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
    }

    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border-radius: 10px;
        padding: 1.5rem;
        border: 2px solid #FF7F50;
    }
    div[data-testid="stMetric"] label { color: #002D62 !important; font-weight: 600; text-transform: uppercase; font-size: 0.85rem !important; }
    div[data-testid="stMetricValue"] { color: #FF7F50 !important; font-weight: 700 !important; font-size: 2.3rem !important; }

    .footer-note { text-align: center; color: #555555 !important; font-size: 0.85rem; margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid #E0E0E0; }
    </style>
""", unsafe_allow_html=True)

# ---------- HERO ----------
st.markdown("""
    <div class="hero">
       <h1>🏠 House Price Predictor System</h1>
     </div>
""", unsafe_allow_html=True)

# ---------- SIDEBAR INPUTS ----------
st.sidebar.markdown("## 🏡 Property Details")
st.sidebar.markdown("---")

st.sidebar.markdown("### 📍 Location")
longitude = st.sidebar.slider("Longitude", feature_info['longitude'][0], feature_info['longitude'][1], -119.5)
latitude = st.sidebar.slider("Latitude", feature_info['latitude'][0], feature_info['latitude'][1], 36.0)
ocean_proximity = st.sidebar.selectbox("Ocean Proximity", feature_info['ocean_proximity_options'])

st.sidebar.markdown("---")
housing_median_age = st.sidebar.slider("Housing Median Age (yrs)", feature_info['housing_median_age'][0], feature_info['housing_median_age'][1], 25.0)
total_rooms = st.sidebar.number_input("Total Rooms", min_value=0, value=0)
population = st.sidebar.number_input("Population", min_value=0, value=0)
households = st.sidebar.number_input("Households", min_value=0, value=0)

# ---------- MAIN LAYOUT ----------
col1, col2 = st.columns([1.3, 1])

with col1:
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("### 📋 Selected Property Summary")
    summary_df = pd.DataFrame({
        "Attribute": ["Longitude", "Latitude", "Median Age", "Total Rooms",
                      "Population", "Households", "Ocean Proximity"],
        "Value": [longitude, latitude, f"{housing_median_age}", total_rooms,
                  population, households, ocean_proximity]
    })
    summary_df["Value"] = summary_df["Value"].astype(str)
    st.table(summary_df.set_index("Attribute"))
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("### 💰 Estimated Valuation")

    predict_btn = st.button("🔍 Calculate Price")

    if predict_btn:
        with st.spinner("Analyzing market data..."):
            rooms_per_household = total_rooms / households if households > 0 else 0
            population_per_household = population / households if households > 0 else 0

            input_dict = {
                'longitude': longitude, 'latitude': latitude,
                'housing_median_age': housing_median_age, 'total_rooms': total_rooms,
                'population': population, 'households': households,
                'rooms_per_household': rooms_per_household,
                'population_per_household': population_per_household,
                'ocean_proximity_INLAND': 1 if ocean_proximity == 'INLAND' else 0,
                'ocean_proximity_ISLAND': 1 if ocean_proximity == 'ISLAND' else 0,
                'ocean_proximity_NEAR BAY': 1 if ocean_proximity == 'NEAR BAY' else 0,
                'ocean_proximity_NEAR OCEAN': 1 if ocean_proximity == 'NEAR OCEAN' else 0,
            }
            input_df = pd.DataFrame([input_dict])[model_columns]
            prediction = model.predict(input_df)[0]

        st.metric("Predicted Price", f"$ {prediction:,.0f}")

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prediction,
            number={'prefix': "$", 'valueformat': ",.0f", 'font': {'color': '#002D62', 'size': 22}},
            gauge={
                'axis': {'range': [0, 600000], 'tickcolor': '#002D62'},
                'bar': {'color': '#FF7F50'},
                'bgcolor': '#FFFFFF', 'borderwidth': 1, 'bordercolor': '#002D62',
                'steps': [
                    {'range': [0, 250000], 'color': '#E6F4F7'},
                    {'range': [250000, 450000], 'color': '#B8E2EA'},
                ],
            }
        ))
        fig.update_layout(height=250, margin=dict(t=20, b=20, l=20, r=20),
                           paper_bgcolor='#FFFFFF', font={'color': '#002D62'})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Set property details in the sidebar, then click **Calculate Price**.")
    st.markdown('</div>', unsafe_allow_html=True)
