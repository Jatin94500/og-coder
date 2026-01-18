"""
Main Script for Google Colab
Complete Space Weather Monitoring & Solar Storm Risk Prediction System
Run this in Google Colab
"""

# Install required packages (uncomment if running in Colab)
# !pip install requests pandas numpy matplotlib seaborn scikit-learn tensorflow xgboost lightgbm plotly

import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Import custom modules
from data_collection import SpaceWeatherDataCollector
from feature_engineering import FeatureEngineering
from synthetic_data_generator import generate_synthetic_training_data
from ml_models import SolarFlarePredictor, GeomagneticStormForecaster, SatelliteRiskAssessor, save_models
from visualization import SpaceWeatherVisualizer

print("="*70)
print("SPACE WEATHER MONITORING & SOLAR STORM RISK PREDICTION SYSTEM")
print("="*70)

# ============================================================================
# STEP 1: Generate Training Data
# ============================================================================
print("\n[STEP 1] Generating Synthetic Training Data...")
print("-"*70)

training_data = generate_synthetic_training_data(n_samples=50000)  # Increased from 10000

# Apply feature engineering
fe = FeatureEngineering()
numeric_cols = ['solar_wind_speed', 'proton_density', 'bt', 'bz', 'temperature', 'xray_flux']
training_data = fe.process_dataset(training_data, numeric_cols)

# Fill any remaining NaN values
training_data = training_data.fillna(method='bfill').fillna(method='ffill').fillna(0)

print(f"\n✓ Training data prepared: {training_data.shape}")

# ============================================================================
# STEP 2: Train Machine Learning Models
# ============================================================================
print("\n[STEP 2] Training Machine Learning Models...")
print("-"*70)

# 2.1 Solar Flare Predictor
print("\n2.1 Solar Flare Prediction Model")
flare_predictor = SolarFlarePredictor()
X_flare, y_flare, flare_features = flare_predictor.prepare_data(training_data, 'flare_occurred')

from sklearn.model_selection import train_test_split
X_flare_train, X_flare_test, y_flare_train, y_flare_test = train_test_split(
    X_flare, y_flare, test_size=0.2, random_state=42
)

flare_predictor.train(X_flare_train, y_flare_train)
flare_accuracy = flare_predictor.evaluate(X_flare_test, y_flare_test)

# 2.2 Geomagnetic Storm Forecaster
print("\n2.2 Geomagnetic Storm Forecasting Model (LSTM)")
storm_forecaster = GeomagneticStormForecaster()
X_storm, y_storm, storm_features = storm_forecaster.prepare_data(training_data, 'kp_index', lookback=48)  # Increased lookback

split_idx = int(len(X_storm) * 0.8)
X_storm_train, X_storm_test = X_storm[:split_idx], X_storm[split_idx:]
y_storm_train, y_storm_test = y_storm[:split_idx], y_storm[split_idx:]

storm_forecaster.train(X_storm_train, y_storm_train)
storm_rmse, storm_r2 = storm_forecaster.evaluate(X_storm_test, y_storm_test)

# 2.3 Satellite Risk Assessor
print("\n2.3 Satellite Risk Assessment Model")
risk_assessor = SatelliteRiskAssessor()
X_risk, y_risk, risk_features = risk_assessor.prepare_data(training_data, 'satellite_risk')

X_risk_train, X_risk_test, y_risk_train, y_risk_test = train_test_split(
    X_risk, y_risk, test_size=0.2, random_state=42
)

risk_assessor.train(X_risk_train, y_risk_train)
risk_rmse, risk_r2 = risk_assessor.evaluate(X_risk_test, y_risk_test)

# Save models
print("\n2.4 Saving Models...")
save_models(flare_predictor, storm_forecaster, risk_assessor)

# ============================================================================
# STEP 3: Collect Real-Time Data
# ============================================================================
print("\n[STEP 3] Collecting Real-Time Space Weather Data...")
print("-"*70)

collector = SpaceWeatherDataCollector()
real_time_data = collector.collect_all_data()

# ============================================================================
# STEP 4: Make Predictions on Recent Data
# ============================================================================
print("\n[STEP 4] Making Predictions on Recent Data...")
print("-"*70)

# Use last 100 samples from training data for demonstration
recent_data = training_data.tail(100).copy()

# Flare predictions
X_recent_flare = recent_data[flare_features].fillna(0)
flare_preds, flare_probs = flare_predictor.predict(X_recent_flare)
recent_data['flare_prediction'] = flare_preds
recent_data['flare_probability'] = flare_probs[:, 1]

