# 🌌 Space Weather Dashboard UI

A beautiful, interactive web dashboard for real-time space weather monitoring.

## 🚀 Quick Start

### Local Development

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the dashboard:**
```bash
streamlit run app.py
```

3. **Open in browser:**
The app will automatically open at `http://localhost:8501`

## 🌐 Deploy Anywhere

### Option 1: Streamlit Cloud (FREE)

1. Push this folder to GitHub
2. Go to https://streamlit.io/cloud
3. Click "New app"
4. Select your repository and `ui/app.py`
5. Deploy!

**Result:** Free public dashboard with HTTPS

### Option 2: Heroku (FREE)

1. Create `Procfile`:
```
web: streamlit run app.py --server.port=$PORT
```

2. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

### Option 3: Docker

1. Build:
```bash
docker build -t space-weather-ui .
```

2. Run:
```bash
docker run -p 8501:8501 space-weather-ui
```

### Option 4: Render (FREE)

1. Go to https://render.com
2. Create new "Web Service"
3. Connect GitHub repo
4. Build command: `pip install -r requirements.txt`
5. Start command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

## 📊 Features

### Real-Time Monitoring
- ✅ Solar wind speed
- ✅ Geomagnetic activity (Kp index)
- ✅ Magnetic field components
- ✅ Proton density
- ✅ X-ray flux

### Event Tracking
- ✅ Recent solar flares
- ✅ Coronal Mass Ejections (CME)
- ✅ Geomagnetic storms

### Visualizations
- ✅ Interactive Plotly charts
- ✅ Real-time data updates
- ✅ Historical trends
- ✅ Risk assessment

### Alert System
- 🔴 High Risk (7-10)
- 🟡 Moderate Risk (4-6)
- 🟢 Low Risk (0-3)

## 🎨 Customization

### Change Theme

Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

### Modify Refresh Rate

In `app.py`, change the cache TTL:
```python
@st.cache_data(ttl=900)  # 900 seconds = 15 minutes
```

### Add Custom Metrics

Add to the metrics section:
```python
st.metric(
    label="Your Metric",
    value="Value",
    delta="Change"
)
```

## 📱 Mobile Responsive

The dashboard is fully responsive and works on:
- 📱 Mobile phones
- 📱 Tablets
- 💻 Desktops
- 🖥️ Large screens

## 🔒 Security

### Environment Variables

For production, use environment variables for API keys:

```python
import os
nasa_api_key = os.getenv('NASA_API_KEY', 'DEMO_KEY')
```

Set in deployment:
- **Streamlit Cloud:** Settings → Secrets
- **Heroku:** Config Vars
- **Render:** Environment Variables

## 🐛 Troubleshooting

### Port already in use
```bash
streamlit run app.py --server.port=8502
```

### Module not found
```bash
pip install -r requirements.txt
```

### Data not loading
- Check internet connection
- Verify API endpoints are accessible
- Check NOAA/NASA API status

## 📊 Performance

- **Load time:** < 3 seconds
- **Data refresh:** Every 15 minutes (configurable)
- **Memory usage:** ~200MB
- **CPU usage:** Low

## 🌟 Features Coming Soon

- [ ] Email/SMS alerts
- [ ] User authentication
- [ ] Custom alert thresholds
- [ ] Historical data export
- [ ] API endpoint for integrations
- [ ] Dark mode toggle
- [ ] Multi-language support

## 📞 Support

For issues or questions:
1. Check the main README.md
2. Review NOAA API documentation
3. Check Streamlit documentation

## 📄 License

MIT License - Free to use and modify

---

**Made with ❤️ for Space Weather Monitoring**
