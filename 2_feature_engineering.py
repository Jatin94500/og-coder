"""
Feature Engineering Module
Creates features for machine learning models
"""

import pandas as pd
import numpy as np
from datetime import datetime

class FeatureEngineering:
    """
    Creates features for machine learning models from space weather data
    """
    
    @staticmethod
    def create_time_features(df, time_column='time_tag'):
        """Extract temporal features"""
        df = df.copy()
        df['hour'] = df[time_column].dt.hour
        df['day'] = df[time_column].dt.day
        df['month'] = df[time_column].dt.month
        df['day_of_week'] = df[time_column].dt.dayofweek
        df['day_of_year'] = df[time_column].dt.dayofyear
        df['quarter'] = df[time_column].dt.quarter
        
        # Cyclical encoding for time features
        df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
        df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
        df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
        df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
        
        return df
    
    @staticmethod
    def create_rolling_features(df, columns, windows=[3, 6, 12, 24]):
        """Create rolling statistics"""
        df = df.copy()
        for col in columns:
            if col in df.columns:
                for window in windows:
                    df[f'{col}_rolling_mean_{window}'] = df[col].rolling(window=window, min_periods=1).mean()
                    df[f'{col}_rolling_std_{window}'] = df[col].rolling(window=window, min_periods=1).std()
                    df[f'{col}_rolling_max_{window}'] = df[col].rolling(window=window, min_periods=1).max()
                    df[f'{col}_rolling_min_{window}'] = df[col].rolling(window=window, min_periods=1).min()
        return df
    
    @staticmethod
    def create_lag_features(df, columns, lags=[1, 3, 6, 12, 24]):
        """Create lagged features"""
        df = df.copy()
        for col in columns:
            if col in df.columns:
                for lag in lags:
                    df[f'{col}_lag_{lag}'] = df[col].shift(lag)
        return df
    
    @staticmethod
    def create_rate_of_change(df, columns):
        """Calculate rate of change"""
        df = df.copy()
        for col in columns:
            if col in df.columns:
                df[f'{col}_roc'] = df[col].pct_change()
                df[f'{col}_diff'] = df[col].diff()
                df[f'{col}_diff_2'] = df[col].diff(periods=2)
        return df
    
    @staticmethod
    def create_interaction_features(df):
        """Create interaction features between key parameters"""
        df = df.copy()
        
        # Solar wind dynamic pressure
        if 'solar_wind_speed' in df.columns and 'proton_density' in df.columns:
            df['dynamic_pressure'] = df['proton_density'] * (df['solar_wind_speed'] ** 2)
        
        # Electric field (simplified)
        if 'solar_wind_speed' in df.columns and 'bz' in df.columns:
            df['electric_field'] = df['solar_wind_speed'] * np.abs(df['bz'])
        
        # Alfven Mach number (simplified)
        if 'solar_wind_speed' in df.columns and 'bt' in df.columns:
            df['alfven_mach'] = df['solar_wind_speed'] / (df['bt'] + 1)
        
        return df
    
    @staticmethod
    def classify_flare_intensity(flux_value):
        """Classify X-ray flux into flare classes (A, B, C, M, X)"""
        if pd.isna(flux_value) or flux_value <= 0:
            return 'A'
        elif flux_value < 1e-8:
            return 'A'
        elif flux_value < 1e-7:
            return 'B'
        elif flux_value < 1e-6:
            return 'C'
        elif flux_value < 1e-5:
            return 'M'
        else:
            return 'X'
    
    @staticmethod
    def classify_geomag_storm(kp_value):
        """Classify geomagnetic storm intensity"""
        if pd.isna(kp_value):
            return 'Unknown'
        elif kp_value < 5:
            return 'None'
        elif kp_value < 6:
            return 'G1-Minor'
        elif kp_value < 7:
            return 'G2-Moderate'
        elif kp_value < 8:
            return 'G3-Strong'
        elif kp_value < 9:
            return 'G4-Severe'
        else:
            return 'G5-Extreme'
    
    @staticmethod
    def calculate_dst_index(bz, solar_wind_speed, proton_density):
        """
        Simplified Dst index calculation
        Dst (Disturbance Storm Time) indicates geomagnetic storm intensity
        """
        # Simplified Burton equation
        if pd.isna(bz) or pd.isna(solar_wind_speed) or pd.isna(proton_density):
            return 0
        
        # Electric field
        ey = solar_wind_speed * np.abs(np.minimum(bz, 0)) / 1000
        
        # Simplified Dst
        dst = -15 * ey - 20
        return dst
    
    def process_dataset(self, df, numeric_columns):
        """Apply all feature engineering steps"""
        print("Applying feature engineering...")
        
        # Time features
        if 'time_tag' in df.columns or 'timestamp' in df.columns:
            time_col = 'time_tag' if 'time_tag' in df.columns else 'timestamp'
            df = self.create_time_features(df, time_col)
        
        # Rolling features
        df = self.create_rolling_features(df, numeric_columns, windows=[6, 12, 24])
        
        # Lag features
        df = self.create_lag_features(df, numeric_columns, lags=[1, 3, 6])
        
        # Rate of change
        df = self.create_rate_of_change(df, numeric_columns)
        
        # Interaction features
        df = self.create_interaction_features(df)
        
        print(f"✓ Feature engineering complete. Total features: {df.shape[1]}")
        return df

if __name__ == "__main__":
    # Example usage
    fe = FeatureEngineering()
    print("Feature Engineering module loaded")