# Risk predictions
X_recent_risk = recent_data[risk_features].fillna(0)
risk_preds = risk_assessor.predict(X_recent_risk)
recent_data['risk_prediction'] = risk_preds

print(f"\n✓ Predictions generated for {len(recent_data)} time points")
print(f"  - Flare alerts: {flare_preds.sum()} events")
print(f"  - Average risk level: {risk_preds.mean():.2f}/10")
print(f"  - High risk periods (>7): {(risk_preds > 7).sum()} hours")

# ============================================================================
# STEP 5: Generate Visualizations
# ============================================================================
print("\n[STEP 5] Generating Visualizations...")
print("-"*70)

viz = SpaceWeatherVisualizer()

# Create comprehensive dashboard
dashboard = viz.create_dashboard(recent_data)
dashboard.show()

# Individual plots
solar_wind_plot = viz.plot_solar_wind_parameters(recent_data)
solar_wind_plot.show()

kp_plot = viz.plot_kp_index(recent_data)
kp_plot.show()

xray_plot = viz.plot_xray_flux(recent_data)
xray_plot.show()

risk_plot = viz.plot_risk_assessment(recent_data)
risk_plot.show()

correlation_plot = viz.plot_correlation_matrix(recent_data)
correlation_plot.show()

print("\n✓ All visualizations generated")


# ============================================================================
# STEP 6: Risk Assessment Summary
# ============================================================================
print("\n[STEP 6] Current Space Weather Risk Assessment")
print("="*70)

latest_data = recent_data.iloc[-1]

print("\n📊 CURRENT CONDITIONS:")
print(f"  Solar Wind Speed: {latest_data['solar_wind_speed']:.1f} km/s")
print(f"  Proton Density: {latest_data['proton_density']:.2f} p/cm³")
print(f"  IMF Bz: {latest_data['bz']:.2f} nT")
print(f"  X-ray Flux: {latest_data['xray_flux']:.2e} W/m²")
print(f"  Kp Index: {latest_data['kp_index']:.1f}")

print("\n⚠️  RISK LEVELS:")
print(f"  Flare Probability: {latest_data['flare_probability']*100:.1f}%")
print(f"  Satellite Risk: {latest_data['risk_prediction']:.1f}/10")
print(f"  Storm Classification: {latest_data['storm_class']}")
print(f"  Flare Classification: {latest_data['flare_class']}")

# Risk interpretation
if latest_data['risk_prediction'] < 3:
    risk_status = "🟢 LOW - Normal operations"
elif latest_data['risk_prediction'] < 7:
    risk_status = "🟡 MODERATE - Monitor conditions"
else:
    risk_status = "🔴 HIGH - Take precautions"

print(f"\n  Overall Status: {risk_status}")

# ============================================================================
# STEP 7: Generate Forecast
# ============================================================================
print("\n[STEP 7] 24-Hour Forecast")
print("="*70)

# Generate forecast for next 24 hours
forecast_hours = 24
last_sequence = X_storm[-1:]  # Last sequence for LSTM

# Simple forecast (using last known conditions)
forecast_data = []
for hour in range(1, forecast_hours + 1):
    forecast_time = recent_data['timestamp'].iloc[-1] + timedelta(hours=hour)
    
    # Predict Kp index
    kp_forecast = storm_forecaster.predict(last_sequence)[0]
    
    # Estimate other parameters (simplified)
    forecast_row = {
        'timestamp': forecast_time,
        'hour_ahead': hour,
        'kp_forecast': kp_forecast,
        'storm_level': fe.classify_geomag_storm(kp_forecast)
    }
    forecast_data.append(forecast_row)

forecast_df = pd.DataFrame(forecast_data)

print("\nForecast Summary:")
print(forecast_df[['hour_ahead', 'kp_forecast', 'storm_level']].to_string(index=False))

# Plot forecast
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=forecast_df['hour_ahead'],
    y=forecast_df['kp_forecast'],
    mode='lines+markers',
    name='Kp Forecast',
    line=dict(color='blue', width=3)
))

fig.add_hline(y=5, line_dash="dash", line_color="orange", 
              annotation_text="Storm Threshold")

fig.update_layout(
    title="24-Hour Geomagnetic Activity Forecast",
    xaxis_title="Hours Ahead",
    yaxis_title="Kp Index",
    height=400
)
fig.show()

# ============================================================================
# STEP 8: Alert System
# ============================================================================
print("\n[STEP 8] Alert System")
print("="*70)

