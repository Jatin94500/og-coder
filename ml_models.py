"""
Machine Learning Models
Solar flare prediction, geomagnetic storm forecasting, and risk assessment
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor, RandomForestRegressor
from sklearn.metrics import classification_report, confusion_matrix, mean_squared_error, r2_score, accuracy_score
import xgboost as xgb
import lightgbm as lgb
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import LSTM, Dense, Dropout, Input, Bidirectional
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import joblib
import warnings
warnings.filterwarnings('ignore')

class SolarFlarePredictor:
    """
    Predicts solar flare occurrence and classification
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        
    def prepare_data(self, df, target_col='flare_occurred'):
        """Prepare data for training"""
        # Select features
        feature_cols = [col for col in df.columns if col not in 
                       ['timestamp', 'flare_occurred', 'flare_class', 'storm_occurred', 
                        'storm_class', 'satellite_risk', 'comm_disruption_prob']]
        
        X = df[feature_cols].fillna(0)
        y = df[target_col]
        
        return X, y, feature_cols
    
    def train(self, X_train, y_train):
        """Train XGBoost classifier"""
        print("Training Solar Flare Predictor...")
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Train XGBoost
        self.model = xgb.XGBClassifier(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            eval_metric='logloss'
        )
        
        self.model.fit(X_train_scaled, y_train)
        print("✓ Solar Flare Predictor trained")
        
    def predict(self, X):
        """Predict flare occurrence"""
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        probabilities = self.model.predict_proba(X_scaled)
        return predictions, probabilities
    
    def evaluate(self, X_test, y_test):
        """Evaluate model performance"""
        predictions, probabilities = self.predict(X_test)
        
        print("\n=== Solar Flare Predictor Evaluation ===")
        print(f"Accuracy: {accuracy_score(y_test, predictions):.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, predictions))
        
        return accuracy_score(y_test, predictions)

class GeomagneticStormForecaster:
    """
    Forecasts Kp index and geomagnetic storm intensity
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        
    def prepare_data(self, df, target_col='kp_index', lookback=48):
        """Prepare time series data for LSTM with longer lookback"""
        feature_cols = ['solar_wind_speed', 'proton_density', 'bt', 'bz', 'temperature', 'xray_flux']
        
        X = df[feature_cols].fillna(method='ffill').fillna(0).values
        y = df[target_col].fillna(0).values
        
        # Create sequences with longer lookback
        X_seq, y_seq = [], []
        for i in range(lookback, len(X)):
            X_seq.append(X[i-lookback:i])
            y_seq.append(y[i])
        
        return np.array(X_seq), np.array(y_seq), feature_cols
    
    def build_lstm_model(self, input_shape):
        """Build improved LSTM model for time series forecasting"""
        model = Sequential([
            # First LSTM layer with more units
            Bidirectional(LSTM(128, return_sequences=True), input_shape=input_shape),
            Dropout(0.2),
            
            # Second LSTM layer
            Bidirectional(LSTM(64, return_sequences=True)),
            Dropout(0.2),
            
            # Third LSTM layer
            Bidirectional(LSTM(32)),
            Dropout(0.2),
            
            # Dense layers
            Dense(32, activation='relu'),
            Dropout(0.2),
            Dense(16, activation='relu'),
            Dense(1, activation='linear')
        ])
        
        # Use better optimizer
        from tensorflow.keras.optimizers import Adam
        optimizer = Adam(learning_rate=0.001)
        model.compile(optimizer=optimizer, loss='mse', metrics=['mae'])
        return model
    
    def train(self, X_train, y_train):
        """Train LSTM model with improved settings"""
        print("Training Geomagnetic Storm Forecaster...")
        
        # Scale data
        n_samples, n_timesteps, n_features = X_train.shape
        X_train_reshaped = X_train.reshape(-1, n_features)
        X_train_scaled = self.scaler.fit_transform(X_train_reshaped)
        X_train_scaled = X_train_scaled.reshape(n_samples, n_timesteps, n_features)
        
        # Build and train model
        self.model = self.build_lstm_model((n_timesteps, n_features))
        
        early_stop = EarlyStopping(monitor='loss', patience=15, restore_best_weights=True)
        reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.5, patience=7, min_lr=1e-6)
        
        self.model.fit(
            X_train_scaled, y_train,
            epochs=100,  # Increased from 50
            batch_size=32,
            callbacks=[early_stop, reduce_lr],
            verbose=0
        )
        
        print("✓ Geomagnetic Storm Forecaster trained")
    
    def predict(self, X):
        """Predict Kp index"""
        n_samples, n_timesteps, n_features = X.shape
        X_reshaped = X.reshape(-1, n_features)
        X_scaled = self.scaler.transform(X_reshaped)
        X_scaled = X_scaled.reshape(n_samples, n_timesteps, n_features)
        
        predictions = self.model.predict(X_scaled, verbose=0)
        return predictions.flatten()
    
    def evaluate(self, X_test, y_test):
        """Evaluate model performance"""
        predictions = self.predict(X_test)
        
        mse = mean_squared_error(y_test, predictions)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, predictions)
        
        print("\n=== Geomagnetic Storm Forecaster Evaluation ===")
        print(f"RMSE: {rmse:.4f}")
        print(f"R² Score: {r2:.4f}")
        
        return rmse, r2

class SatelliteRiskAssessor:
    """
    Assesses risk to satellites and communication systems
    """
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
    
    def prepare_data(self, df, target_col='satellite_risk'):
        """Prepare data for training"""
        feature_cols = [col for col in df.columns if col not in 
                       ['timestamp', 'flare_occurred', 'flare_class', 'storm_occurred', 
                        'storm_class', 'satellite_risk', 'comm_disruption_prob']]
        
        X = df[feature_cols].fillna(0)
        y = df[target_col]
        
        return X, y, feature_cols
    
    def train(self, X_train, y_train):
        """Train LightGBM regressor"""
        print("Training Satellite Risk Assessor...")
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Train LightGBM
        self.model = lgb.LGBMRegressor(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            num_leaves=31,
            random_state=42,
            verbose=-1
        )
        
        self.model.fit(X_train_scaled, y_train)
        print("✓ Satellite Risk Assessor trained")
    
    def predict(self, X):
        """Predict satellite risk level"""
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        return np.clip(predictions, 0, 10)
    
    def evaluate(self, X_test, y_test):
        """Evaluate model performance"""
        predictions = self.predict(X_test)
        
        mse = mean_squared_error(y_test, predictions)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, predictions)
        
        print("\n=== Satellite Risk Assessor Evaluation ===")
        print(f"RMSE: {rmse:.4f}")
        print(f"R² Score: {r2:.4f}")
        
        return rmse, r2

def save_models(flare_model, storm_model, risk_model):
    """Save trained models"""
    joblib.dump(flare_model, 'solar_flare_predictor.pkl')
    storm_model.model.save('geomagnetic_storm_forecaster.h5')
    joblib.dump(storm_model.scaler, 'storm_scaler.pkl')
    joblib.dump(risk_model, 'satellite_risk_assessor.pkl')
    print("\n✓ All models saved successfully")

def load_models():
    """Load trained models"""
    flare_model = joblib.load('solar_flare_predictor.pkl')
    storm_model = GeomagneticStormForecaster()
    storm_model.model = keras.models.load_model('geomagnetic_storm_forecaster.h5')
    storm_model.scaler = joblib.load('storm_scaler.pkl')
    risk_model = joblib.load('satellite_risk_assessor.pkl')
    return flare_model, storm_model, risk_model
