"""
Synthetic Data Generator
Creates realistic training data for model development
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from feature_engineering import FeatureEngineering

def generate_synthetic_training_data(n_samples=10000, seed=42):
    """
    Generate synthetic space weather data for model training
    Based on realistic parameter ranges from scientific literature
    """
    np.random.seed(seed)
    
    print(f"Generating {n_samples} synthetic training samples...")
    
    # Generate timestamps (hourly data)
    start_date = datetime(2020, 1, 1)
    timestamps = [start_date + timedelta(hours=i) for i in range(n_samples)]
    
    # Solar wind speed (km/s) - typical range 300-800, extreme up to 1000+
    solar_wind_speed = np.random.normal(450, 100, n_samples)
    solar_wind_speed = np.clip(solar_wind_speed, 250, 900)
    
    # Add occasional high-speed streams
    high_speed_events = np.random.random(n_samples) < 0.05
    solar_wind_speed[high_speed_events] += np.random.uniform(200, 400, high_speed_events.sum())
    solar_wind_speed = np.clip(solar_wind_speed, 250, 1200)
    
    # Proton density (particles/cm³) - typical 1-10, can spike to 50+
    proton_density = np.random.lognormal(1.5, 0.5, n_samples)
    proton_density = np.clip(proton_density, 0.5, 50)
    
    # IMF Bt (total magnetic field, nT) - typical 2-10
    bt = np.random.gamma(2, 2, n_samples)
    bt = np.clip(bt, 0.5, 30)
    
    # IMF Bz (north-south component, nT) - critical for geomagnetic activity
    bz = np.random.normal(0, 3, n_samples)
    
    # Add southward Bz events (negative = geoeffective)
    southward_events = np.random.random(n_samples) < 0.1
    bz[southward_events] = np.random.uniform(-20, -5, southward_events.sum())
    
    # Temperature (Kelvin) - typical 10^4 to 10^6
    temperature = np.random.lognormal(11, 0.5, n_samples)
    temperature = np.clip(temperature, 1e4, 1e6)
    
    # X-ray flux (W/m²) - log scale from 10^-9 to 10^-3
    xray_flux_log = np.random.normal(-7, 1.5, n_samples)
    xray_flux = 10 ** xray_flux_log
    xray_flux = np.clip(xray_flux, 1e-9, 1e-3)
    
    # Add flare events (M and X class)
    flare_events = np.random.random(n_samples) < 0.02
    xray_flux[flare_events] = 10 ** np.random.uniform(-5.5, -3.5, flare_events.sum())
    
    # Proton flux (particles/cm²-s-sr) - background and events
    proton_flux = np.random.lognormal(0, 2, n_samples)
    proton_flux = np.clip(proton_flux, 0.01, 1e5)
    
    # Calculate Kp index (0-9 scale)
    # Based on solar wind speed, density, and southward Bz
    kp_base = ((solar_wind_speed - 300) / 150) + (np.abs(np.minimum(bz, 0)) / 3)
    kp_base += (proton_density - 5) / 10
    kp_noise = np.random.normal(0, 0.5, n_samples)
    kp_index = np.clip(kp_base + kp_noise, 0, 9)
    
    # Dst index (nT) - measure of ring current
    # Negative values indicate storm intensity
    dst_base = -15 * solar_wind_speed * np.abs(np.minimum(bz, 0)) / 1000 - 20
    dst_noise = np.random.normal(0, 10, n_samples)
    dst_index = dst_base + dst_noise
    dst_index = np.clip(dst_index, -300, 20)
    
    # Flare classification
    fe = FeatureEngineering()
    flare_class = [fe.classify_flare_intensity(x) for x in xray_flux]
    
    # Flare occurrence (binary)
    flare_occurred = (np.array([c in ['M', 'X'] for c in flare_class])).astype(int)
    
    # Geomagnetic storm classification
    storm_class = [fe.classify_geomag_storm(k) for k in kp_index]
    
    # Storm occurrence (binary)
    storm_occurred = (kp_index >= 5).astype(int)
    
    # Satellite risk level (0-10 scale)
    # Based on multiple factors
    risk_base = (kp_index / 9) * 5 + (np.log10(xray_flux + 1e-9) + 9) * 0.5
    risk_base += (proton_flux / 1000) * 0.1
    satellite_risk = np.clip(risk_base, 0, 10)
    
    # Communication disruption probability (0-1)
    comm_disruption_prob = 1 / (1 + np.exp(-0.5 * (kp_index - 5)))
    comm_disruption_prob += (xray_flux > 1e-5).astype(float) * 0.3
    comm_disruption_prob = np.clip(comm_disruption_prob, 0, 1)
    
    # Create DataFrame
    df = pd.DataFrame({
        'timestamp': timestamps,
        'solar_wind_speed': solar_wind_speed,
        'proton_density': proton_density,
        'bt': bt,
        'bz': bz,
        'temperature': temperature,
        'xray_flux': xray_flux,
        'proton_flux': proton_flux,
        'kp_index': kp_index,
        'dst_index': dst_index,
        'flare_occurred': flare_occurred,
        'flare_class': flare_class,
        'storm_occurred': storm_occurred,
        'storm_class': storm_class,
        'satellite_risk': satellite_risk,
        'comm_disruption_prob': comm_disruption_prob
    })
    
    print(f"✓ Generated {len(df)} samples")
    print(f"\nFlare distribution:")
    print(df['flare_class'].value_counts().sort_index())
    print(f"\nStorm distribution:")
    print(df['storm_class'].value_counts())
    print(f"\nFlare events: {flare_occurred.sum()} ({flare_occurred.sum()/len(df)*100:.2f}%)")
    print(f"Storm events: {storm_occurred.sum()} ({storm_occurred.sum()/len(df)*100:.2f}%)")
    
    return df

if __name__ == "__main__":
    # Generate and save training data
    training_data = generate_synthetic_training_data(10000)
    training_data.to_csv('space_weather_training_data.csv', index=False)
    print("\n✓ Training data saved to 'space_weather_training_data.csv'")