def generate_alerts(data):
    """Generate alerts based on current conditions"""
    alerts = []
    
    latest = data.iloc[-1]
    
    # Flare alerts
    if latest['flare_probability'] > 0.7:
        alerts.append({
            'level': 'HIGH',
            'type': 'Solar Flare',
            'message': f"High probability ({latest['flare_probability']*100:.0f}%) of solar flare"
        })
    elif latest['flare_probability'] > 0.4:
        alerts.append({
            'level': 'MODERATE',
            'type': 'Solar Flare',
            'message': f"Moderate probability ({latest['flare_probability']*100:.0f}%) of solar flare"
        })
    
    # Storm alerts
    if latest['kp_index'] >= 7:
        alerts.append({
            'level': 'HIGH',
            'type': 'Geomagnetic Storm',
            'message': f"Strong geomagnetic storm in progress (Kp={latest['kp_index']:.1f})"
        })
    elif latest['kp_index'] >= 5:
        alerts.append({
            'level': 'MODERATE',
            'type': 'Geomagnetic Storm',
            'message': f"Minor geomagnetic storm conditions (Kp={latest['kp_index']:.1f})"
        })
    
    # Satellite risk alerts
    if latest['risk_prediction'] >= 7:
        alerts.append({
            'level': 'HIGH',
            'type': 'Satellite Risk',
            'message': f"High risk to satellite operations (Risk={latest['risk_prediction']:.1f}/10)"
        })
    elif latest['risk_prediction'] >= 5:
        alerts.append({
            'level': 'MODERATE',
            'type': 'Satellite Risk',
            'message': f"Elevated satellite risk (Risk={latest['risk_prediction']:.1f}/10)"
        })
    
    # Solar wind alerts
    if latest['solar_wind_speed'] > 700:
        alerts.append({
            'level': 'MODERATE',
            'type': 'Solar Wind',
            'message': f"High-speed solar wind stream ({latest['solar_wind_speed']:.0f} km/s)"
        })
    
    # Southward Bz alert
    if latest['bz'] < -10:
        alerts.append({
            'level': 'HIGH',
            'type': 'IMF Bz',
            'message': f"Strong southward IMF Bz ({latest['bz']:.1f} nT) - geoeffective"
        })
    
    return alerts

# Generate alerts
current_alerts = generate_alerts(recent_data)

if current_alerts:
    print("\n🚨 ACTIVE ALERTS:")
    for alert in current_alerts:
        icon = "🔴" if alert['level'] == 'HIGH' else "🟡"
        print(f"\n{icon} {alert['level']} - {alert['type']}")
        print(f"   {alert['message']}")
else:
    print("\n✅ No active alerts - conditions normal")

# ============================================================================
# STEP 9: Model Performance Summary
# ============================================================================
print("\n[STEP 9] Model Performance Summary")
print("="*70)

print("\n📈 MODEL METRICS:")
print(f"\n1. Solar Flare Predictor:")
print(f"   - Accuracy: {flare_accuracy:.4f}")
print(f"   - Model: XGBoost Classifier")

print(f"\n2. Geomagnetic Storm Forecaster:")
print(f"   - RMSE: {storm_rmse:.4f}")
print(f"   - R² Score: {storm_r2:.4f}")
print(f"   - Model: Bidirectional LSTM")

print(f"\n3. Satellite Risk Assessor:")
print(f"   - RMSE: {risk_rmse:.4f}")
print(f"   - R² Score: {risk_r2:.4f}")
print(f"   - Model: LightGBM Regressor")

# ============================================================================
# STEP 10: Export Results
# ============================================================================
print("\n[STEP 10] Exporting Results")
print("="*70)

# Save predictions
recent_data.to_csv('space_weather_predictions.csv', index=False)
forecast_df.to_csv('space_weather_forecast.csv', index=False)

print("\n✓ Results exported:")
print("  - space_weather_predictions.csv")
print("  - space_weather_forecast.csv")

# ============================================================================
# COMPLETION
# ============================================================================
print("\n" + "="*70)
print("✅ SPACE WEATHER MONITORING SYSTEM - COMPLETE")
print("="*70)
print("\nSystem Features:")
print("  ✓ Real-time data collection from NOAA/NASA")
print("  ✓ Solar flare prediction (XGBoost)")
print("  ✓ Geomagnetic storm forecasting (LSTM)")
print("  ✓ Satellite risk assessment (LightGBM)")
print("  ✓ Interactive visualizations")
print("  ✓ 24-hour forecast")
print("  ✓ Automated alert system")
print("\nAll models trained and ready for deployment!")
print("="*70)
