# ⚡ Quick Start - Space Weather Dashboard

## 🎯 Run Locally (2 minutes)

### Windows:
```bash
# Double-click this file:
run.bat
```

### Mac/Linux:
```bash
pip install -r requirements.txt
streamlit run app.py
```

**Dashboard opens at:** http://localhost:8501

---

## 🌐 Deploy FREE (5 minutes)

### Streamlit Cloud (Easiest):
1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Click "New app"
4. Select `ui/app.py`
5. Deploy!

**Result:** Free public dashboard with HTTPS

---

## 📁 Folder Structure

```
ui/
├── app.py                  # Main dashboard
├── requirements.txt        # Dependencies
├── run.bat                 # Windows launcher
├── Dockerfile             # Docker deployment
├── .streamlit/
│   └── config.toml        # Theme settings
└── README.md              # Full documentation
```

---

## 🎨 Features

✅ Real-time space weather data
✅ Interactive charts (Plotly)
✅ Risk assessment alerts
✅ Solar flare tracking
✅ CME event monitoring
✅ Mobile responsive
✅ Auto-refresh option

---

## 🔧 Customize

### Change Colors:
Edit `.streamlit/config.toml`

### Change Refresh Rate:
In `app.py`, line 60:
```python
@st.cache_data(ttl=900)  # 900 = 15 minutes
```

### Add Your Logo:
Replace line 45 in `app.py`:
```python
st.image("your-logo.png", width=200)
```

---

## 📱 Access Anywhere

Once deployed, access from:
- 💻 Desktop browser
- 📱 Mobile phone
- 📱 Tablet
- Any device with internet!

---

## 🆓 100% Free Options

| Platform | Cost | Setup Time |
|----------|------|------------|
| Streamlit Cloud | $0 | 5 min |
| Render | $0 | 10 min |
| Heroku | $0 | 15 min |
| Local | $0 | 2 min |

---

## 🚀 Next Steps

1. ✅ Run locally to test
2. ✅ Deploy to Streamlit Cloud
3. ✅ Share your dashboard URL
4. ✅ Add to your portfolio!

---

**Need help?** Check `README.md` or `deploy_streamlit.md`
