"""
Quick Test Script - Verify System Components
Run this to test individual components before full execution
"""

import sys
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("SPACE WEATHER SYSTEM - COMPONENT TEST")
print("="*70)

# Test 1: Import all modules
print("\n[TEST 1] Importing modules...")
try:
    from data_collection import SpaceWeatherDataCollector
    from feature_engineering import FeatureEngineering
    from synthetic_data_generator import generate_synthetic_training_data
    from ml_models import SolarFlarePredictor, GeomagneticStormForecaster, SatelliteRiskAssessor
    from visualization import SpaceWeatherVisualizer
    print("✓ All modules imported successfully")
except Exception as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

# Test 2: Generate small dataset
print("\n[TEST 2] Generating test data...")
try:
    test_data = generate_synthetic_training_data(n_samples=100)
    print(f"✓ Generated {len(test_data)} samples")
    print(f"  Columns: {list(test_data.columns)}")
except Exception as e:
    print(f"✗ Data generation failed: {e}")
    sys.exit(1)

# Test 3: Feature engineering
print("\n[TEST 3] Testing feature engineering...")
try:
    fe = FeatureEngineering()
    numeric_cols = ['solar_wind_speed', 'proton_density', 'bt', 'bz', 'temperature', 'xray_flux']
    test_data = fe.process_dataset(test_data, numeric_cols)
    print(f"✓ Features engineered: {test_data.shape}")
except Exception as e:
    print(f"✗ Feature engineering failed: {e}")
    sys.exit(1)

# Test 4: Model initialization
print("\n[TEST 4] Initializing models...")
try:
    flare_model = SolarFlarePredictor()
    storm_model = GeomagneticStormForecaster()
    risk_model = SatelliteRiskAssessor()
    print("✓ All models initialized")
except Exception as e:
    print(f"✗ Model initialization failed: {e}")
    sys.exit(1)

# Test 5: Data collection (optional - requires internet)
print("\n[TEST 5] Testing data collection...")
try:
    collector = SpaceWeatherDataCollector()
    solar_wind = collector.get_solar_wind_data()
    if solar_wind:
        print(f"✓ Collected {len(solar_wind)} solar wind records")
    else:
        print("⚠ No data collected (API might be unavailable)")
except Exception as e:
    print(f"⚠ Data collection warning: {e}")
    print("  (This is OK - system can work with synthetic data)")

# Test 6: Visualization
print("\n[TEST 6] Testing visualization...")
try:
    viz = SpaceWeatherVisualizer()
    print("✓ Visualizer initialized")
except Exception as e:
    print(f"✗ Visualization failed: {e}")
    sys.exit(1)

print("\n" + "="*70)
print("✅ ALL TESTS PASSED - System ready to run!")
print("="*70)
print("\nNext steps:")
print("  1. Run: python 6_main_colab.py")
print("  2. Or execute in Google Colab")
print("  3. Check generated CSV files and visualizations")
print("="*70)
