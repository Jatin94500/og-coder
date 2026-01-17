"""
Visualization Module
Interactive dashboards and plots for space weather monitoring
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class SpaceWeatherVisualizer:
    """
    Creates interactive visualizations for space weather data
    """
    
    def __init__(self):
        self.colors = {
            'flare_A': '#90EE90',
            'flare_B': '#FFD700',
            'flare_C': '#FFA500',
            'flare_M': '#FF6347',
            'flare_X': '#DC143C',
            'storm_none': '#90EE90',
            'storm_minor': '#FFD700',
            'storm_moderate': '#FFA500',
            'storm_strong': '#FF6347',
            'storm_severe': '#DC143C',
            'storm_extreme': '#8B0000'
        }
    
    def plot_solar_wind_parameters(self, df):
        """Plot solar wind speed, density, and temperature"""
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=('Solar Wind Speed', 'Proton Density', 'Temperature'),
            vertical_spacing=0.1
        )
        
        # Solar wind speed
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['solar_wind_speed'],
                      mode='lines', name='Speed (km/s)',
                      line=dict(color='blue', width=2)),
            row=1, col=1
        )
        
        # Proton density
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['proton_density'],
                      mode='lines', name='Density (p/cm³)',
                      line=dict(color='green', width=2)),
            row=2, col=1
        )
        
        # Temperature
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['temperature'],
                      mode='lines', name='Temperature (K)',
                      line=dict(color='red', width=2)),
            row=3, col=1
        )
        
        fig.update_layout(
            height=800,
            title_text="Solar Wind Parameters",
            showlegend=False
        )
        
        return fig
    
    def plot_magnetic_field(self, df):
        """Plot IMF components"""
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Total Magnetic Field (Bt)', 'Bz Component'),
            vertical_spacing=0.15
        )
        
        # Bt
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['bt'],
                      mode='lines', name='Bt (nT)',
                      line=dict(color='purple', width=2)),
            row=1, col=1
        )
        
        # Bz with color coding (negative = geoeffective)
        colors = ['red' if bz < 0 else 'blue' for bz in df['bz']]
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['bz'],
                      mode='lines', name='Bz (nT)',
                      line=dict(color='orange', width=2)),
            row=2, col=1
        )
        
        # Add zero line for Bz
        fig.add_hline(y=0, line_dash="dash", line_color="gray", row=2, col=1)
        
        fig.update_layout(
            height=600,
            title_text="Interplanetary Magnetic Field",
            showlegend=False
        )
        
        return fig
    
    def plot_kp_index(self, df):
        """Plot Kp index with storm level indicators"""
        fig = go.Figure()
        
        # Kp index line
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['kp_index'],
                      mode='lines+markers', name='Kp Index',
                      line=dict(color='darkblue', width=2),
                      marker=dict(size=4))
        )
        
        # Storm level thresholds
        storm_levels = [
            (5, 'G1-Minor', 'yellow'),
            (6, 'G2-Moderate', 'orange'),
            (7, 'G3-Strong', 'red'),
            (8, 'G4-Severe', 'darkred'),
            (9, 'G5-Extreme', 'purple')
        ]
        
        for level, name, color in storm_levels:
            fig.add_hline(y=level, line_dash="dash", line_color=color,
                         annotation_text=name, annotation_position="right")
        
        fig.update_layout(
            title="Geomagnetic Activity (Kp Index)",
            xaxis_title="Time",
            yaxis_title="Kp Index",
            height=400,
            yaxis=dict(range=[0, 10])
        )
        
        return fig
    
    def plot_xray_flux(self, df):
        """Plot X-ray flux with flare classifications"""
        fig = go.Figure()
        
        # X-ray flux (log scale)
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['xray_flux'],
                      mode='lines', name='X-ray Flux',
                      line=dict(color='red', width=2))
        )
        
        # Flare class thresholds
        flare_levels = [
            (1e-8, 'A Class', 'green'),
            (1e-7, 'B Class', 'yellow'),
            (1e-6, 'C Class', 'orange'),
            (1e-5, 'M Class', 'red'),
            (1e-4, 'X Class', 'darkred')
        ]
        
        for level, name, color in flare_levels:
            fig.add_hline(y=level, line_dash="dash", line_color=color,
                         annotation_text=name, annotation_position="right")
        
        fig.update_layout(
            title="Solar X-ray Flux",
            xaxis_title="Time",
            yaxis_title="Flux (W/m²)",
            yaxis_type="log",
            height=400
        )
        
        return fig
    
    def plot_risk_assessment(self, df):
        """Plot satellite risk and communication disruption probability"""
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Satellite Risk Level', 'Communication Disruption Probability'),
            vertical_spacing=0.15
        )
        
        # Satellite risk
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['satellite_risk'],
                      mode='lines', name='Risk Level',
                      line=dict(color='red', width=2),
                      fill='tozeroy', fillcolor='rgba(255,0,0,0.2)'),
            row=1, col=1
        )
        
        # Communication disruption
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['comm_disruption_prob'],
                      mode='lines', name='Disruption Prob',
                      line=dict(color='orange', width=2),
                      fill='tozeroy', fillcolor='rgba(255,165,0,0.2)'),
            row=2, col=1
        )
        
        fig.update_yaxes(title_text="Risk (0-10)", row=1, col=1)
        fig.update_yaxes(title_text="Probability (0-1)", row=2, col=1)
        
        fig.update_layout(
            height=600,
            title_text="Risk Assessment",
            showlegend=False
        )
        
        return fig
    
    def create_dashboard(self, df, predictions=None):
        """Create comprehensive dashboard"""
        fig = make_subplots(
            rows=4, cols=2,
            subplot_titles=(
                'Solar Wind Speed', 'Kp Index',
                'X-ray Flux', 'Magnetic Field Bz',
                'Satellite Risk', 'Storm Classification',
                'Flare Predictions', 'System Status'
            ),
            specs=[
                [{"type": "scatter"}, {"type": "scatter"}],
                [{"type": "scatter"}, {"type": "scatter"}],
                [{"type": "scatter"}, {"type": "bar"}],
                [{"type": "indicator"}, {"type": "indicator"}]
            ],
            vertical_spacing=0.1,
            horizontal_spacing=0.1
        )
        
        # Solar Wind Speed
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['solar_wind_speed'],
                      mode='lines', name='Speed', line=dict(color='blue')),
            row=1, col=1
        )
        
        # Kp Index
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['kp_index'],
                      mode='lines+markers', name='Kp', line=dict(color='red')),
            row=1, col=2
        )
        
        # X-ray Flux
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['xray_flux'],
                      mode='lines', name='X-ray', line=dict(color='orange')),
            row=2, col=1
        )
        
        # Bz Component
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['bz'],
                      mode='lines', name='Bz', line=dict(color='purple')),
            row=2, col=2
        )
        
        # Satellite Risk
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['satellite_risk'],
                      mode='lines', name='Risk', line=dict(color='red'),
                      fill='tozeroy'),
            row=3, col=1
        )
        
        # Storm Classification
        storm_counts = df['storm_class'].value_counts()
        fig.add_trace(
            go.Bar(x=storm_counts.index, y=storm_counts.values,
                  marker_color='lightblue'),
            row=3, col=2
        )
        
        # Current Status Indicators
        current_kp = df['kp_index'].iloc[-1] if len(df) > 0 else 0
        current_risk = df['satellite_risk'].iloc[-1] if len(df) > 0 else 0
        
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=current_kp,
                title={'text': "Current Kp"},
                delta={'reference': 5},
                gauge={'axis': {'range': [None, 9]},
                      'bar': {'color': "darkblue"},
                      'steps': [
                          {'range': [0, 5], 'color': "lightgreen"},
                          {'range': [5, 7], 'color': "yellow"},
                          {'range': [7, 9], 'color': "red"}],
                      'threshold': {'line': {'color': "red", 'width': 4},
                                  'thickness': 0.75, 'value': 7}}),
            row=4, col=1
        )
        
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=current_risk,
                title={'text': "Satellite Risk"},
                gauge={'axis': {'range': [None, 10]},
                      'bar': {'color': "darkred"},
                      'steps': [
                          {'range': [0, 3], 'color': "lightgreen"},
                          {'range': [3, 7], 'color': "yellow"},
                          {'range': [7, 10], 'color': "red"}]}),
            row=4, col=2
        )
        
        fig.update_layout(
            height=1200,
            title_text="Space Weather Monitoring Dashboard",
            showlegend=False
        )
        
        return fig
    
    def plot_correlation_matrix(self, df):
        """Plot correlation matrix of key parameters"""
        numeric_cols = ['solar_wind_speed', 'proton_density', 'bt', 'bz', 
                       'temperature', 'xray_flux', 'kp_index', 'satellite_risk']
        
        corr_matrix = df[numeric_cols].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 10}
        ))
        
        fig.update_layout(
            title="Parameter Correlation Matrix",
            height=600,
            width=700
        )
        
        return fig

if __name__ == "__main__":
    print("Visualization module loaded")
