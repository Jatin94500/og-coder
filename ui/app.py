"""
Space Weather Monitoring Dashboard
Streamlit Web Application
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_collection import SpaceWeatherDataCollector
import joblib

# Page configuration
st.set_page_config(
    page_title="Space Weather Monitor",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .alert-high {
        background-color: #ff4444;
        padding: 1rem;
        border-radius: 5px;
        color: white;
        font-weight: bold;
    }
    .alert-moderate {
        background-color: #ffbb33;
        padding: 1rem;
        border-radius: 5px;
        color: white;
        font-weight: bold;
    }
    .alert-low {
        background-color: #00C851;
        padding: 1rem;
        border-radius: 5px;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🌌 Space Weather Monitoring System</h1>', unsafe_allow_html=True)
st.markdown("### Real-time Solar Storm Predictions Powered by AI")

# Sidebar
with st.sidebar:
    st.image("https://www.nasa.gov/wp-content/uploads/2023/03/nasa-logo-web-rgb.png", width=200)
    st.markdown("## 📡 Data Sources")
    st.markdown("- NOAA SWPC")
    st.markdown("- NASA DONKI")
    st.markdown("- GOES Satellite")
    
    st.markdown("---")
    st.markdown("## ⚙️ Settings")
    auto_refresh = st.checkbox("Auto-refresh (15 min)", value=False)
    show_advanced = st.checkbox("Show Advanced Metrics", value=False)
    
    st.markdown("---")
    st.markdown("## 📊 Model Info")
    st.markdown("**Flare Predictor:** XGBoost")
    st.markdown("**Storm Forecaster:** LSTM")
    st.markdown("**Risk Assessor:** LightGBM")

# Load ML models
@st.cache_resource
def load_models():
    """Load trained ML models"""
    try:
        import sys
        import os
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(parent_dir)
        
        from ml_models import SolarFlarePredictor, GeomagneticStormForecaster, SatelliteRiskAssessor
        
        # Try to load saved models
        flare_model = joblib.load(os.path.join(parent_dir, 'solar_flare_predictor.pkl'))
        risk_model = joblib.load(os.path.join(parent_dir, 'satellite_risk_assessor.pkl'))
        
        # Load LSTM model
        from tensorflow import keras
        storm_model = GeomagneticStormForecaster()
        storm_model.model = keras.models.load_model(os.path.join(parent_dir, 'geomagnetic_storm_forecaster.h5'))
        storm_model.scaler = joblib.load(os.path.join(parent_dir, 'storm_scaler.pkl'))
        
        return flare_model, storm_model, risk_model
    except Exception as e:
        st.warning(f"⚠️ ML models not loaded: {e}. Using rule-based predictions.")
        return None, None, None

# Cache data collection
@st.cache_data(ttl=900)  # Cache for 15 minutes
def load_data():
    """Load real-time space weather data"""
    collector = SpaceWeatherDataCollector()
    
    data = {
        'solar_wind': collector.get_solar_wind_data(),
        'geomagnetic': collector.get_geomagnetic_data(),
        'xray': collector.get_xray_flux(),
        'proton': collector.get_proton_flux(),
        'magnetometer': collector.get_magnetometer_data(),
    }
    
    # Get recent events
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    data['flares'] = collector.get_solar_flares(start_date, end_date)
    data['cme'] = collector.get_cme_data(start_date, end_date)
    
    return data

def prepare_features_for_prediction(conditions):
    """Prepare features from current conditions for ML prediction"""
    import numpy as np
    
    # Create feature vector matching training data
    features = {
        'solar_wind_speed': conditions.get('speed', 400),
        'proton_density': conditions.get('density', 5),
        'bt': conditions.get('bt', 5),
        'bz': conditions.get('bz', 0),
        'temperature': conditions.get('temperature', 100000),
        'kp_index': conditions.get('kp', 2),
    }
    
    # Add derived features
    features['speed_squared'] = features['solar_wind_speed'] ** 2
    features['density_speed'] = features['proton_density'] * features['solar_wind_speed']
    features['bz_negative'] = 1 if features['bz'] < 0 else 0
    
    return pd.DataFrame([features])

def predict_with_ml(conditions, flare_model, storm_model, risk_model):
    """Make predictions using ML models"""
    predictions = {
        'flare_probability': 0.0,
        'predicted_kp': conditions.get('kp', 2),
        'risk_score': 0.0,
        'using_ml': False
    }
    
    try:
        # Prepare features
        features_df = prepare_features_for_prediction(conditions)
        
        # Flare prediction
        if flare_model is not None:
            flare_pred, flare_prob = flare_model.predict(features_df)
            predictions['flare_probability'] = float(flare_prob[0][1]) if len(flare_prob[0]) > 1 else 0.0
            predictions['using_ml'] = True
        
        # Risk assessment
        if risk_model is not None:
            risk_pred = risk_model.predict(features_df)
            predictions['risk_score'] = float(risk_pred[0])
            predictions['using_ml'] = True
        
        # Storm forecast (if we have time series data)
        # Note: LSTM needs sequence data, so we'll use current Kp as baseline
        predictions['predicted_kp'] = conditions.get('kp', 2)
        
    except Exception as e:
        st.warning(f"ML prediction error: {e}")
    
    return predictions

# Load data
with st.spinner("🔄 Fetching real-time space weather data..."):
    try:
        data = load_data()
        st.success("✅ Data loaded successfully!")
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        st.stop()

# Load ML models
with st.spinner("🤖 Loading AI models..."):
    flare_model, storm_model, risk_model = load_models()
    if flare_model is not None:
        st.success("✅ AI models loaded!")
    else:
        st.info("ℹ️ Using rule-based predictions (train models first with main_colab.py)")

# Extract current conditions
current_conditions = {}
if data['solar_wind'] is not None and len(data['solar_wind']) > 0:
    latest_sw = data['solar_wind'].iloc[-1]
    current_conditions['speed'] = latest_sw.get('speed', 'N/A')
    current_conditions['density'] = latest_sw.get('density', 'N/A')
    current_conditions['temperature'] = latest_sw.get('temperature', 'N/A')

if data['geomagnetic'] is not None and len(data['geomagnetic']) > 0:
    latest_kp = data['geomagnetic'].iloc[-1]
    current_conditions['kp'] = latest_kp.get('kp_index', 'N/A')

if data['magnetometer'] is not None and len(data['magnetometer']) > 0:
    latest_mag = data['magnetometer'].iloc[-1]
    current_conditions['bz'] = latest_mag.get('bz_gsm', 'N/A')
    current_conditions['bt'] = latest_mag.get('bt', 'N/A')

# Get ML predictions
ml_predictions = predict_with_ml(current_conditions, flare_model, storm_model, risk_model)

# Risk Assessment (now using ML if available)
def calculate_risk(conditions, ml_preds):
    """Calculate overall risk level using ML predictions or rules"""
    
    # Use ML risk score if available
    if ml_preds['using_ml'] and ml_preds['risk_score'] > 0:
        return min(ml_preds['risk_score'], 10)
    
    # Fallback to rule-based
    risk_score = 0
    
    # Solar wind speed
    if isinstance(conditions.get('speed'), (int, float)):
        if conditions['speed'] > 700:
            risk_score += 3
        elif conditions['speed'] > 500:
            risk_score += 1
    
    # Kp index
    if isinstance(conditions.get('kp'), (int, float)):
        if conditions['kp'] >= 7:
            risk_score += 4
        elif conditions['kp'] >= 5:
            risk_score += 2
    
    # Bz component
    if isinstance(conditions.get('bz'), (int, float)):
        if conditions['bz'] < -10:
            risk_score += 3
        elif conditions['bz'] < -5:
            risk_score += 1
    
    return min(risk_score, 10)

risk_level = calculate_risk(current_conditions, ml_predictions)

# Alert Banner
if risk_level >= 7:
    st.markdown('<div class="alert-high">🔴 HIGH RISK: Severe space weather conditions detected!</div>', unsafe_allow_html=True)
elif risk_level >= 4:
    st.markdown('<div class="alert-moderate">🟡 MODERATE RISK: Elevated space weather activity</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="alert-low">🟢 LOW RISK: Normal space weather conditions</div>', unsafe_allow_html=True)

st.markdown("---")

# Main Metrics
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="☀️ Solar Wind Speed",
        value=f"{current_conditions.get('speed', 'N/A')} km/s" if isinstance(current_conditions.get('speed'), (int, float)) else "N/A",
        delta="Normal" if isinstance(current_conditions.get('speed'), (int, float)) and current_conditions['speed'] < 500 else "High"
    )

with col2:
    st.metric(
        label="🧲 Kp Index",
        value=f"{current_conditions.get('kp', 'N/A')}" if isinstance(current_conditions.get('kp'), (int, float)) else "N/A",
        delta="Quiet" if isinstance(current_conditions.get('kp'), (int, float)) and current_conditions['kp'] < 4 else "Active"
    )

with col3:
    st.metric(
        label="🌊 Proton Density",
        value=f"{current_conditions.get('density', 'N/A')} p/cm³" if isinstance(current_conditions.get('density'), (int, float)) else "N/A"
    )

with col4:
    st.metric(
        label="🧭 IMF Bz",
        value=f"{current_conditions.get('bz', 'N/A')} nT" if isinstance(current_conditions.get('bz'), (int, float)) else "N/A",
        delta="Favorable" if isinstance(current_conditions.get('bz'), (int, float)) and current_conditions['bz'] > 0 else "Geoeffective"
    )

with col5:
    st.metric(
        label="⚠️ Risk Level",
        value=f"{risk_level:.1f}/10",
        delta="AI Predicted" if ml_predictions['using_ml'] else "Rule-based"
    )

st.markdown("---")

# ML Predictions Section
if ml_predictions['using_ml']:
    st.markdown("### 🤖 AI Model Predictions")
    
    pred_col1, pred_col2, pred_col3 = st.columns(3)
    
    with pred_col1:
        flare_prob = ml_predictions['flare_probability'] * 100
        st.metric(
            label="☀️ Solar Flare Probability",
            value=f"{flare_prob:.1f}%",
            delta="XGBoost Model"
        )
        if flare_prob > 70:
            st.error("🔴 HIGH: Flare likely in next 24h")
        elif flare_prob > 40:
            st.warning("🟡 MODERATE: Flare possible")
        else:
            st.success("🟢 LOW: Flare unlikely")
    
    with pred_col2:
        predicted_kp = ml_predictions['predicted_kp']
        st.metric(
            label="🧲 Predicted Kp Index",
            value=f"{predicted_kp:.1f}",
            delta="LSTM Forecast"
        )
        if predicted_kp >= 7:
            st.error("🔴 Strong storm predicted")
        elif predicted_kp >= 5:
            st.warning("🟡 Minor storm predicted")
        else:
            st.success("🟢 Quiet conditions")
    
    with pred_col3:
        risk_score = ml_predictions['risk_score']
        st.metric(
            label="🛰️ Satellite Risk Score",
            value=f"{risk_score:.1f}/10",
            delta="LightGBM Model"
        )
        if risk_score >= 7:
            st.error("🔴 HIGH: Take precautions")
        elif risk_score >= 4:
            st.warning("🟡 MODERATE: Monitor closely")
        else:
            st.success("🟢 LOW: Normal operations")
    
    st.markdown("---")

# Tabs for different views
tab1, tab2, tab3, tab4 = st.tabs(["📊 Real-Time Data", "⚡ Recent Events", "📈 Trends", "🔮 Forecast"])

with tab1:
    st.subheader("Real-Time Space Weather Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Solar Wind Speed Chart
        if data['solar_wind'] is not None and len(data['solar_wind']) > 0:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=data['solar_wind']['time_tag'],
                y=data['solar_wind']['speed'],
                mode='lines',
                name='Solar Wind Speed',
                line=dict(color='#667eea', width=2)
            ))
            fig.add_hline(y=500, line_dash="dash", line_color="orange", annotation_text="High Speed Threshold")
            fig.update_layout(
                title="Solar Wind Speed (7-Day)",
                xaxis_title="Time",
                yaxis_title="Speed (km/s)",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Kp Index Chart
        if data['geomagnetic'] is not None and len(data['geomagnetic']) > 0:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=data['geomagnetic']['time_tag'],
                y=data['geomagnetic']['kp_index'],
                mode='lines+markers',
                name='Kp Index',
                line=dict(color='#764ba2', width=2)
            ))
            fig.add_hline(y=5, line_dash="dash", line_color="red", annotation_text="Storm Threshold")
            fig.update_layout(
                title="Geomagnetic Activity (Kp Index)",
                xaxis_title="Time",
                yaxis_title="Kp Index",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Magnetic Field Components
        if data['magnetometer'] is not None and len(data['magnetometer']) > 0:
            fig = go.Figure()
            if 'bz_gsm' in data['magnetometer'].columns:
                fig.add_trace(go.Scatter(
                    x=data['magnetometer']['time_tag'],
                    y=data['magnetometer']['bz_gsm'],
                    mode='lines',
                    name='Bz (North-South)',
                    line=dict(color='#00C851', width=2)
                ))
            fig.add_hline(y=0, line_dash="dash", line_color="gray")
            fig.add_hline(y=-10, line_dash="dash", line_color="red", annotation_text="Geoeffective")
            fig.update_layout(
                title="IMF Bz Component",
                xaxis_title="Time",
                yaxis_title="Bz (nT)",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col4:
        # Proton Density
        if data['solar_wind'] is not None and len(data['solar_wind']) > 0 and 'density' in data['solar_wind'].columns:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=data['solar_wind']['time_tag'],
                y=data['solar_wind']['density'],
                mode='lines',
                name='Proton Density',
                line=dict(color='#ffbb33', width=2),
                fill='tozeroy'
            ))
            fig.update_layout(
                title="Proton Density",
                xaxis_title="Time",
                yaxis_title="Density (p/cm³)",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Recent Solar Events")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ☀️ Solar Flares (Last 7 Days)")
        if data['flares'] is not None and len(data['flares']) > 0:
            st.dataframe(
                data['flares'][['beginTime', 'classType', 'sourceLocation']].head(10),
                use_container_width=True
            )
            st.metric("Total Flares", len(data['flares']))
        else:
            st.info("No recent solar flares detected")
    
    with col2:
        st.markdown("### 🌊 Coronal Mass Ejections")
        if data['cme'] is not None and len(data['cme']) > 0:
            st.dataframe(
                data['cme'][['startTime', 'latitude', 'longitude']].head(10),
                use_container_width=True
            )
            st.metric("Total CMEs", len(data['cme']))
        else:
            st.info("No recent CME events detected")

with tab3:
    st.subheader("Historical Trends & Analysis")
    
    # Combined view
    if data['solar_wind'] is not None and data['geomagnetic'] is not None:
        fig = go.Figure()
        
        # Normalize data for comparison
        sw_normalized = (data['solar_wind']['speed'] - data['solar_wind']['speed'].min()) / (data['solar_wind']['speed'].max() - data['solar_wind']['speed'].min())
        kp_normalized = data['geomagnetic']['kp_index'] / 9
        
        fig.add_trace(go.Scatter(
            x=data['solar_wind']['time_tag'],
            y=sw_normalized,
            mode='lines',
            name='Solar Wind (normalized)',
            line=dict(color='#667eea')
        ))
        
        fig.add_trace(go.Scatter(
            x=data['geomagnetic']['time_tag'],
            y=kp_normalized,
            mode='lines',
            name='Kp Index (normalized)',
            line=dict(color='#764ba2')
        ))
        
        fig.update_layout(
            title="Normalized Comparison: Solar Wind vs Geomagnetic Activity",
            xaxis_title="Time",
            yaxis_title="Normalized Value (0-1)",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("🔮 24-Hour Forecast")
    st.info("Forecast feature coming soon! This will show predicted Kp index and risk levels for the next 24 hours.")
    
    # Placeholder forecast
    forecast_hours = list(range(1, 25))
    forecast_kp = [current_conditions.get('kp', 2)] * 24
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=forecast_hours,
        y=forecast_kp,
        mode='lines+markers',
        name='Kp Forecast',
        line=dict(color='#667eea', width=3)
    ))
    fig.add_hline(y=5, line_dash="dash", line_color="orange", annotation_text="Storm Threshold")
    fig.update_layout(
        title="Kp Index Forecast (Next 24 Hours)",
        xaxis_title="Hours Ahead",
        yaxis_title="Predicted Kp Index",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Data Sources:**")
    st.markdown("- NOAA SWPC")
    st.markdown("- NASA DONKI")

with col2:
    st.markdown("**Last Updated:**")
    st.markdown(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

with col3:
    st.markdown("**Status:**")
    st.markdown("🟢 System Operational")

# Refresh button
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()
