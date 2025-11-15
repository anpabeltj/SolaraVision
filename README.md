# SolaraVision 🌞

A simple and interactive dashboard for analyzing solar power generation data.

---

## 📋 Problem Statement

Solar energy systems collect lots of data (power output, temperature, weather), but operators struggle to understand it. This leads to:

- 📉 Lower energy production
- ⚠️ Missed performance issues
- 🔧 Difficulty making maintenance decisions

**Solution:** A dashboard that makes solar data easy to understand!

---

## 🎯 Project Goals

1. 📊 Analyze solar power data to find trends
2. 🌡️ See how weather affects energy output
3. 📈 Calculate important performance metrics
4. 💻 Create an easy-to-use dashboard

---

## 📚 Data Source

- **From:** [Kaggle Solar Power Generation Data](https://www.kaggle.com/datasets/anikannal/solar-power-generation-data)
- **Weather Data:** ~3,200 rows (temperature, irradiation)
- **Generation Data:** ~68,800 rows (power output from inverters)
- **Time Period:** 34 days

---

## ✨ Features

### Summary Dashboard 📊

- Total energy generated
- Daily average production
- System efficiency metrics
- Temperature and weather stats
- Quick charts for trends

### Visualizations 📈

- Daily power generation trend
- Hourly power patterns
- Monthly comparisons
- Weather impact analysis
- Inverter performance comparison
- Efficiency vs temperature

### Tools 🔧

- Filter by date range
- Select specific inverters
- Export data as CSV
- Interactive charts

---

## 📁 Project Structure

```


SolaraVision/
│
├── 📄 app.py                                # Main application (entry point)
│
├── 📁 modules/                              # Core functionality modules
│   ├── data_loader.py                       # Loads and processes data
│   ├── kpi_calculator.py                    # Calculates metrics
│   ├── export_utils.py                      # Export functions
│   └── ui_components.py                     # UI elements
│
├── 📁 views/                                # Dashboard views
│   ├── summary_dashboard.py                 # Summary page
│   ├── visualization.py                     # Charts page
│   └── data_overview.py                     # Data exploration page
│
├── 📁 data/                                 # Data files folder
│   ├── Plant_1_Generation_Data.csv          # Add this (from Kaggle)
│   └── Plant_1_Weather_Sensor_Data.csv      # Add this (from Kaggle)
│
├── 📄 requirements.txt                      # Required packages
└── 📄 README.md                             # This file
```

---

## 🚀 How to Run

### 1. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it:
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Add Data Files

Download from Kaggle and place in the project folder:

- `Plant_1_Generation_Data.csv`
- `Plant_1_Weather_Sensor_Data.csv`

### 4. Run the Dashboard

```bash
streamlit run app.py
```

The dashboard opens automatically in your browser!

---

## 📂 Files & Folders

### **Main Application**

- `app.py` → Entry point (run this file)

### **Core Modules**

- `data_loader.py` → Loads CSV files and processes data
- `kpi_calculator.py` → Calculates performance metrics
- `export_utils.py` → Handles CSV exports
- `ui_components.py` → Reusable UI elements (header, filters, cards)

### **Page Modules**

- `summary_dashboard.py` → Summary page with KPIs
- `visualization.py` → Charts and analysis page
- `data_overview.py` → Raw data exploration page

### **Configuration**

- `requirements.txt` → Python packages needed
- `README.md` → Project documentation

### **Data Files** (You add these)

- `Plant_1_Generation_Data.csv` → Power generation data
- `Plant_1_Weather_Sensor_Data.csv` → Weather sensor data

---

## 🎮 How to Use

### Step 1: Activate Virtual Environment

```bash
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### Step 2: Start the Dashboard

```bash
streamlit run app.py
```

### Step 3: Navigate

Use the sidebar menu to switch between:

- 📊 Summary Dashboard
- 📈 Visualization & Analysis
- 📋 Data Overview

### Step 4: Apply Filters

- Select date range from the date picker
- Choose specific inverters from dropdown
- Filters update all charts automatically

### Step 5: Export Data

- Click "📥 Export Data (CSV)" buttons
- Files download with timestamps

---

## 🛠️ Technology

- **Python 3.8+** - Programming language
- **Streamlit** - Dashboard framework
- **Pandas** - Data processing
- **Plotly** - Interactive charts
- **NumPy** - Numerical operations

---

## 👥 Team

- Muhammad Naufal Alif Islami - 22008960
- Anpabelt Trah Javala - 24000761
- Muhammad Hafizuddin Bin Norraihizulkfli - 21001216

---

## ❓ Troubleshooting

**Can't find CSV files?**
→ Make sure CSV files are in the same folder as `app.py`

**Virtual environment not working?**
→ Make sure you activated it before installing packages

**Missing packages?**
→ Run: `pip install -r requirements.txt`

**Dashboard is slow?**
→ Select a smaller date range or fewer inverters

---

## 🙏 Credits

- Dataset from [Anikannal on Kaggle](https://www.kaggle.com/anikannal)
- Built with Streamlit, Pandas, and Plotly

---

<div align="center">

**Made with ☀️ by SolaraVision Team**

_Making solar data simple_

</div>
