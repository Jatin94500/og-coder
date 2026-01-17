"""
SPACE WEATHER MONITORING & SOLAR STORM RISK PREDICTION SYSTEM
Complete All-in-One Script for Google Colab

This single file contains everything needed to run the system.
Simply upload to Google Colab and run!

Author: Space Weather Prediction System
Version: 1.0
"""

# ============================================================================
# INSTALLATION (Run this first in Colab)
# ============================================================================
# !pip install requests pandas numpy matplotlib seaborn scikit-learn tensorflow xgboost lightgbm plotly

import warnings
warnings.filterwarnings('ignore')

import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score, mean_squared_error, r2_score
import xgboost as xgb
import lightgbm as lgb
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow