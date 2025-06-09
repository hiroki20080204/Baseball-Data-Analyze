# ⚾ Baseball Data Analyze

An interactive Streamlit web app to explore and visualize Cushing Academy Varsity Penguins Spring 2025 baseball statistics.

## 📦 Features

- Dynamic player stat cards (batting, pitching, fielding)
- Player spray chart visualization
- CSV export of selected player stats
- Clean UI using HTML/CSS styling in Streamlit

## 📁 File Structure

```
├── app.py                      # Main Streamlit app
├── data.py                    # Data parser from raw CSV
├── requirements.txt           # Python dependencies
├── Cushing Academy Varsity... # Raw CSV stats file
├── baseball_field_map.png     # Spray chart image
├── mock_player_photo.png      # Placeholder player image
└── __pycache__/               # Python cache files
```

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/hiroki20080204/Baseball-Data-Analyze.git
cd Baseball-Data-Analyze
```

### 2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate.bat   # Windows
```

### 3. Install requirements
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

## 📤 Data Source
All player data is based on the CSV: `Cushing Academy Varsity Penguins Spring 2025 Stats.csv`.

## 👤 Author
GitHub: [hiroki20080204](https://github.com/hiroki20080204)

---

Enjoy analyzing player performance with clean visuals and exportable stats!