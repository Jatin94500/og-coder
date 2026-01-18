# 🤖 ML Model Integration in Dashboard

## How AI Models Work in the UI

### Overview

The dashboard now uses **3 trained ML models** to make real-time predictions:

1. **Solar Flare Predictor** (XGBoost) - Predicts flare probability
2. **Geomagnetic Storm Forecaster** (LSTM) - Forecasts Kp index
3. **Satellite Risk Assessor** (LightGBM) - Calculates risk score

## 🔄 Data Flow

```
Real-Time Data (NOAA/NASA)
         ↓
Feature Engineering
         ↓
ML Models (XGBoost, LSTM, LightGBM)
         ↓
Predictions & Risk Assessment
         ↓
Dashboard Display
```

## 📊 What Each Model Does

### 1. Solar Flare Predictor (XGBoost)
**Input:**
- Solar wind speed
- Proton density
- Magnetic field (Bt, Bz)
- Temperature
- X-ray flux

**Output:**
- Flare probability (0-100%)
- Classification: Will a flare occur in next 24h?

**Display:**
- 🔴 HIGH (>70%): Flare likely
- 🟡 MODERATE (40-70%): Flare possible
- 🟢 LOW (<40%): Flare unlikely

### 2. Geomagnetic Storm Forecaster (LSTM)
**Input:**
- Time series of solar wind parameters
- 24-hour lookback window
- Magnetic field components

**Output:**
- Predicted Kp index (0-9 scale)
- Storm intensity forecast

**Display:**
- 🔴 Kp ≥ 7: Strong storm
- 🟡 Kp 5-6: Minor storm
- 🟢 Kp < 5: Quiet conditions

### 3. Satellite Risk Assessor (LightGBM)
**Input:**
- Combined space weather parameters
- Current conditions
- Derived features

**Output:**
- Risk score (0-10 scale)
- Satellite/communication impact level

**Display:**
- 🔴 Risk ≥ 7: HIGH - Take precautions
- 🟡 Risk 4-6: MODERATE - Monitor
- 🟢 Risk < 4: LOW - Normal ops

## 🎯 How to Use

### Step 1: Train Models First

Before the dashboard can use ML predictions, you need to train the models:

```bash
# Run the training script
python main_colab.py
```

This creates:
- `solar_flare_predictor.pkl`
- `geomagnetic_storm_forecaster.h5`
- `storm_scaler.pkl`
- `satellite_risk_assessor.pkl`

### Step 2: Run Dashboard

```bash
cd ui
streamlit run app.py
```

The dashboard will:
1. ✅ Load trained models automatically
2. ✅ Fetch real-time data
3. ✅ Make AI predictions
4. ✅ Display results

### Step 3: View Predictions

Look for the **"🤖 AI Model Predictions"** section showing:
- Solar flare probability
- Predicted Kp index
- Satellite risk score

## 🔧 How It Works Technically

### Model Loading
```python
@st.cache_resource
def load_models():
    flare_model = joblib.load('solar_flare_predictor.pkl')
    risk_model = joblib.load('satellite_risk_assessor.pkl')
    storm_model = keras.models.load_model('geomagnetic_storm_forecaster.h5')
    return flare_model, storm_model, risk_model
```

### Feature Preparation
```python
def prepare_features_for_prediction(conditions):
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
    return pd.DataFrame([features])
```

### Making Predictions
```python
def predict_with_ml(conditions, flare_model, storm_model, risk_model):
    features_df = prepare_features_for_prediction(conditions)
    
    # Flare prediction
    flare_pred, flare_prob = flare_model.predict(features_df)
    
    # Risk assessment
    risk_pred = risk_model.predict(features_df)
    
    return {
        'flare_probability': flare_prob[0][1],
        'risk_score': risk_pred[0]
    }
```

## 📈 Model Performance

Based on training results:

| Model | Metric | Performance |
|-------|--------|-------------|
| **Flare Predictor** | Accuracy | 99.8% |
| **Storm Forecaster** | RMSE | 2.13 |
| **Risk Assessor** | R² Score | 0.999 |

## 🔄 Update Frequency

- **Real-time data:** Every 15 minutes
- **ML predictions:** Recalculated on each data refresh
- **Model retraining:** Manual (run main_colab.py)

## ⚠️ Fallback Behavior

If models are not trained yet:
- Dashboard shows: "ℹ️ Using rule-based predictions"
- Falls back to threshold-based risk calculation
- Still shows real-time data
- All features work, just without ML predictions

## 🎓 Understanding the Predictions

### Flare Probability
- Based on current solar conditions
- Predicts likelihood in next 24 hours
- Considers: wind speed, density, magnetic field

### Kp Index Forecast
- Geomagnetic activity level
- Scale: 0 (quiet) to 9 (extreme storm)
- Kp ≥ 5 = Geomagnetic storm

### Risk Score
- Overall threat to satellites/communications
- Scale: 0 (safe) to 10 (severe)
- Combines all space weather factors

## 🚀 Advanced Usage

### Custom Thresholds

Edit `app.py` to change alert levels:
```python
if flare_prob > 80:  # Change from 70
    st.error("🔴 HIGH")
```

### Add More Models

To add additional ML models:
1. Train new model in main_colab.py
2. Save with joblib
3. Load in load_models()
4. Add prediction logic
5. Display in dashboard

### Real-Time Retraining

For production, set up automated retraining:
```python
# Retrain models weekly with new data
if should_retrain():
    retrain_models()
    reload_models()
```

## 💡 Pro Tips

1. **Train models first** - Run main_colab.py before using dashboard
2. **Check model files** - Ensure .pkl and .h5 files exist
3. **Monitor accuracy** - Compare predictions with actual events
4. **Update regularly** - Retrain with new data monthly
5. **Use ensemble** - Combine ML + rule-based for best results

## 🐛 Troubleshooting

### "ML models not loaded"
**Solution:** Run `python main_colab.py` to train models first

### "Module not found"
**Solution:** Install dependencies: `pip install -r requirements.txt`

### "Prediction error"
**Solution:** Check that model files are in parent directory

### Models load but predictions are wrong
**Solution:** Retrain models with more recent data

## 📊 Example Output

When models are loaded, you'll see:

```
🤖 AI Model Predictions

☀️ Solar Flare Probability    🧲 Predicted Kp Index    🛰️ Satellite Risk Score
      23.5%                          2.3                      3.2/10
   🟢 LOW: Flare unlikely      🟢 Quiet conditions      🟢 LOW: Normal operations
   XGBoost Model               LSTM Forecast            LightGBM Model
```

## 🎯 Summary

**Without ML Models:**
- Shows real-time data ✅
- Uses rule-based risk calculation ✅
- Basic threshold alerts ✅

**With ML Models:**
- Shows real-time data ✅
- AI-powered predictions ✅
- Advanced risk assessment ✅
- Flare probability forecast ✅
- Storm intensity prediction ✅
- Satellite risk scoring ✅

---

**Train your models first, then enjoy AI-powered predictions! 🤖**
